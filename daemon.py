import os
import psutil
import signal
import sys
import time
import logging

logger = logging.getLogger('custom_logger')


class Daemon(object):

    def __init__(self, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.startDelay = 1
        self.hardKillDelay = 3
        self.processName = os.path.basename(sys.argv[0])
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr

    @staticmethod
    def _sigterm_handler(signum, frame):
        logger.warning('Received signal SIGTERM..')

    @staticmethod
    def on_daemon_termination(proc):
        logger.info(f'The daemon process with PID {proc.pid} has terminated')

    def _make_daemon(self):
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            m = f"Fork #1 failed: {e}"
            logger.error(m)
            sys.exit(1)

        # Decouple from the parent environment.
        os.chdir("/")
        os.setsid()
        os.umask(0)

        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            m = f"Fork #2 failed: {e}"
            logger.error(m)
            sys.exit(1)

        logger.info('The daemon process is going to background')

        # Redirect standard file descriptors.
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(self.stdin, 'r')
        so = open(self.stdout, 'a+')
        se = open(self.stderr, 'a+')
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

    def _get_process(self):
        procs = []
        for proc in psutil.process_iter(['name', 'pid', 'cmdline']):
            if self.processName in [cmd_part for cmd_part in proc.cmdline()]:
                if proc.pid != os.getpid():
                    procs.append(proc)
        return procs

    def start(self):
        # Handle signals
        signal.signal(signal.SIGINT, self._sigterm_handler)
        signal.signal(signal.SIGTERM, self._sigterm_handler)

        # Check if the daemon is already running.
        procs = self._get_process()
        if procs:
            pids = ",".join([str(p.pid) for p in procs])
            logger.info(f'Found old daemon running with PIDs {pids}')
            sys.exit(1)
        else:
            logger.info('Starting daemon')

        self._make_daemon()
        self.run()

    def status(self):
        procs = self._get_process()
        if procs:
            pids = ",".join([str(p.pid) for p in procs])
            logger.info(f'Daemon found running with PIDs {pids}')
        else:
            logger.info('No active daemon found')

    def stop(self):
        procs = self._get_process()

        if procs:
            for p in procs:
                p.terminate()

            gone, alive = psutil.wait_procs(procs, timeout=self.hardKillDelay, callback=self.on_daemon_termination)

            for p in alive:
                logger.info(f'The daemon process with PID {p.pid} was killed with SIGTERM!')
                p.kill()
        else:
            logger.info('No active daemon process found')

    def restart(self):
        self.stop()

        if self.startDelay:
            time.sleep(self.startDelay)

        self.start()

    def run(self):
        pass

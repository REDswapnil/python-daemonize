import time
import logging
from daemon import Daemon
import sys

logger = logging.getLogger('custom_logger')


class CustomDaemon(Daemon):

    def run(self):
        while True:
            logger.info("Daemon is running !")
            sys.stderr.write("Daemon is running .. \n")
            time.sleep(4)


if __name__ == '__main__':

    APP_LOGGER = 'custom_logger'

    # Initialize Logger
    logger = logging.getLogger(APP_LOGGER)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('app.log')
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s -> %(message)s\n')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)

    daemon = CustomDaemon()
    usageMessage = f"Usage: {sys.argv[0]} (start|stop|restart|status)"
    if len(sys.argv) == 2:
        choice = sys.argv[1]
        if choice == "start":
            daemon.start()
        elif choice == "stop":
            daemon.stop()
        elif choice == "restart":
            daemon.restart()
        elif choice == "status":
            daemon.status()
        else:
            print(usageMessage)
            sys.exit(1)
        sys.exit(0)
    else:
        print(usageMessage)
        sys.exit(1)

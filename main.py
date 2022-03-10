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

    logging.basicConfig(filename='app.log',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s  - %(message)s \n',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    daemon = CustomDaemon()
    usageMessage = f"Usage: {sys.argv[0]} (start|stop|restart|status|reload|version)"
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
        elif choice == "reload":
            daemon.reload()
        elif choice == "version":
            daemon.version()
        else:
            print("Unknown command.")
            print(usageMessage)
            sys.exit(1)
        sys.exit(0)
    else:
        print(usageMessage)
        sys.exit(1)

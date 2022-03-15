## INTRODUCTION

This is a python3 script that can be used to create background daemons of other python3 projects.

---

## USAGE

A 'requirements.txt' file which mentions the only external package needed for the script i.e. psutil, which is used to get status of the running daemons and extract their PIDs for restarting or stopping them.

Usage would include inheriting the Daemon class and over-riding the run() method to specify the task the daemon has to perform:

```
class CustomDaemon(Daemon):

    def run(self):
        while True:
            print("Daemon is running !")
            time.sleep(4)
```

The script can then be called by:

```python main.py (start|stop|restart|status)```

The script has a console and a basic file logger configured by default and will produce log in the project directory with the file name: ```app.log```

---

## EXPLANATION

The script performs double fork of the parent process to make sure that the daemon process is properly disassociated from the parent process.

With ```setsid()```, the child process is forced to break any associations with the controlling terminal i.e. making it independent. 

However, this also means that the daemon process could be a session leader for the new session created which could also lead to a scenario where the daemon process could acquire a controlling terminal, since it will be the first process in the new session.

The second fork ensures that the daemon process is not the session leader and cannot acquire a controlling terminal.

> Reference: https://stackoverflow.com/questions/881388/what-is-the-reason-for-performing-a-double-fork-when-creating-a-daemon

---

import time
import os
import sys
from enum import IntEnum
import Configs.bonline_task_config as btc


class Level(IntEnum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    COMPULSORY = 4  # the log information in the log file may be reused by the program


class Handler(IntEnum):
    TERMINAL = 0
    FILE = 1
    TERMINAL_AND_FILE = 2


class Logger:

    def __init__(self, btc=btc):
        self.log_level = btc.task_log_level
        self.log_handler = btc.task_log_handler
        self.log_level_info = {
            Level.DEBUG: "DEBUG",
            Level.INFO: "INFO",
            Level.WARNING: "WARNING",
            Level.ERROR: "ERROR",
            Level.COMPULSORY: "COMPULSORY"
        }

        self.log_path = btc.task_log_path
        check_path = [btc.task_storage_path, btc.task_log_path]
        for path in check_path:
            if not os.path.exists(path):
                print("[WARING][TASK] %s didn't exists" % path)
                try:
                    os.mkdir(path)
                    print("[INFO][TASK] %s has been created" % path)
                except Exception as e:
                    print("[ERROR][TASK] create path %s failed:%s" % (path, e))

    def _timestamp(self):
        return time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time()))

    def _log(self, level, info, heads=None):
        if heads is None:
            log_title = "[%s][%s] " % (self._timestamp(), self.log_level_info[level])
        else:
            log_title = "[%s][%s]" % (self._timestamp(), self.log_level_info[level])
            if type(heads) is list:
                for head in heads:
                    log_title += "[%s]" % str(head)
                log_title += " "
            else:
                log_title += "[%s] " % str(heads)
        return log_title + info

    def _write_log(self, level, task_id, log):
        log_file_path = self.get_log_path(task_id)
        if level <= Level.WARNING:
            with open(log_file_path, encoding="utf-8", mode="a") as log_file:
                log_file.write(log)
                log_file.write("\n")
        elif level >= Level.COMPULSORY:
            with open(log_file_path, encoding="utf-8", mode="a", buffering=-1) as log_file:
                log_file.write(log)
                log_file.write("\n")
                log_file.flush()

    def _print_log(self, level, log):
        print(log)
        if level >= Level.COMPULSORY:
            sys.stdout.flush()

    def get_log_path(self, task_id):
        return os.path.join(self.log_path, "task_%s.out" % str(task_id))

    def log(self, level, task_id, info, heads=None, handler=None):
        if handler is None:
            handler = self.log_handler
        if level >= self.log_level:
            log = self._log(level, info, heads)
            if level == Level.COMPULSORY or handler == Handler.FILE or handler == Handler.TERMINAL_AND_FILE:
                self._write_log(level, task_id, log)
            if handler == Handler.TERMINAL or handler == Handler.TERMINAL_AND_FILE:
                self._print_log(level, log)

logger = Logger()

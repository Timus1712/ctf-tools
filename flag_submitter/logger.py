#!/usr/bin/python

from __future__ import print_function
from __future__ import unicode_literals

import sys
import time


class Logger:
    DEBUG = 1
    INFO = 2
    ERROR = 3
    LEVELS = ("", "DEBUG", "INFO ", "ERR")

    def __init__(self, name="", logfilename=None, level=0):
        self.name = name
        self.level = level
        if logfilename:
            self.logfile = open(logfilename, "a")
        else:
            self.logfile = None

    def log(self, level, msg, *args):
        t = time.localtime()
        formatted_message = "[{0} {1} {2}] {3}".format(
            self.name,
            self.LEVELS[level],
            ("%02d:%02d:%02d" % (t.tm_hour, t.tm_min, t.tm_sec)),
            msg % args
        )
        if level >= self.level:
            print(formatted_message, file=sys.stderr)
        if self.logfile:
            print(formatted_message, file=self.logfile)

    def debug(self, msg, *args):
        self.log(self.DEBUG, msg, *args)

    def info(self, msg, *args):
        self.log(self.INFO, msg, *args)

    def error(self, msg, *args):
        self.log(self.ERROR, msg, *args)

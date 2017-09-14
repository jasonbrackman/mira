class Logger(object):

    def __init__(self, lib=None):
        self.__lib = lib

    def info(self, text):
        print self.__lib
        print "[MIRA] info: %s" % text

    def warning(self, text):
        print self.__lib
        print "[MIRA] warning: %s" % text

    def error(self, text):
        print self.__lib
        print "[MIRA] error: %s" % text



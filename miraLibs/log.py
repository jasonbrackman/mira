class Log(object):

    @classmethod
    def info(cls, text):
        print "[MIRA] info: %s" % text

    @classmethod
    def warning(cls, text):
        print "[MIRA] warning: %s" % text

    @classmethod
    def error(cls, text):
        print "[MIRA] error: %s" % text

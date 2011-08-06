import sys

class Color(object):
    DEBUG = '\033[35m'
    INFO = '\033[32m'
    ERROR = '\033[31m'
    ENDC = '\033[0m'
    
    @classmethod
    def _deco(cls, msg, color):
        return '%s%s%s' % (color, msg, cls.ENDC)
    
    @classmethod
    def debug(cls, msg):
        return cls._deco(msg, cls.DEBUG)
    @classmethod
    def info(cls, msg):
        return cls._deco(msg, cls.INFO)
    @classmethod
    def error(cls, msg):
        return cls._deco(msg, cls.ERROR)

class Logger(object):    
    def debug(self, msg):
        self._stdout(Color.debug("DEBUG: %s\n" % msg))
    
    def log(self, msg):
        self._stdout("%s\n" % (msg))
    
    def info(self, msg):
        self._stdout(Color.info('%s\n' % msg))
        
    def error(self, msg):
        self._stderr(Color.error("ERROR: %s\n" % msg))
        
    def _stdout(self, msg):
        sys.stdout.write(msg)
        sys.stdout.flush()
    def _stderr(self, msg):
        sys.stderr.write(msg)
        sys.stderr.flush()

logger = Logger()

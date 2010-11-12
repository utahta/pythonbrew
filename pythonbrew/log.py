import sys
import logging

class Logger(object):
    
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    ERROR = logging.ERROR
    
    def __init__(self):
        self._consumers = []
        consumer = logging.getLogger('info')
        consumer.setLevel(Logger.INFO)
        hdlr = logging.StreamHandler(sys.stdout)
        hdlr.setFormatter(logging.Formatter("%(message)s"))
        consumer.addHandler(hdlr)
        self.add_consumer(Logger.INFO, consumer)
        
        consumer = logging.getLogger('error')
        consumer.setLevel(Logger.ERROR)
        hdlr = logging.StreamHandler(sys.stderr)
        hdlr.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        consumer.addHandler(hdlr)
        self.add_consumer(Logger.ERROR, consumer)
    
    def debug(self, msg, *args, **keys):
        self._log(Logger.DEBUG, msg, *args, **keys)
    
    def info(self, msg, *args, **keys):
        self._log(Logger.INFO, msg, *args, **keys)
        
    def error(self, msg, *args, **keys):
        self._log(Logger.ERROR, msg, *args, **keys)
    
    def _log(self, level, msg, *args, **keys):
        for (consumer_level, consumer) in self._consumers:
            if level == consumer_level:
                consumer.log(level, msg, *args, **keys)
    
    def add_consumer(self, level, consumer):
        self._consumers.append((level, consumer))

logger = Logger()

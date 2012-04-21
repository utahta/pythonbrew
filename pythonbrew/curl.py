import sys
import re
import subprocess
from subprocess import Popen, PIPE
from pythonbrew.log import logger
from pythonbrew.util import to_str
from pythonbrew.exceptions import CurlFetchException

class Curl(object):
    def __init__(self):
        returncode = subprocess.call("command -v curl > /dev/null", shell=True)
        if returncode:
            logger.log("pythonbrew required curl. curl was not found in your path.")
            sys.exit(1)
    
    def read(self, url):
        p = Popen('curl -skL "%s"' % url, stdout=PIPE, shell=True)
        p.wait()
        if p.returncode:
            raise Exception('Failed to read.')
        return p.stdout.read()
    
    def readheader(self, url):
        p = Popen('curl --head -skL "%s"' % url, stdout=PIPE, shell=True)
        p.wait()
        if p.returncode:
            raise Exception('Failed to readheader.')
        respinfo = {}
        for line in p.stdout:
            line = to_str(line.strip())
            if re.match('^HTTP.*? 200 OK$', line):
                break
        for line in p.stdout:
            line = to_str(line.strip()).split(":", 1)
            if len(line) == 2:
                respinfo[line[0].strip().lower()] = line[1].strip()
        return respinfo
    
    def fetch(self, url, filename):
        p = Popen('curl -# -kL "%s" -o "%s"' % (url, filename), shell=True)
        p.wait()
        if p.returncode:
            raise CurlFetchException('Failed to fetch.')

import sys
import urllib
import urllib2
from pythonbrew.util import size_format
from pythonbrew.define import PYTHON_VERSION_URL, PYTHONBREW_UPDATE_URL
from pythonbrew.log import logger

def get_response_from_url(url):
    try:
        resp = urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        logger.error("HTTP error %s while getting %s" % (e.code, url))
        sys.exit(1)
    except IOError, e:
        # Typically an FTP error
        logger.error("Error %s while getting %s" % (e, url))
        sys.exit(1)
    return resp

class Downloader(object):
    def __init__(self):
        self._msg = ""
        self._last_msg = ""
        self._bytes = 0.0
    
    def download(self, msg, url, path):
        self._msg = msg
        self._bytes = 0
        urllib.urlretrieve(url, path, self._download_progress)
        print " downloaded."
    
    def _download_progress(self, block, blockbytes, maxbytes):
        self._bytes += float(blockbytes)
        if self._bytes >= maxbytes:
            self._bytes = maxbytes
        percent = (self._bytes / maxbytes) * 100
        max_size = size_format(maxbytes)
        now_size = size_format(self._bytes)
        now_msg = "\rDownloading %s (%s): %3i%%  %s" % (self._msg, max_size, percent, now_size)
        padding = " " * (len(self._last_msg) - len(now_msg))
        sys.stdout.write("%s%s" % (now_msg, padding))
        sys.stdout.flush()
        self._last_msg = now_msg

def get_pythonbrew_update_url(version):
    if PYTHONBREW_UPDATE_URL.has_key(version):
        return PYTHONBREW_UPDATE_URL[version]
    return None

def get_python_version_url(version):
    if PYTHON_VERSION_URL.has_key(version):
        return PYTHON_VERSION_URL[version]
    return None

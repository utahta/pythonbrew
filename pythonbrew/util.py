import os
import sys
import errno
import shutil
import urllib
import subprocess
import re
from pythonbrew.define import PATH_BIN, PATH_PYTHONS
from pythonbrew.exceptions import BuildingException
from pythonbrew.log import logger

def size_format(b):
    kb = 1000
    mb = kb*kb
    b = float(b)
    if b >= mb:
        return "%.1fMb" % (b/mb)
    if b >= kb:
        return "%.1fKb" % (b/kb)
    return "%.0fbytes" % (b)

def is_url(name):
    if ':' not in name:
        return False
    scheme = name.split(':', 1)[0].lower()
    return scheme in ['http', 'https', 'file', 'ftp']

def splitext(name):
    base, ext = os.path.splitext(name)
    if base.lower().endswith('.tar'):
        ext = base[-4:] + ext
        base = base[:-4]
    return base, ext

def is_archive_file(name):
    ext = splitext(name)[1].lower()
    archives = ('.zip', '.tar.gz', '.tar.bz2', '.tgz', '.tar')
    if ext in archives:
        return True
    return False

def makedirs(path):
    try:
        os.makedirs(path)
    except OSError, (e, es):
        if errno.EEXIST != e:
            raise

def symlink(src, dst):
    try:
        os.symlink(src, dst)
    except:
        pass
    
def unlink(path):
    try:
        os.unlink(path)
    except OSError, (e, es):
        if errno.ENOENT != e:
            raise
        
def rm_r(path):
    """like rm -r command."""
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        unlink(path)

def off():
    for root, dirs, files in os.walk(PATH_BIN):
        for f in files:
            if f == "pythonbrew" or f == "pybrew":
                continue
            unlink("%s/%s" % (root, f))
    unlink("%s/current" % PATH_PYTHONS)
    
class Subprocess(object):
    def __init__(self, log=None, shell=False, cwd=None, print_cmd=True):
        self._log = log
        self._shell = shell
        self._cwd = cwd
        self._print_cmd = print_cmd
    
    def chdir(self, cwd):
        self._cwd = cwd
    
    def check_call(self, cmd, shell=None, cwd=None):
        if shell:
            self._shell = shell
        if cwd:
            self._cwd = cwd
        if self._print_cmd:
            logger.info(cmd)
        if self._log:
            cmd = "(%s) >> '%s' 2>&1" % (cmd, self._log)
        retcode = subprocess.call(cmd, shell=self._shell, cwd=self._cwd)
        if retcode != 0:
            raise BuildingException()

class Package(object):
    def __init__(self, name):
        self.name = None
        self.version = None
        m = re.search("^Python-(.*)$", name)
        if m:
            self.name = name
            self.version = m.group(1)
        else:
            self.name = "Python-%s" % name
            self.version = name
        
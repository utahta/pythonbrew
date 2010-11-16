import os
import errno
import shutil
import subprocess
import re
import posixpath
from pythonbrew.define import PATH_BIN, PATH_PYTHONS
from pythonbrew.exceptions import BuildingException
from pythonbrew.log import logger
import tarfile
import platform

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

def is_html(content_type):
    if content_type and content_type.startswith('text/html'):
        return True
    return False

def is_gzip(content_type, filename):
    if (content_type == 'application/x-gzip'
          or tarfile.is_tarfile(filename)
          or splitext(filename)[1].lower() in ('.tar', '.tar.gz', '.tar.bz2', '.tgz', '.tbz')):
        return True
    return False

def is_macosx_snowleopard():
    mac_ver = platform.mac_ver()[0]
    return mac_ver >= '10.6' and mac_ver < '10.7'

def is_python24(version):
    return version >= '2.4' and version < '2.5'

def is_python25(version):
    return version >= '2.5' and version < '2.6'

def is_python26(version):
    return version >= '2.6' and version < '2.7'

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
    elif os.path.isfile(path):
        unlink(path)

def off():
    for root, dirs, files in os.walk(PATH_BIN):
        for f in files:
            if f == "pythonbrew" or f == "pybrew":
                continue
            unlink("%s/%s" % (root, f))
    unlink("%s/current" % PATH_PYTHONS)

def split_leading_dir(path):
    path = str(path)
    path = path.lstrip('/').lstrip('\\')
    if '/' in path and (('\\' in path and path.find('/') < path.find('\\'))
                        or '\\' not in path):
        return path.split('/', 1)
    elif '\\' in path:
        return path.split('\\', 1)
    else:
        return path, ''

def has_leading_dir(paths):
    """Returns true if all the paths have the same leading path name
    (i.e., everything is in one subdirectory in an archive)"""
    common_prefix = None
    for path in paths:
        prefix, rest = split_leading_dir(path)
        if not prefix:
            return False
        elif common_prefix is None:
            common_prefix = prefix
        elif prefix != common_prefix:
            return False
    return True

def untar_file(filename, location):
    if not os.path.exists(location):
        makedirs(location)
    if filename.lower().endswith('.gz') or filename.lower().endswith('.tgz'):
        mode = 'r:gz'
    elif filename.lower().endswith('.bz2') or filename.lower().endswith('.tbz'):
        mode = 'r:bz2'
    elif filename.lower().endswith('.tar'):
        mode = 'r'
    else:
        logger.error('Cannot determine compression type for file %s' % filename)
        mode = 'r:*'
    tar = tarfile.open(filename, mode)
    try:
        # note: python<=2.5 doesnt seem to know about pax headers, filter them
        leading = has_leading_dir([
            member.name for member in tar.getmembers()
            if member.name != 'pax_global_header'
        ])
        for member in tar.getmembers():
            fn = member.name
            if fn == 'pax_global_header':
                continue
            if leading:
                fn = split_leading_dir(fn)[1]
            path = os.path.join(location, fn)
            if member.isdir():
                if not os.path.exists(path):
                    os.makedirs(path)
            else:
                try:
                    fp = tar.extractfile(member)
                except (KeyError, AttributeError), e:
                    # Some corrupt tar files seem to produce this
                    # (specifically bad symlinks)
                    logger.error('In the tar file %s the member %s is invalid: %s'
                                  % (filename, member.name, e))
                    continue
                if not os.path.exists(os.path.dirname(path)):
                    os.makedirs(os.path.dirname(path))
                destfp = open(path, 'wb')
                try:
                    shutil.copyfileobj(fp, destfp)
                finally:
                    destfp.close()
                os.chmod(path, member.mode)
                fp.close()
    finally:
        tar.close()

def unpack_downloadfile(content_type, download_file, target_dir):
    logger.info("Extracting %s" % os.path.basename(download_file))
    if is_gzip(content_type, download_file):
        untar_file(download_file, target_dir)
    else:
        logger.error("Cannot determine archive format of %s" % download_file)
        return False
    return True
        
class Subprocess(object):
    def __init__(self, log=None, shell=True, cwd=None, print_cmd=False):
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

class Link(object):
    def __init__(self, url):
        self._url = url
    
    @property
    def filename(self):
        url = self._url
        url = url.split('#', 1)[0]
        url = url.split('?', 1)[0]
        url = url.rstrip('/')
        name = posixpath.basename(url)
        assert name, ('URL %r produced no filename' % url)
        return name
    
    @property
    def show_msg(self):
        return posixpath.basename(self._url.split('#', 1)[0].split('?', 1)[0])

        
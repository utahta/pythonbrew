import os
import sys
import errno
import shutil
import re
import posixpath
import tarfile
import platform
import urllib
import subprocess
import shlex
import select
from pythonbrew.define import PATH_BIN, PATH_ETC_CURRENT, PATH_PYTHONS
from pythonbrew.exceptions import ShellCommandException
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

def is_file(name):
    if ':' not in name:
        return False
    scheme = name.split(':', 1)[0].lower()
    return scheme == 'file'

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
    if(content_type == 'application/x-gzip'
       or tarfile.is_tarfile(filename)
       or splitext(filename)[1].lower() in ('.tar', '.tar.gz', '.tgz')):
        return True
    return False

def is_macosx():
    mac_ver = platform.mac_ver()[0]
    return mac_ver >= '10.6'

def get_macosx_deployment_target():
    m = re.search('^([0-9]+\.[0-9]+)', platform.mac_ver()[0])
    if m:
        return m.group(1)
    return None

def is_python24(version):
    return version >= '2.4' and version < '2.5'

def is_python25(version):
    return version >= '2.5' and version < '2.6'

def is_python26(version):
    return version >= '2.6' and version < '2.7'

def is_python27(version):
    return version >= '2.7' and version < '2.8'

def is_python30(version):
    return version >= '3.0' and version < '3.1'

def is_python31(version):
    return version >= '3.1' and version < '3.2'

def is_python32(version):
    return version >= '3.2' and version < '3.3'

def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

def symlink(src, dst):
    try:
        os.symlink(src, dst)
    except:
        pass
    
def unlink(path):
    try:
        os.unlink(path)
    except OSError:
        e = sys.exc_info()[1]
        if errno.ENOENT != e.errno:
            raise
        
def rm_r(path):
    """like rm -r command."""
    if os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.isfile(path):
        unlink(path)

def off():
    set_current_path(PATH_BIN)

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
        os.makedirs(location)
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
                except (KeyError, AttributeError):
                    e = sys.exc_info()[1]
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
                fp.close()
                # note: configure ...etc
                os.chmod(path, member.mode)
                # note: the file timestamps should be such that asdl_c.py is not invoked.
                os.utime(path, (member.mtime, member.mtime))
    finally:
        tar.close()

def extract_downloadfile(content_type, download_file, target_dir):
    logger.info("Extracting %s into %s" % (os.path.basename(download_file), target_dir))
    if is_gzip(content_type, download_file):
        untar_file(download_file, target_dir)
    else:
        logger.error("Cannot determine archive format of %s" % download_file)
        return False
    return True

def get_using_python_path():
    p = subprocess.Popen('command -v python', stdout=subprocess.PIPE, shell=True)
    return to_str(p.communicate()[0].strip())

def get_using_python_pkgname():
    """return: Python-<VERSION> or None"""
    path = get_using_python_path()
    for d in sorted(os.listdir(PATH_PYTHONS)):
        if path and os.path.samefile(path, os.path.join(PATH_PYTHONS, d, 'bin','python')):
            return d
    return None

def get_installed_pythons_pkgname():
    """Get the installed python versions list."""
    return [d for d in sorted(os.listdir(PATH_PYTHONS))]

def is_installed(name):
    pkgname = Package(name).name
    pkgdir = os.path.join(PATH_PYTHONS, pkgname)
    if not os.path.isdir(pkgdir):
        return False
    return True
    
def set_current_path(path):
    fp = open(PATH_ETC_CURRENT, 'w')
    fp.write('PATH_PYTHONBREW="%s"\n' % (path))
    fp.close()

def path_to_fileurl(path):
    path = os.path.normcase(os.path.abspath(path))
    url = urllib.quote(path)
    url = url.replace(os.path.sep, '/')
    url = url.lstrip('/')
    return 'file:///' + url

def fileurl_to_path(url):
    assert url.startswith('file:'), ('Illegal scheme:%s' % url)
    url = '/' + url[len('file:'):].lstrip('/')
    return urllib.unquote(url)

def to_str(val):
    try:
        # python3
        if type(val) is bytes:
            return val.decode()
    except:
        if type(val) is unicode:
            return val.encode("utf-8")
    return val

def is_str(val):
    try:
        # python2
        return isinstance(val, basestring)
    except:
        # python3
        return isinstance(val, str)
    return False

def bltin_any(iter):
    try:
        return any(iter)
    except:
        # python2.4
        for it in iter:
            if it:
                return True
        return False

class Subprocess(object):
    def __init__(self, log=None, cwd=None, verbose=False, debug=False):
        self._log = log
        self._cwd = cwd
        self._verbose = verbose
        self._debug = debug
    
    def chdir(self, cwd):
        self._cwd = cwd
    
    def shell(self, cmd):
        if self._debug:
            logger.info(cmd)
        if self._log:
            if self._verbose:
                cmd = "(%s) 2>&1 | tee '%s'" % (cmd, self._log)
            else:
                cmd = "(%s) >> '%s' 2>&1" % (cmd, self._log)
        returncode = subprocess.call(cmd, shell=True, cwd=self._cwd)
        if returncode:
            raise ShellCommandException('%s: failed to `%s`' % (returncode, cmd))
    
    def call(self, cmd):
        if is_str(cmd):
            cmd = shlex.split(cmd)
        if self._debug:
            logger.info(cmd)
        
        fp = ((self._log and open(self._log, 'a')) or None)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=self._cwd)
        while p.returncode is None:
            while bltin_any(select.select([p.stdout], [], [])):
                line = to_str(p.stdout.readline())
                if not line:
                    break
                if self._verbose:
                    logger.info(line.strip())
                if fp:
                    fp.write(line)
                    fp.flush()
            p.poll()
        if fp:
            fp.close()
        return p.returncode
    
    def check_call(self, cmd):
        returncode = self.call(cmd)
        if returncode:
            raise ShellCommandException('%s: failed to `%s`' % (returncode, cmd))

class Package(object):
    def __init__(self, name, alias=None):
        self.name = None
        self.version = None
        self.alias = None
        if is_archive_file(name):
            name = splitext(name)[0]
        m = re.search("^Python-(.*)$", name)
        if m:
            self.name = name
            self.version = self.alias = m.group(1)
        else:
            self.name = "Python-%s" % name
            self.version = self.alias = name
        if alias:
            self.name = 'Python-%s' % alias
            self.alias = alias

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
    def base_url(self):
        return posixpath.basename(self._url.split('#', 1)[0].split('?', 1)[0])

        

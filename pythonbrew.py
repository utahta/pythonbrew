#!/usr/bin/env python
# vim:fileencoding=utf-8

import os
import sys
import urllib
import errno
import re
import shutil
import filecmp
import subprocess
import tempfile
from HTMLParser import HTMLParser
from optparse import OptionParser

VERSION = "0.4"
if os.environ.has_key("PYTHONBREW_ROOT"):
    ROOT = os.environ["PYTHONBREW_ROOT"]
else:
    ROOT = "%s/python/pythonbrew" % os.environ["HOME"]
PYTHONDLSITE = "http://www.python.org/ftp/python/%s/%s"
DISTRIBUTE_SETUP_DLSITE = "http://python-distribute.org/distribute_setup.py"
EZSETUP_DLSITE = "http://peak.telecommunity.com/dist/ez_setup.py"

PATH_PYTHONS = "%s/pythons" % ROOT
PATH_BUILD = "%s/build" % ROOT
PATH_DISTS = "%s/dists" % ROOT
PATH_ETC = "%s/etc" % ROOT
PATH_BIN = "%s/bin" % ROOT

parser = OptionParser(usage="%prog COMMAND [OPTIONS]",
                      version=VERSION,
                      add_help_option=False)
parser.add_option(
    '-h', '--help',
    dest='help',
    action='store_true',
    help='Show help')
parser.disable_interspersed_args()

command_dict = {}
def add_command(command):
    command_dict[command.name] = command

#----------------------------------------------------
# exception
#----------------------------------------------------
class BuildingException(Exception):
    """General exception during building"""

#----------------------------------------------------
# util
#----------------------------------------------------
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

def makedirs(name):
    try:
        os.makedirs(name)
    except OSError, (e, es):
        if errno.EEXIST != e:
            raise

def symlink(src, dst):
    try:
        os.symlink(src, dst)
    except:
        pass
    
def unlink(name):
    try:
        os.unlink(name)
    except OSError, (e, es):
        if errno.ENOENT != e:
            raise

def clean_switch_symlink():
    for root, dirs, files in os.walk("%s/bin/" % ROOT):
        for f in files:
            if f == "pythonbrew":
                continue
            unlink("%s%s" % (root, f))

#----------------------------------------------------
# classes
#----------------------------------------------------
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
            print cmd
        if self._log:
            cmd = "(%s) >> '%s' 2>&1" % (cmd, self._log)
        retcode = subprocess.call(cmd, shell=self._shell, cwd=self._cwd)
        if retcode != 0:
            raise BuildingException()

class PythonVersionParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self._versions = []
        self._re = re.compile("^(\d+\.\d+(\..*)?)/$")
    
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            attrs = dict(attrs)
            if "href" in attrs:
                m = self._re.search(attrs["href"])
                if m:
                    self._versions.append(m.group(1))
    
    def get_sorted_versions(self):
        return sorted(self._versions)

class PythonPackages(object):
    def __init__(self):
        parser = PythonVersionParser()
        fp = urllib.urlopen("http://www.python.org/ftp/python/")
        parser.feed(fp.read())
        fp.close()
        parser.close()
        self._versions = parser.get_sorted_versions()
        
    def has_version(self, version):
        return version in self._versions
    
    def get_packages(self):
        return ["Python-%s" % v for v in self._versions]

#----------------------------------------------------
# commands
#----------------------------------------------------
class Command(object):
    name = None
    usage = None
    summary = ""
    
    def __init__(self):
        self.parser = OptionParser(usage=self.usage,
                                   prog='%s %s' % (os.path.basename(sys.argv[0]), self.name))
        
    def run(self, args):
        options, args = self.parser.parse_args(args)
        self.run_command(options, args[1:])

class HelpCommand(Command):
    name = "help"
    usage = "%prog [COMMAND]"
    summary = "Show available commands"
    
    def run_command(self, options, args):
        if args:
            command = args[0]
            if command not in command_dict:
                parser.error("Unknown command: `%s`" % command)
                return
            command = command_dict[command]
            command.parser.print_help()
            return
        parser.print_help()
        print
        print "Commands available:"
        commands = [command_dict[key] for key in sorted(command_dict.keys())]
        for command in commands:
            print "  %s: %s" % (command.name, command.summary)
        print
        print "Further Instructions:"
        print "  http://github.com/utahta/pythonbrew"

class InitCommand(Command):
    name = "init"
    usage = "%prog"
    summary = "Run this once to setup the pythonbrew directory ready for installing pythons into"
        
    def run_command(self, options, args):
        makedirs(PATH_PYTHONS)
        makedirs(PATH_BUILD)
        makedirs(PATH_DISTS)
        makedirs(PATH_ETC)
        
        os.system("echo 'export PATH=%s/bin:%s/current/bin:${PATH}' > %s/bashrc" % (ROOT, PATH_PYTHONS, PATH_ETC))
        os.system("echo 'setenv PATH %s/bin:%s/current/bin:$PATH' > %s/cshrc" % (ROOT, PATH_PYTHONS, PATH_ETC))
        m = re.search("(t?csh)", os.environ.get("SHELL"))
        if m:
            shrc = "cshrc"
            yourshrc = m.group(1)+"rc"
        else:
            shrc = yourshrc = "bashrc"
        print """
Pythonbrew environment initiated, required directories are created under

    """+ROOT+"""
    
Well-done! Congratulations! Please add the following line to the end
of your ~/."""+yourshrc+"""

    source """+PATH_ETC+"""/"""+shrc+"""

After that, exit this shell, start a new one, and install some fresh
pythons:

    pythonbrew install Python-2.6.6
    pythonbrew install Python-2.5.5

For further instructions, simply run:

    pythonbrew

The default help messages will popup and tell you what to do!

Enjoy pythonbrew at $HOME!!
INSTRUCTION"""

class InstallCommand(Command):
    name = "install"
    usage = "%prog [OPTIONS] PACKAGE_NAMES"
    summary = "Build and install the given version of python"
    
    def __init__(self):
        super(InstallCommand, self).__init__()
        self.parser.add_option(
            "-f", "--force",
            dest="force",
            action="store_true",
            default=False,
            help="Force installation of a Python."
        )
        self.parser.add_option(
            "-b", "--build-options",
            dest="build_options",
            default="",
            help="Set configure options."
        )
        self.parser.add_option(
            "-n", "--no-setuptools",
            dest="no_setuptools",
            action="store_true",
            default=False,
            help="Skip installation of setuptools."
        )
        self._logfile = "%s/build.log" % ROOT
    
    def run_command(self, options, args):
        if args:
            # Install Python
            self._install_python(args[0], options)
        else:
            # Install pythonbrew
            self._install_myself()

    def _install_myself(self):
        executable = os.path.abspath(sys.argv[0])
        (fd, src) = tempfile.mkstemp()
        fp = file(executable, "r")
        line = fp.readline()
        if line.startswith("#!"):
            os.write(fd, "#!%s\n" % os.path.realpath(sys.executable))
        else:
            os.write(fd, line)
        os.write(fd, fp.read())
        os.close(fd)
        fp.close()
        
        dist = "%s/pythonbrew" % PATH_BIN
        if os.path.isfile(src) and os.path.isfile(dist):
            if filecmp.cmp(src, dist):
                os.remove(src)
                print """You are already running the installed pythonbrew:
        
    """ + dist
                sys.exit()        
        makedirs(PATH_BIN)
        shutil.copy(src, dist)
        os.chmod(dist, 0755)
        os.remove(src)
        print """The pythonbrew is installed as:
    
    """+dist+"""

You may trash the downloaded """+executable+""" from now on.

Next, if this is the first time you've run pythonbrew installation, run:

    """+dist+""" init

And follow the instruction on screen."""

    def _get_package(self, name):
        if not os.path.isfile(name) and not os.path.isdir(name):
            if is_url(name):
                basename = os.path.basename(name)
                download_url = name
                download_path = "%s/%s" % (PATH_DISTS, basename)
            else:
                m = re.search("^Python-(\d+\.\d+(\..*)?)$", name)
                if not m:
                    print "Unknown package: `%s`" % name
                    sys.exit(1)
                dist_version = m.group(1)
                pkgs = PythonPackages()
                if not pkgs.has_version(dist_version):
                    print "Package not found: `%s`" % name
                    sys.exit(1)
                basename = "%s.tgz" % name
                download_url = PYTHONDLSITE % (dist_version, basename)
                download_path = "%s/%s" % (PATH_DISTS, basename)
            
            if os.path.isfile(download_path):
                print "Use the previously fetched %s" % (download_path)
            else:
                try:
                    dl = Downloader()
                    dl.download(
                        basename,
                        download_url,
                        download_path
                    )
                except:
                    os.remove(download_path)
                    print "\nInterrupt to abort. `%s`" % (download_url)
                    sys.exit(1)
                # iffy
                if os.path.getsize(download_path) < 1000000:
                    print "Invalid file downloaded. (maybe 404 not found?) `%s`" % (download_url)
                    os.remove(download_path)
                    sys.exit(1)
        else:
            if os.path.isfile(name):
                basename = os.path.basename(name)
                print "Copy the file %s to %s/%s" % (name, PATH_DISTS, basename)
                shutil.copy(name, "%s/%s" % (PATH_DISTS, basename))
            elif os.path.isdir(name):
                basename = name
                print "Copy the directory %s to %s/%s" % (name, PATH_DISTS, basename)
                shutil.copytree(name, "%s/%s" % (PATH_DISTS, basename))
            else:
                print "Unknown object. `%s`" % name
                sys.exit(1)
        return basename
    
    def _get_uncompress_command(self, basename):
        distpath = "%s/%s" % (PATH_DISTS, basename)
        if os.path.isfile(distpath):
            ext = splitext(basename)[1]
            if ext == ".tar.gz" or ext == ".tgz":
                return "tar zxf %s" % (distpath)
            elif ext == ".tar.bz2":
                return "tar jxf %s" % (distpath)
            elif ext == ".tar":
                return "tar xf %s" % (distpath)
            elif ext == ".zip":
                return "unzip %s" % (distpath)
        elif os.path.isdir(distpath):
            return "mv %s %s/%s" % (distpath, PATH_BUILD, basename)
        else:
            print "Unknown object. `%s`" % (basename)
        return ""
    
    def _install_python(self, dist, options):
        basename = self._get_package(dist)
        pkgname = splitext(basename)[0]
        
        install_dir = "%s/%s" % (PATH_PYTHONS, pkgname)
        build_options = "--prefix=%s %s" % (install_dir, options.build_options)
        print "Installing %s into %s" % (pkgname, install_dir);
        print """This could take a while. You can run the following command on another shell to track the status:

  tail -f %s
""" % (self._logfile)
        try:
            s = Subprocess(log=self._logfile, shell=True, cwd=PATH_BUILD)
            s.check_call(self._get_uncompress_command(basename))
            
            s.chdir("%s/%s" % (PATH_BUILD, pkgname))
            s.check_call("./configure %s" % (build_options))
            if options.force:
                s.check_call("make")
                s.check_call("make install")
            else:
                s.check_call("make")
                s.check_call("make test")
                s.check_call("make install")
        except:
            print """Installing %(pkgname)s failed. See %(ROOT)s/build.log to see why.
    
    pythonbrew install --force %(pkgname)s""" % {"pkgname":pkgname, "ROOT":ROOT}
            sys.exit(1)

        # install setuptools
        self._install_setuptools(pkgname, options.no_setuptools)
        print """Installed """+pkgname+""" successfully. Run the following command to switch to it.

    pythonbrew switch """+pkgname
    
    def _install_setuptools(self, pkgname, no_setuptools):
        if no_setuptools:
            print "Skip installation setuptools."
            return
        if re.match("^Python-3.*", pkgname):
            download_url = DISTRIBUTE_SETUP_DLSITE
            is_python3 = True
        else:
            download_url = EZSETUP_DLSITE
            is_python3 = False
        basename = os.path.basename(download_url)
        
        dl = Downloader()
        dl.download(basename, download_url, "%s/%s" % (PATH_DISTS, basename))
        
        if is_python3:
            if os.path.isfile("%s/%s/bin/python3" % (PATH_PYTHONS, pkgname)):
                pyexec = "%s/%s/bin/python3" % (PATH_PYTHONS, pkgname)
            elif os.path.isfile("%s/%s/bin/python3.0" % (PATH_PYTHONS, pkgname)):
                pyexec = "%s/%s/bin/python3.0" % (PATH_PYTHONS, pkgname)
            else:
                print "Python3 binary not found. `%s/%s`" % (PATH_PYTHONS, pkgname)
                return
        else:
            pyexec = "%s/%s/bin/python" % (PATH_PYTHONS, pkgname)
        os.system("%s %s/%s" % (pyexec, PATH_DISTS, basename))
        
        if os.path.isfile("%s/%s/bin/easy_install" % (PATH_PYTHONS, pkgname)) and not is_python3:
            os.system("%s/%s/bin/easy_install pip" % (PATH_PYTHONS, pkgname))

class InstalledCommand(Command):
    name = "installed"
    usage = "%prog"
    summary = "List the installed versions of python"
        
    def run_command(self, options, args):
        if os.path.islink("%s/current" % PATH_PYTHONS):
            if os.path.realpath("%s/current" % PATH_PYTHONS) == ROOT:
                cur = os.path.realpath("%s/bin/python" % ROOT)
            else:
                cur = os.path.basename(os.path.realpath("%s/current" % PATH_PYTHONS))
            print "%s (*)" % cur
        else:
            cur = ""
        for d in os.listdir("%s/" % PATH_PYTHONS):
            if d == "current" or cur == "%s" % (d):
                continue
            print "%s" % (d)

class SwitchCommand(Command):
    name = "switch"
    usage = "%prog PACKAGE"
    summary = "Switch to the given version"
    
    def run_command(self, options, args):
        if args:
            dist = args[0]
        distdir = dist
        if os.path.isfile( dist ) and os.access( dist, os.X_OK ):
            if re.search( ".*python(\d(\.\d)?)?$", dist ):
                self._switch_file(dist)
            else:
                print "Invalid binary: `%s`" % dist
            return
        elif os.path.isdir( dist ):
            if os.path.isdir("%s/bin" % dist):
                if os.path.isfile("%s/bin/python" % dist):
                    self._switch_file("%s/bin/python" % dist)
                if os.path.isfile("%s/bin/python3" % dist):
                    self._switch_file("%s/bin/python3" % dist)
                return
            elif os.path.isfile("%s/python" % dist) and os.access("%s/python" % dist, os.X_OK):
                self._switch_file("%s/python" % dist)
                return
            elif os.path.isfile("%s/python3" % dist) and os.access("%s/python3" % dist, os.X_OK):
                self._switch_file("%s/python3" % dist)
                return
            else:
                print "Invalid directory: `%s`" % dist
                return
        elif not os.path.isdir( "%s/%s" % (PATH_PYTHONS, dist) ):
            print "Unknown package: `%s`" % dist
            return
        self._switch_dir( distdir )
    
    def _switch_file(self, dist):
        unlink("%s/current" % PATH_PYTHONS)
        unlink("%s/bin/python" % ROOT)
        clean_switch_symlink()
        symlink(dist, "%s/bin/python" % ROOT)
        symlink(ROOT, "%s/current" % PATH_PYTHONS)
        print "Switched to "+dist
    
    def _switch_dir(self, dist):
        unlink("%s/current" % PATH_PYTHONS)
        unlink("%s/bin/python" % ROOT)
        symlink(dist, "%s/current" % PATH_PYTHONS)
        clean_switch_symlink()
        for root, dirs, files in os.walk("%s/current/bin/" % PATH_PYTHONS):
            for f in files:
                symlink("%s%s" % (root, f), "%s/%s" % (PATH_BIN, f))
        # I want better code
        if not os.path.isfile("%s/python" % PATH_BIN):
            if os.path.isfile("%s/python3" % PATH_BIN):
                symlink(os.path.realpath("%s/python3" % PATH_BIN), "%s/python" % PATH_BIN)
            elif os.path.isfile("%s/python3.0" % PATH_BIN):
                symlink(os.path.realpath("%s/python3.0" % PATH_BIN), "%s/python" % PATH_BIN)
        print "Switched to "+dist
        
class OffCommand(Command):
    name = "off"
    usage = "%prog"
    summary = "Disable pythonbrew"
    
    def run_command(self, options, args):
        unlink("%s/current" % PATH_PYTHONS)
        clean_switch_symlink()

class VersionCommand(Command):
    name = "version"
    usage = "%prog"
    summary = "Show version"
    
    def run_command(self, options, args):
        print VERSION

class SearchCommand(Command):
    name = "search"
    usage = "%prog [Python-<VERSION>]"
    summary = "Search Python packages"
    
    def run_command(self, options, args):
        pkgs = PythonPackages()
        if args:
            pattern = args[0]
            _re = re.compile(r"%s" % pattern)
            pkgnames = []
            for pkgname in pkgs.get_packages():
                if _re.match(pkgname):
                    pkgnames.append(pkgname)
            if pkgnames:
                for pkgname in pkgnames:
                    print pkgname
            else:
                print "Package not found. `%s`" % pattern
        else:
            for pkgname in pkgs.get_packages():
                print pkgname

class Pythonbrew(object):
    def run(self):
        options, args = parser.parse_args(sys.argv[1:])
        if options.help and not args:
            args = ["help"]
        if not args:
            parser.error('You must give a command (use "pythonbrew help" to see a list of commands)')
            return
        add_command(HelpCommand())
        add_command(InitCommand())
        add_command(InstallCommand())
        add_command(InstalledCommand())
        add_command(SwitchCommand())
        add_command(OffCommand())
        add_command(VersionCommand())
        add_command(SearchCommand())
        
        command = args[0].lower()
        if command not in command_dict:
            parser.error("Unknown command: `%s`" % command)
            return
        command = command_dict[command]
        command.run(args)
            
def main():
    p = Pythonbrew()
    p.run()
    
if __name__ == "__main__":
    main()

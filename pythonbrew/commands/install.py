import os
import sys
import re
import shutil
from pythonbrew.basecommand import Command
from pythonbrew.util import unlink, splitext, Subprocess, Package, makedirs,\
    rm_r
from pythonbrew.define import ROOT, PATH_PYTHONS, PATH_DISTS, PATH_BUILD, PATH_LOG, DISTRIBUTE_SETUP_DLSITE
from pythonbrew.log import logger
from pythonbrew.downloader import get_python_package_url, Downloader

class InstallCommand(Command):
    name = "install"
    usage = "%prog [OPTIONS] VERSION"
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
            "-C", "--configure",
            dest="configure",
            default="",
            metavar="CONFIGURE_OPTIONS",
            help="Custom configure options."
        )
        self.parser.add_option(
            "-n", "--no-setuptools",
            dest="no_setuptools",
            action="store_true",
            default=False,
            help="Skip installation of setuptools."
        )
        self._logfile = "%s/build.log" % PATH_LOG
    
    def run_command(self, options, args):
        if args:
            # Install Python
            self._install_python(args[0], options)
        else:
            logger.error("Package not found.")
    
    def _install_python(self, dist, options):
        pkg = Package(dist)
        distname = self._download_package(pkg)
        pkgname = pkg.name
        version = pkg.version
        
        install_dir = "%s/%s" % (PATH_PYTHONS, pkgname)
        configure = "--prefix=%s %s" % (install_dir, options.configure)
        logger.info("")
        logger.info("This could take a while. You can run the following command on another shell to track the status:")
        logger.info("  tail -f %s" % self._logfile)
        logger.info("")
        
        try:
            s = Subprocess(log=self._logfile, shell=True, cwd=PATH_BUILD, print_cmd=False)

            logger.info("Extracting %s" % distname)
            s.check_call(self._get_uncompress_command(distname))
            
            logger.info("Installing %s into %s" % (pkgname, install_dir))
            s.chdir("%s/%s" % (PATH_BUILD, pkgname))
            s.check_call("./configure %s" % (configure))
            if options.force:
                s.check_call("make")
            else:
                s.check_call("make")
                s.check_call("make test")
            if version == "1.5.2" or version == "1.6.1":
                makedirs(install_dir)
            s.check_call("make install")
        except:
            rm_r(install_dir)
            logger.error("""Failed to install %(pkgname)s. See %(ROOT)s/build.log to see why.
  
  pythonbrew install --force %(version)s""" % {"pkgname":pkgname, "ROOT":ROOT, "version":version})
            sys.exit(1)
        
        # install setuptools
        self._install_setuptools(pkgname, options.no_setuptools)
        logger.info("""
Installed %(pkgname)s successfully. Run the following command to switch to %(pkgname)s.

  pythonbrew switch %(version)s""" % {"pkgname":pkgname, "version":version})
    
    def _download_package(self, pkg):
        pkgname = pkg.name
        version = pkg.version
        
        if os.path.isdir("%s/%s" % (PATH_PYTHONS, pkgname)):
            logger.error("You are already installed `%s`." % pkgname)
            sys.exit(1)
        
        download_url = get_python_package_url(version)
        if not download_url:
            logger.error("Unknown package: `%s`" % pkgname)
            sys.exit(1)
        distname = os.path.basename(download_url)
        download_path = "%s/%s" % (PATH_DISTS, distname)
        
        if os.path.isfile(download_path):
            logger.info("Use the previously fetched %s" % (download_path))
        else:
            try:
                dl = Downloader()
                dl.download(
                    distname,
                    download_url,
                    download_path
                )
            except:
                unlink(download_path)
                logger.info("\nInterrupt to abort. `%s`" % (download_url))
                sys.exit(1)
            # iffy
            if os.path.getsize(download_path) < 1000000:
                logger.error("Failed to download. `%s`" % (download_url))
                unlink(download_path)
                sys.exit(1)
        return distname
    
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
            logger.error("File not found. `%s`" % (basename))
        return ""
    
    def _install_setuptools(self, pkgname, no_setuptools):
        if no_setuptools:
            logger.info("Skip installation setuptools.")
            return
        if re.match("^Python-3.*", pkgname):
            is_python3 = True
        else:
            is_python3 = False
        download_url = DISTRIBUTE_SETUP_DLSITE
        basename = os.path.basename(download_url)
        
        dl = Downloader()
        dl.download(basename, download_url, "%s/%s" % (PATH_DISTS, basename))
        
        install_dir = "%s/%s" % (PATH_PYTHONS, pkgname)
        if is_python3:
            if os.path.isfile("%s/bin/python3" % (install_dir)):
                pyexec = "%s/bin/python3" % (install_dir)
            elif os.path.isfile("%s/bin/python3.0" % (install_dir)):
                pyexec = "%s/bin/python3.0" % (install_dir)
            else:
                logger.error("Python3 binary not found. `%s`" % (install_dir))
                return
        else:
            pyexec = "%s/bin/python" % (install_dir)
        
        try:
            s = Subprocess(log=self._logfile, shell=True, cwd=PATH_DISTS, print_cmd=False)
            logger.info("Installing distribute into %s" % install_dir)
            s.check_call("%s %s" % (pyexec, basename))
            if os.path.isfile("%s/bin/easy_install" % (install_dir)) and not is_python3:
                logger.info("Installing pip into %s" % install_dir)
                s.check_call("%s/bin/easy_install pip" % (install_dir), cwd=None)
        except:
            logger.error("Failed to install setuptools. See %s/build.log to see why." % (ROOT))
            logger.info("Skip install setuptools.")

InstallCommand()

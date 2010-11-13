import os
import sys
import glob
import shutil
import re
from pythonbrew.util import makedirs, symlink, Package, is_url, splitext, Link,\
    unlink, is_gzip, is_html, untar_file, Subprocess, rm_r,\
    is_macosx_snowleopard, is_python25, is_python24, is_python26
from pythonbrew.define import PATH_BUILD, PATH_BIN, PATH_DISTS, PATH_PYTHONS,\
    PATH_ETC, PATH_SCRIPTS, PATH_SCRIPTS_PYTHONBREW,\
    PATH_SCRIPTS_PYTHONBREW_COMMANDS, INSTALLER_ROOT, PATH_BIN_PYTHONBREW,\
    PATH_BIN_PYBREW, ROOT, PATH_LOG, DISTRIBUTE_SETUP_DLSITE, PATH_PATCHES,\
    PATH_PATCHES_MACOSX_PYTHON25, PATH_PATCHES_MACOSX_PYTHON24
from pythonbrew.downloader import get_python_package_url, Downloader,\
    get_response_from_url
from pythonbrew.log import logger

def install_pythonbrew():
    makedirs(PATH_PYTHONS)
    makedirs(PATH_BUILD)
    makedirs(PATH_DISTS)
    makedirs(PATH_ETC)
    makedirs(PATH_BIN)
    makedirs(PATH_LOG)
    makedirs(PATH_SCRIPTS)
    makedirs(PATH_SCRIPTS_PYTHONBREW)
    makedirs(PATH_SCRIPTS_PYTHONBREW_COMMANDS)

    for path in glob.glob(os.path.join(INSTALLER_ROOT,"*.py")):
        shutil.copy(path, PATH_SCRIPTS_PYTHONBREW)

    for path in glob.glob(os.path.join(INSTALLER_ROOT,"commands","*.py")):
        shutil.copy(path, PATH_SCRIPTS_PYTHONBREW_COMMANDS)
    
    rm_r(PATH_PATCHES)
    shutil.copytree(os.path.join(INSTALLER_ROOT,"patches"), PATH_PATCHES)
    
    fp = open("%s/pythonbrew_main.py" % PATH_SCRIPTS, "w")
    fp.write("""import pythonbrew
if __name__ == "__main__":
    pythonbrew.main()
""")
    fp.close()

    fp = open(PATH_BIN_PYTHONBREW, "w")
    fp.write("""#!/usr/bin/env bash
%s %s/pythonbrew_main.py "$@"
""" % (sys.executable, PATH_SCRIPTS))
    fp.close()
    os.chmod(PATH_BIN_PYTHONBREW, 0755)
    symlink(PATH_BIN_PYTHONBREW, PATH_BIN_PYBREW) # pyb as pythonbrew

    os.system("echo 'export PATH=%s/bin:%s/current/bin:${PATH}' > %s/bashrc" % (ROOT, PATH_PYTHONS, PATH_ETC))
    os.system("echo 'setenv PATH %s/bin:%s/current/bin:$PATH' > %s/cshrc" % (ROOT, PATH_PYTHONS, PATH_ETC))

class PythonInstaller(object):
    def __init__(self, arg, options):
        if is_url(arg):
            self.download_url = arg
            filename = Link(self.download_url).filename
            pkg = Package(splitext(filename)[0])
        else:
            pkg = Package(arg)
            self.download_url = get_python_package_url(pkg.version)
            if not self.download_url:
                logger.error("Unknown package: `%s`" % pkg.name)
                sys.exit(1)
            filename = Link(self.download_url).filename
        self.pkg = pkg
        self.install_dir = "%s/%s" % (PATH_PYTHONS, pkg.name)
        self.build_dir = "%s/%s" % (PATH_BUILD, pkg.name)
        self.download_file = "%s/%s" % (PATH_DISTS, filename)
        resp = get_response_from_url(self.download_url)
        self.content_type = resp.info()['content-type']
        self.options = options
        self.logfile = "%s/build.log" % PATH_LOG
    
    def install(self):
        if os.path.isdir(self.install_dir):
            logger.info("You are already installed `%s`" % self.pkg.name)
            sys.exit()
        self.ensure()
        self.download()
        logger.info("")
        logger.info("This could take a while. You can run the following command on another shell to track the status:")
        logger.info("  tail -f %s" % self.logfile)
        logger.info("")
        self.unpack()
        self.patch()
        logger.info("Installing %s into %s" % (self.pkg.name, self.install_dir))
        try:
            self.configure()
            self.make()
            self.make_install()
        except:
            rm_r(self.install_dir)
            logger.error("Failed to install %s. See %s to see why." % (self.pkg.name, self.logfile))
            logger.info("  pythonbrew install --force %s" % self.pkg.version)
            sys.exit(1)
        self.install_setuptools()
        logger.info("Installed %(pkgname)s successfully. Run the following command to switch to %(pkgname)s."
                    % {"pkgname":self.pkg.name})
        logger.info("")
        logger.info("  pythonbrew switch %s" % self.pkg.version)
    
    def ensure(self):
        if is_macosx_snowleopard():
            version = self.pkg.version
            if version < '2.6' and (version != '2.4.6' and version != '2.5.5'):
                logger.info("`%s` is not supported on MacOSX Snow Leopard" % self.pkg.name)
                sys.exit()
    
    def download(self):
        content_type = self.content_type
        if is_html(content_type):
            logger.error("Invalid content-type: `%s`" % content_type)
            sys.exit(1)
        if os.path.isfile(self.download_file):
            logger.info("Use the previously fetched %s" % (self.download_file))
            return
        msg = Link(self.download_url).show_msg
        try:
            dl = Downloader()
            dl.download(
                msg,
                self.download_url,
                self.download_file
            )
        except:
            unlink(self.download_file)
            logger.info("\nInterrupt to abort. `%s`" % (self.download_url))
            sys.exit(1)

    def unpack(self):
        logger.info("Extracting %s" % os.path.basename(self.download_file))
        if is_gzip(self.content_type, self.download_file):
            untar_file(self.download_file, self.build_dir)
        else:
            logger.error("Cannot determine archive format of %s" % self.download_file)
    
    def patch(self):
        version = self.pkg.version
        try:
            s = Subprocess(log=self.logfile, shell=True, cwd=self.build_dir, print_cmd=False)
            patches = []
            if is_macosx_snowleopard():
                if is_python24(version):
                    patch_dir = os.path.join(PATH_PATCHES_MACOSX_PYTHON24,'files')
                    patches = ['patch-configure', 'patch-Makefile.pre.in',
                               'patch-Lib-cgi.py', 'patch-Lib-site.py',
                               'patch-setup.py', 'patch-Include-pyport.h',
                               'patch-Mac-OSX-Makefile.in', 'patch-Mac-OSX-IDLE-Makefile.in',
                               'patch-Mac-OSX-PythonLauncher-Makefile.in', 'patch-configure-badcflags.diff',
                               'patch-configure-arch_only.diff', 'patch-macosmodule.diff',
                               'patch-mactoolboxglue.diff', 'patch-pymactoolbox.diff']
                elif is_python25(version):
                    patch_dir = os.path.join(PATH_PATCHES_MACOSX_PYTHON25,'files')
                    patches = ['patch-Makefile.pre.in.diff', 'patch-Lib-cgi.py.diff',
                               'patch-Lib-distutils-dist.py.diff', 'patch-setup.py.diff',
                               'patch-configure-badcflags.diff', 'patch-configure-arch_only.diff',
                               'patch-64bit.diff', 'patch-pyconfig.h.in.diff',
                               'patch-Modules-posixmodule.c.diff']
            if patches:
                logger.info("Patching %s" % self.pkg.name)
                for patch in patches:
                    s.check_call("patch -p0 < %s" % os.path.join(patch_dir, patch))
        except:
            logger.error("Failed to patch `%s`" % self.build_dir)
            sys.exit(1)
    
    def configure(self):
        configure_option = ""
        if is_macosx_snowleopard():
            version = self.pkg.version
            if is_python24(version):
                configure_option = '--with-universal-archs="intel" MACOSX_DEPLOYMENT_TARGET=10.6 CPPFLAGS="-D__DARWIN_UNIX03"'
            elif is_python25(version):
                configure_option = '--with-universal-archs="intel" MACOSX_DEPLOYMENT_TARGET=10.6 CPPFLAGS="-D_DARWIN_C_SOURCE"'
            elif is_python26(version):
                configure_option = '--with-universal-archs="intel" MACOSX_DEPLOYMENT_TARGET=10.6'
        
        s = Subprocess(log=self.logfile, shell=True, cwd=self.build_dir, print_cmd=False)
        s.check_call("./configure --prefix=%s %s %s" % (self.install_dir, self.options.configure, configure_option))
        
    def make(self):
        s = Subprocess(log=self.logfile, shell=True, cwd=self.build_dir, print_cmd=False)
        if self.options.force:
            s.check_call("make")
        else:
            s.check_call("make")
            s.check_call("make test")
            
    def make_install(self):
        version = self.pkg.version
        if version == "1.5.2" or version == "1.6.1":
            makedirs(self.install_dir)
        s = Subprocess(log=self.logfile, shell=True, cwd=self.build_dir, print_cmd=False)
        s.check_call("make install")
            
    def install_setuptools(self):
        options = self.options
        pkgname = self.pkg.name
        if options.no_setuptools:
            logger.info("Skip installation setuptools.")
            return
        if re.match("^Python-3.*", pkgname):
            is_python3 = True
        else:
            is_python3 = False
        download_url = DISTRIBUTE_SETUP_DLSITE
        filename = Link(download_url).filename
        download_file = os.path.join(PATH_DISTS, filename)
        
        dl = Downloader()
        dl.download(filename, download_url, download_file)
        
        install_dir = os.path.join(PATH_PYTHONS, pkgname)
        if is_python3:
            if os.path.isfile("%s/bin/python3" % (install_dir)):
                pyexec = "%s/bin/python3" % (install_dir)
            elif os.path.isfile("%s/bin/python3.0" % (install_dir)):
                pyexec = "%s/bin/python3.0" % (install_dir)
            else:
                logger.error("Python3 binary not found. `%s`" % (install_dir))
                return
        else:
            pyexec = os.path.join(install_dir,"bin","python")
        
        try:
            s = Subprocess(log=self.logfile, shell=True, cwd=PATH_DISTS, print_cmd=False)
            logger.info("Installing distribute into %s" % install_dir)
            s.check_call("%s %s" % (pyexec, filename))
            if os.path.isfile("%s/bin/easy_install" % (install_dir)) and not is_python3:
                logger.info("Installing pip into %s" % install_dir)
                s.check_call("%s/bin/easy_install pip" % (install_dir), cwd=None)
        except:
            logger.error("Failed to install setuptools. See %s/build.log to see why." % (ROOT))
            logger.info("Skip install setuptools.")




import os
import sys
import glob
import shutil
import re
import mimetypes
from pythonbrew.util import makedirs, symlink, Package, is_url, Link,\
    unlink, is_html, Subprocess, rm_r,\
    is_macosx_snowleopard, is_python25, is_python24, is_python26,\
    unpack_downloadfile, is_archive_file, path_to_fileurl, is_file,\
    fileurl_to_path
from pythonbrew.define import PATH_BUILD, PATH_BIN, PATH_DISTS, PATH_PYTHONS,\
    PATH_ETC, PATH_SCRIPTS, PATH_SCRIPTS_PYTHONBREW,\
    PATH_SCRIPTS_PYTHONBREW_COMMANDS, INSTALLER_ROOT, PATH_BIN_PYTHONBREW,\
    ROOT, PATH_LOG, DISTRIBUTE_SETUP_DLSITE, PATH_PATCHES,\
    PATH_PATCHES_MACOSX_PYTHON25, PATH_PATCHES_MACOSX_PYTHON24, PATH_ETC_CONFIG
from pythonbrew.downloader import get_python_version_url, Downloader,\
    get_headerinfo_from_url
from pythonbrew.log import logger

def install_pythonbrew():
    PythonbrewInstaller().install(INSTALLER_ROOT)
    
    # pythonbrew is only for bash
    shrc = yourshrc = "bashrc"
    logger.info("""
Well-done! Congratulations!

The pythonbrew is installed as:
    
  %(ROOT)s

Please add the following line to the end of your ~/.%(yourshrc)s

  source %(PATH_ETC)s/%(shrc)s

After that, exit this shell, start a new one, and install some fresh
pythons:

  pythonbrew install 2.6.6
  pythonbrew install 2.5.5

For further instructions, run:

  pythonbrew help

The default help messages will popup and tell you what to do!

Enjoy pythonbrew at %(ROOT)s!!
""" % {'ROOT':ROOT, 'yourshrc':yourshrc, 'shrc':shrc, 'PATH_ETC':PATH_ETC})

def upgrade_pythonbrew():
    PythonbrewInstaller().install(INSTALLER_ROOT)

class PythonbrewInstaller(object):
    def install(self, installer_root):
        # create directories
        makedirs(PATH_PYTHONS)
        makedirs(PATH_BUILD)
        makedirs(PATH_DISTS)
        makedirs(PATH_ETC)
        makedirs(PATH_BIN)
        makedirs(PATH_LOG)
        
        # remove old and create new script directories
        rm_r(PATH_SCRIPTS)
        makedirs(PATH_SCRIPTS)
        makedirs(PATH_SCRIPTS_PYTHONBREW)
        makedirs(PATH_SCRIPTS_PYTHONBREW_COMMANDS)
        
        # copy all py files
        for path in glob.glob(os.path.join(installer_root,"*.py")):
            shutil.copy(path, PATH_SCRIPTS_PYTHONBREW)
    
        for path in glob.glob(os.path.join(installer_root,"commands","*.py")):
            shutil.copy(path, PATH_SCRIPTS_PYTHONBREW_COMMANDS)
        
        # remove old and create patches direcotry
        rm_r(PATH_PATCHES)
        shutil.copytree(os.path.join(installer_root,"patches"), PATH_PATCHES)
        
        # create a main file
        fp = open("%s/pythonbrew_main.py" % PATH_SCRIPTS, "w")
        fp.write("""import pythonbrew
if __name__ == "__main__":
    pythonbrew.main()
""")
        fp.close()
        
        # create entry point file
        fp = open(PATH_BIN_PYTHONBREW, "w")
        fp.write("""#!/usr/bin/env bash
%s %s/pythonbrew_main.py "$@"
""" % (sys.executable, PATH_SCRIPTS))
        fp.close()
        os.chmod(PATH_BIN_PYTHONBREW, 0755)
        
        # create a bashrc for pythonbrew
        fp = open(os.path.join(PATH_ETC,'bashrc'), 'w')
        for line in open(os.path.join(installer_root,'etc','bashrc')):
            line = line.replace('@ROOT@', ROOT)
            fp.write(line)
        fp.close()
        
        # copy config.cfg
        shutil.copy(os.path.join(installer_root,'etc','config.cfg'), PATH_ETC_CONFIG)

class PythonInstaller(object):
    def __init__(self, arg, options):
        if is_url(arg):
            name = arg
        elif is_archive_file(arg):
            name = path_to_fileurl(arg)
        elif os.path.isdir(arg):
            name = path_to_fileurl(arg)
        else:
            name = arg
        
        if is_url(name):
            self.download_url = name
            filename = Link(self.download_url).filename
            pkg = Package(filename)
        else:
            pkg = Package(name)
            self.download_url = get_python_version_url(pkg.version)
            if not self.download_url:
                logger.info("Unknown python version: `%s`" % pkg.name)
                sys.exit(1)
            filename = Link(self.download_url).filename
        self.pkg = pkg
        self.install_dir = os.path.join(PATH_PYTHONS, pkg.name)
        self.build_dir = os.path.join(PATH_BUILD, pkg.name)
        self.download_file = os.path.join(PATH_DISTS, filename)
        if is_file(self.download_url):
            path = fileurl_to_path(self.download_url)
            self.content_type = mimetypes.guess_type(path)[0]
        else:
            headerinfo = get_headerinfo_from_url(self.download_url)
            self.content_type = headerinfo['content-type']
        self.options = options
        self.logfile = os.path.join(PATH_LOG, 'build.log')
    
    def install(self):
        if os.path.isdir(self.install_dir):
            logger.info("You are already installed `%s`" % self.pkg.name)
            sys.exit()
        self.ensure()
        self.download_unpack()
        logger.info("")
        logger.info("This could take a while. You can run the following command on another shell to track the status:")
        logger.info("  tail -f %s" % self.logfile)
        logger.info("")
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
        self.symlink()
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
    
    def download_unpack(self):
        content_type = self.content_type
        if is_html(content_type):
            logger.error("Invalid content-type: `%s`" % content_type)
            sys.exit(1)
        if is_file(self.download_url):
            path = fileurl_to_path(self.download_url)
            if os.path.isdir(path):
                logger.info('Copying %s into %s' % (path, self.build_dir))
                if os.path.isdir(self.build_dir):
                    shutil.rmtree(self.build_dir)
                shutil.copytree(path, self.build_dir)
                return
        if os.path.isfile(self.download_file):
            logger.info("Use the previously fetched %s" % (self.download_file))
        else:
            msg = Link(self.download_url).show_msg
            try:
                dl = Downloader()
                dl.download(msg, self.download_url, self.download_file)
            except:
                unlink(self.download_file)
                logger.info("\nInterrupt to abort. `%s`" % (self.download_url))
                sys.exit(1)
        # unpack
        if not unpack_downloadfile(self.content_type, self.download_file, self.build_dir):
            sys.exit(1)
    
    def patch(self):
        version = self.pkg.version
        try:
            s = Subprocess(log=self.logfile, cwd=self.build_dir)
            patches = []
            if is_macosx_snowleopard():
                if is_python24(version):
                    patch_dir = PATH_PATCHES_MACOSX_PYTHON24
                    patches = ['patch-configure', 'patch-Makefile.pre.in',
                               'patch-Lib-cgi.py.diff', 'patch-Lib-site.py.diff',
                               'patch-setup.py.diff', 'patch-Include-pyport.h',
                               'patch-Mac-OSX-Makefile.in', 'patch-Mac-OSX-IDLE-Makefile.in',
                               'patch-Mac-OSX-PythonLauncher-Makefile.in', 'patch-configure-badcflags.diff',
                               'patch-configure-arch_only.diff', 'patch-macosmodule.diff',
                               'patch-mactoolboxglue.diff', 'patch-pymactoolbox.diff',
                               'patch-gestaltmodule.c.diff']
                elif is_python25(version):
                    patch_dir = PATH_PATCHES_MACOSX_PYTHON25
                    patches = ['patch-Makefile.pre.in.diff', 'patch-Lib-cgi.py.diff',
                               'patch-Lib-distutils-dist.py.diff', 'patch-setup.py.diff',
                               'patch-configure-badcflags.diff', 'patch-configure-arch_only.diff',
                               'patch-64bit.diff', 'patch-pyconfig.h.in.diff',
                               'patch-Modules-posixmodule.c.diff', 'patch-gestaltmodule.c.diff']
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
                configure_option = '--with-universal-archs="intel" --enable-universalsdk=/ MACOSX_DEPLOYMENT_TARGET=10.6'
        
        s = Subprocess(log=self.logfile, cwd=self.build_dir)
        s.check_call("./configure --prefix=%s %s %s" % (self.install_dir, self.options.configure, configure_option))
        
    def make(self):
        s = Subprocess(log=self.logfile, cwd=self.build_dir)
        if self.options.force:
            s.check_call("make")
        else:
            s.check_call("make")
            s.check_call("make test")
            
    def make_install(self):
        version = self.pkg.version
        if version == "1.5.2" or version == "1.6.1":
            makedirs(self.install_dir)
        s = Subprocess(log=self.logfile, cwd=self.build_dir)
        s.check_call("make install")
    
    def symlink(self):
        install_dir = os.path.realpath(self.install_dir)
        path_python = os.path.join(install_dir,'bin','python')
        if not os.path.isfile(path_python):
            path_python3 = os.path.join(install_dir,'bin','python3')
            path_python3_0 = os.path.join(install_dir,'bin','python3.0')
            if os.path.isfile(path_python3):
                symlink(path_python3, path_python)
            elif os.path.isfile(path_python3_0):
                symlink(path_python3_0, path_python)
    
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
        path_python = os.path.join(install_dir,"bin","python")
        try:
            s = Subprocess(log=self.logfile, cwd=PATH_DISTS)
            logger.info("Installing distribute into %s" % install_dir)
            s.check_call("%s %s" % (path_python, filename))
            # Using easy_install install pip
            easy_install = os.path.join(install_dir, 'bin', 'easy_install')
            if os.path.isfile(easy_install) and not is_python3:
                logger.info("Installing pip into %s" % install_dir)
                s.check_call("%s pip" % (easy_install))
        except:
            logger.error("Failed to install setuptools. See %s/build.log to see why." % (ROOT))
            logger.info("Skip install setuptools.")




import os
import sys
import shutil
import mimetypes
from pythonbrew.util import makedirs, symlink, Package, is_url, Link,\
    unlink, is_html, Subprocess, rm_r,\
    is_python25, is_python24, is_python26, is_python27,\
    unpack_downloadfile, is_archive_file, path_to_fileurl, is_file,\
    fileurl_to_path
from pythonbrew.define import PATH_BUILD, PATH_DISTS, PATH_PYTHONS,\
    ROOT, PATH_LOG, DISTRIBUTE_SETUP_DLSITE,\
    PATH_PATCHES_MACOSX_PYTHON25, PATH_PATCHES_MACOSX_PYTHON24,\
    PATH_PATCHES_MACOSX_PYTHON26, PATH_PATCHES_MACOSX_PYTHON27, PATH_PATCHES_ALL
from pythonbrew.downloader import get_python_version_url, Downloader,\
    get_headerinfo_from_url
from pythonbrew.log import logger
from pythonbrew.exceptions import UnknownVersionException,\
    AlreadyInstalledException, NotSupportedVersionException

class PythonInstaller(object):
    """Python installer
    """

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
            pkg = Package(filename, options.alias)
        else:
            pkg = Package(name, options.alias)
            self.download_url = get_python_version_url(pkg.version)
            if not self.download_url:
                logger.info("Unknown python version: `%s`" % pkg.name)
                raise UnknownVersionException
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
        self.configure_options = ''
        self.patches = []

    def install(self):
        if os.path.isdir(self.install_dir):
            logger.info("You are already installed `%s`" % self.pkg.name)
            raise AlreadyInstalledException
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
        logger.info("  pythonbrew switch %s" % self.pkg.alias)

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
        if is_python25(version):
            patch_dir = os.path.join(PATH_PATCHES_ALL, "python25")
            self._add_patches_to_list(patch_dir, ['patch-setup.py.diff'])
        else:
            patch_dir = os.path.join(PATH_PATCHES_ALL, "common")
            self._add_patches_to_list(patch_dir, ['patch-setup.py.diff'])
        self._do_patch()
    
    def _do_patch(self):
        try:
            s = Subprocess(log=self.logfile, cwd=self.build_dir)
            if self.patches:
                logger.info("Patching %s" % self.pkg.name)
                for patch in self.patches:
                    if type(patch) is dict:
                        for (ed, source) in patch.items():
                            s.check_call('ed - %s < %s' % (source, ed))
                    else:
                        s.check_call("patch -p0 < %s" % patch)
        except:
            logger.error("Failed to patch `%s`" % self.build_dir)
            sys.exit(1)
    
    def _add_patches_to_list(self, patch_dir, patch_files):
        for patch in patch_files:
            if type(patch) is dict:
                for key in patch.keys():
                    patch[os.path.join(patch_dir, key)] = patch[key]
                    del patch[key]
                self.patches.append(patch)
            else:
                self.patches.append(os.path.join(patch_dir, patch))
    
    def configure(self):
        s = Subprocess(log=self.logfile, cwd=self.build_dir)
        s.check_call("./configure --prefix=%s %s %s" % (self.install_dir, self.options.configure, self.configure_options))

    def make(self):
        jobs = self.options.jobs
        make = ((jobs > 0 and 'make -j%s' % jobs) or 'make')
        s = Subprocess(log=self.logfile, cwd=self.build_dir)
        if self.options.force:
            s.check_call(make)
        else:
            s.check_call(make)
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
            if os.path.isfile(easy_install):
                logger.info("Installing pip into %s" % install_dir)
                s.check_call("%s pip" % (easy_install))
        except:
            logger.error("Failed to install setuptools. See %s/build.log to see why." % (ROOT))
            logger.info("Skip install setuptools.")

class PythonInstallerMacOSX(PythonInstaller):
    """Python installer for MacOSX SnowLeopard
    """
    def __init__(self, arg, options):
        super(PythonInstallerMacOSX, self).__init__(arg, options)
        version = self.pkg.version
        # check for version
        if version < '2.6' and (version != '2.4.6' and version < '2.5.5'):
            logger.info("`%s` is not supported on MacOSX Snow Leopard" % self.pkg.name)
            raise NotSupportedVersionException
        # set configure options
        if is_python24(version):
            self.configure_options = '--with-universal-archs="intel" MACOSX_DEPLOYMENT_TARGET=10.6 CPPFLAGS="-D__DARWIN_UNIX03"'
        elif is_python25(version):
            self.configure_options = '--with-universal-archs="intel" MACOSX_DEPLOYMENT_TARGET=10.6 CPPFLAGS="-D_DARWIN_C_SOURCE"'
        elif is_python26(version):
            self.configure_options = '--with-universal-archs="intel" --enable-universalsdk=/ MACOSX_DEPLOYMENT_TARGET=10.6'
        elif is_python27(version):
            self.configure_options = '--with-universal-archs="intel" --enable-universalsdk=/ MACOSX_DEPLOYMENT_TARGET=10.6'
        else:
            self.configure_options = '--with-universal-archs="intel" --enable-universalsdk=/ MACOSX_DEPLOYMENT_TARGET=10.6'

    def patch(self):
        version = self.pkg.version
        if is_python24(version):
            patch_dir = PATH_PATCHES_MACOSX_PYTHON24
            self._add_patches_to_list(patch_dir, ['patch-configure', 'patch-Makefile.pre.in',
                                                  'patch-Lib-cgi.py.diff', 'patch-Lib-site.py.diff',
                                                  'patch-setup.py.diff', 'patch-Include-pyport.h',
                                                  'patch-Mac-OSX-Makefile.in', 'patch-Mac-OSX-IDLE-Makefile.in',
                                                  'patch-Mac-OSX-PythonLauncher-Makefile.in', 'patch-configure-badcflags.diff',
                                                  'patch-configure-arch_only.diff', 'patch-macosmodule.diff',
                                                  'patch-mactoolboxglue.diff', 'patch-pymactoolbox.diff',
                                                  'patch-gestaltmodule.c.diff'])
        elif is_python25(version):
            patch_dir = PATH_PATCHES_MACOSX_PYTHON25
            self._add_patches_to_list(patch_dir, ['patch-Makefile.pre.in.diff',
                                                  'patch-Lib-cgi.py.diff',
                                                  'patch-Lib-distutils-dist.py.diff',
                                                  'patch-setup.py.diff',
                                                  'patch-configure-badcflags.diff',
                                                  'patch-configure-arch_only.diff',
                                                  'patch-64bit.diff',
                                                  'patch-pyconfig.h.in.diff',
                                                  'patch-gestaltmodule.c.diff',
                                                  {'_localemodule.c.ed': 'Modules/_localemodule.c'},
                                                  {'locale.py.ed': 'Lib/locale.py'}])
        elif is_python26(version):
            patch_dir = PATH_PATCHES_MACOSX_PYTHON26
            self._add_patches_to_list(patch_dir, ['patch-Lib-cgi.py.diff',
                                                  'patch-Lib-distutils-dist.py.diff',
                                                  'patch-Mac-IDLE-Makefile.in.diff',
                                                  'patch-Mac-Makefile.in.diff',
                                                  'patch-Mac-PythonLauncher-Makefile.in.diff',
                                                  'patch-Mac-Tools-Doc-setup.py.diff',
                                                  'patch-setup.py-db46.diff',
                                                  'patch-Lib-ctypes-macholib-dyld.py.diff',
                                                  'patch-setup_no_tkinter.py.diff',
                                                  {'_localemodule.c.ed': 'Modules/_localemodule.c'},
                                                  {'locale.py.ed': 'Lib/locale.py'}])
        elif is_python27(version):
            patch_dir = PATH_PATCHES_MACOSX_PYTHON27
            self._add_patches_to_list(patch_dir, ['patch-Modules-posixmodule.diff'])
            
        self._do_patch()

import os
import sys
import shutil
import mimetypes
import re
from pythonbrew.util import makedirs, symlink, Package, is_url, Link,\
    unlink, is_html, Subprocess, rm_r,\
    is_python25, is_python24, is_python26, is_python27,\
    extract_downloadfile, is_archive_file, path_to_fileurl, is_file,\
    fileurl_to_path, is_python30, is_python31, is_python32,\
    get_macosx_deployment_target, Version
from pythonbrew.define import PATH_BUILD, PATH_DISTS, PATH_PYTHONS,\
    ROOT, PATH_LOG, DISTRIBUTE_SETUP_DLSITE,\
    PATH_PATCHES_MACOSX_PYTHON25, PATH_PATCHES_MACOSX_PYTHON24,\
    PATH_PATCHES_MACOSX_PYTHON26, PATH_PATCHES_MACOSX_PYTHON27, PATH_PATCHES_ALL
from pythonbrew.downloader import get_python_version_url, Downloader,\
    get_headerinfo_from_url
from pythonbrew.log import logger
from pythonbrew.exceptions import UnknownVersionException,\
    NotSupportedVersionException

class PythonInstaller(object):
    """Python installer
    """

    def __init__(self, arg, options):
        if is_archive_file(arg):
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
                logger.error("Unknown python version: `%s`" % pkg.name)
                raise UnknownVersionException
            filename = Link(self.download_url).filename
        self.pkg = pkg
        self.install_dir = os.path.join(PATH_PYTHONS, pkg.name)
        self.build_dir = os.path.join(PATH_BUILD, pkg.name)
        self.download_file = os.path.join(PATH_DISTS, filename)

        self.options = options
        self.logfile = os.path.join(PATH_LOG, 'build.log')
        self.patches = []

        if Version(self.pkg.version) >= '3.1':
            self.configure_options = ['--with-computed-gotos']
        else:
            self.configure_options = []

    def install(self):
        # cleanup
        if os.path.isdir(self.build_dir):
            shutil.rmtree(self.build_dir)

        # get content type.
        if is_file(self.download_url):
            path = fileurl_to_path(self.download_url)
            self.content_type = mimetypes.guess_type(path)[0]
        else:
            headerinfo = get_headerinfo_from_url(self.download_url)
            self.content_type = headerinfo['content-type']
        if is_html(self.content_type):
            # note: maybe got 404 or 503 http status code.
            logger.error("Invalid content-type: `%s`" % self.content_type)
            return

        if os.path.isdir(self.install_dir):
            logger.info("You are already installed `%s`" % self.pkg.name)
            return

        self.download_and_extract()
        logger.info("\nThis could take a while. You can run the following command on another shell to track the status:")
        logger.info("  tail -f \"%s\"\n" % self.logfile)
        self.patch()
        logger.info("Installing %s into %s" % (self.pkg.name, self.install_dir))
        try:
            self.configure()
            self.make()
            self.make_install()
        except:
            rm_r(self.install_dir)
            logger.error("Failed to install %s. See %s to see why." % (self.pkg.name, self.logfile))
            sys.exit(1)
        self.symlink()
        self.install_setuptools()
        logger.info("\nInstalled %(pkgname)s successfully. Run the following command to switch to %(pkgname)s."
                    % {"pkgname":self.pkg.name})
        logger.info("  pythonbrew switch %s" % self.pkg.alias)

    def download_and_extract(self):
        if is_file(self.download_url):
            path = fileurl_to_path(self.download_url)
            if os.path.isdir(path):
                logger.info('Copying %s into %s' % (path, self.build_dir))
                shutil.copytree(path, self.build_dir)
                return
        if os.path.isfile(self.download_file):
            logger.info("Use the previously fetched %s" % (self.download_file))
        else:
            base_url = Link(self.download_url).base_url
            try:
                dl = Downloader()
                dl.download(base_url, self.download_url, self.download_file)
            except:
                unlink(self.download_file)
                logger.error("Failed to download.\n%s" % (sys.exc_info()[1]))
                sys.exit(1)
        # extracting
        if not extract_downloadfile(self.content_type, self.download_file, self.build_dir):
            sys.exit(1)

    def patch(self):
        version = Version(self.pkg.version)
        # for ubuntu 11.04(Natty)
        if is_python24(version):
            patch_dir = os.path.join(PATH_PATCHES_ALL, "python24")
            self._add_patches_to_list(patch_dir, ['patch-setup.py.diff'])
        elif is_python25(version):
            patch_dir = os.path.join(PATH_PATCHES_ALL, "python25")
            self._add_patches_to_list(patch_dir, ['patch-setup.py.diff'])
        elif is_python26(version):
            if version < '2.6.6':
                patch_dir = os.path.join(PATH_PATCHES_ALL, "python26")
                if version < '2.6.3':
                    self._add_patches_to_list(patch_dir, ['patch-Makefile.pre.in-for-2.6.2-and-earlier.diff'])
                self._add_patches_to_list(patch_dir, ['patch-setup.py-for-2.6.5-and-earlier.diff'])
                self._add_patches_to_list(patch_dir, ['patch-_ssl.c-for-ubuntu-oneiric-and-later.diff'])
            else:
                patch_dir = os.path.join(PATH_PATCHES_ALL, "common")
                self._add_patches_to_list(patch_dir, ['patch-setup.py.diff'])
        elif is_python27(version):
            if version < '2.7.2':
                patch_dir = os.path.join(PATH_PATCHES_ALL, "common")
                self._add_patches_to_list(patch_dir, ['patch-setup.py.diff'])
            if version == '2.7.3':
                patch_dir = os.path.join(PATH_PATCHES_ALL, "python27")
                self._add_patches_to_list(patch_dir, ['patch-Modules-_sqlite-connection.c.diff'])
            if version == '2.7.4':
                patch_dir = os.path.join(PATH_PATCHES_ALL, "python27")
                self._add_patches_to_list(patch_dir, ['patch-Modules-_sqlite-for-2.7.4.diff'])
        elif is_python30(version):
            patch_dir = os.path.join(PATH_PATCHES_ALL, "python30")
            self._add_patches_to_list(patch_dir, ['patch-setup.py.diff'])
        elif is_python31(version):
            if version < '3.1.4':
                patch_dir = os.path.join(PATH_PATCHES_ALL, "common")
                self._add_patches_to_list(patch_dir, ['patch-setup.py.diff'])
        elif is_python32(version):
            if version == '3.2':
                patch_dir = os.path.join(PATH_PATCHES_ALL, "python32")
                self._add_patches_to_list(patch_dir, ['patch-setup.py.diff'])
        self._do_patch()

    def _do_patch(self):
        try:
            s = Subprocess(log=self.logfile, cwd=self.build_dir, verbose=self.options.verbose)
            if self.patches:
                logger.info("Patching %s" % self.pkg.name)
                for patch in self.patches:
                    if type(patch) is dict:
                        for (ed, source) in patch.items():
                            s.shell('ed - "%s" < "%s"' % (source, ed))
                    else:
                        s.shell('patch -p0 < "%s"' % patch)
        except:
            logger.error("Failed to patch `%s`.\n%s" % (self.build_dir, sys.exc_info()[1]))
            sys.exit(1)

    def _add_patches_to_list(self, patch_dir, patch_files):
        for patch in patch_files:
            if type(patch) is dict:
                tmp = patch
                patch = {}
                for key in tmp.keys():
                    patch[os.path.join(patch_dir, key)] = tmp[key]
                self.patches.append(patch)
            else:
                self.patches.append(os.path.join(patch_dir, patch))

    def configure(self):
        s = Subprocess(log=self.logfile, cwd=self.build_dir, verbose=self.options.verbose)
        cmd = './configure --prefix="%s" %s %s' % (self.install_dir, self.options.configure, ' '.join(self.configure_options))
        if self.options.verbose:
            logger.log(cmd)
        s.check_call(cmd)

    def make(self):
        jobs = self.options.jobs
        make = ((jobs > 0 and 'make -j%s' % jobs) or 'make')
        s = Subprocess(log=self.logfile, cwd=self.build_dir, verbose=self.options.verbose)
        s.check_call(make)
        if self.options.test:
            if self.options.force:
                # note: ignore tests failure error.
                s.call("make test")
            else:
                s.check_call("make test")

    def make_install(self):
        version = Version(self.pkg.version)
        if version == "1.5.2" or version == "1.6.1":
            makedirs(self.install_dir)
        s = Subprocess(log=self.logfile, cwd=self.build_dir, verbose=self.options.verbose)
        s.check_call("make install")

    def symlink(self):
        install_dir = os.path.realpath(self.install_dir)
        if self.options.framework:
            # create symlink bin -> /path/to/Frameworks/Python.framework/Versions/?.?/bin
            bin_dir = os.path.join(install_dir, 'bin')
            if os.path.exists(bin_dir):
                rm_r(bin_dir)
            m = re.match(r'\d\.\d', self.pkg.version)
            if m:
                version = m.group(0)
            symlink(os.path.join(install_dir,'Frameworks','Python.framework','Versions',version,'bin'),
                    os.path.join(bin_dir))

        path_python = os.path.join(install_dir,'bin','python')
        if not os.path.isfile(path_python):
            src = None
            for d in os.listdir(os.path.join(install_dir,'bin')):
                if re.match(r'^python\d\.\d$', d):
                    src = d
                    break
            if src:
                path_src = os.path.join(install_dir,'bin',src)
                symlink(path_src, path_python)

    def install_setuptools(self):
        options = self.options
        pkgname = self.pkg.name
        if options.no_setuptools:
            logger.log("Skip installation of setuptools.")
            return
        download_url = DISTRIBUTE_SETUP_DLSITE
        filename = Link(download_url).filename
        download_file = os.path.join(PATH_DISTS, filename)

        dl = Downloader()
        dl.download(filename, download_url, download_file)

        install_dir = os.path.join(PATH_PYTHONS, pkgname)
        path_python = os.path.join(install_dir,"bin","python")
        try:
            s = Subprocess(log=self.logfile, cwd=PATH_DISTS, verbose=self.options.verbose)
            logger.info("Installing distribute into %s" % install_dir)
            s.check_call([path_python, filename])
            # installing pip
            easy_install = os.path.join(install_dir, 'bin', 'easy_install')
            if os.path.isfile(easy_install):
                logger.info("Installing pip into %s" % install_dir)
                s.check_call([easy_install, 'pip'])
        except:
            logger.error("Failed to install setuptools. See %s/log/build.log to see why." % (ROOT))
            logger.log("Skip installation of setuptools.")

class PythonInstallerMacOSX(PythonInstaller):
    """Python installer for MacOSX
    """
    def __init__(self, arg, options):
        super(PythonInstallerMacOSX, self).__init__(arg, options)

        # check for version
        version = Version(self.pkg.version)
        if version < '2.6' and (version != '2.4.6' and version < '2.5.5'):
            logger.error("`%s` is not supported on MacOSX Snow Leopard" % self.pkg.name)
            raise NotSupportedVersionException
        # set configure options
        target = get_macosx_deployment_target()
        if target:
            self.configure_options.append('MACOSX_DEPLOYMENT_TARGET=%s' % target)

        # set build options
        if options.framework and options.static:
            logger.error("Can't specify both framework and static.")
            raise Exception
        if options.framework:
            self.configure_options.append('--enable-framework=%s' % os.path.join(self.install_dir, 'Frameworks'))
        elif not options.static:
            self.configure_options.append('--enable-shared')
        if options.universal:
            self.configure_options.append('--enable-universalsdk=/')
            self.configure_options.append('--with-universal-archs=intel')

        # note: skip `make test` to avoid hanging test_threading.
        if is_python25(version) or is_python24(version):
            self.options.test = False

    def patch(self):
        # note: want an interface to the source patching functionality. like a patchperl.
        version = Version(self.pkg.version)
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
                                                  'patch-configure-no-posix-c-source.diff',
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
            if version < '2.7.4':
                patch_dir = PATH_PATCHES_MACOSX_PYTHON27
                self._add_patches_to_list(patch_dir, ['patch-Modules-posixmodule.diff'])

        self._do_patch()

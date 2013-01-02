import os
import sys
from pythonbrew.basecommand import Command
from pythonbrew.define import PATH_DISTS, VERSION, ROOT,\
    PATH_BUILD, PYTHONBREW_UPDATE_URL_CONFIG, PATH_ETC_CONFIG
from pythonbrew.log import logger
from pythonbrew.downloader import Downloader, get_pythonbrew_update_url,\
    get_stable_version, get_headerinfo_from_url
from pythonbrew.util import rm_r, extract_downloadfile, Link, is_gzip, Subprocess, Version

class UpdateCommand(Command):
    name = "update"
    usage = "%prog"
    summary = "Update the pythonbrew to the latest version"
    
    def __init__(self):
        super(UpdateCommand, self).__init__()
        self.parser.add_option(
            '--master',
            dest='master',
            action='store_true',
            default=False,
            help='Update the pythonbrew to the `master` branch on github.'
        )
        self.parser.add_option(
            '--config',
            dest='config',
            action='store_true',
            default=False,
            help='Update config.cfg.'
        )
        self.parser.add_option(
            '-f', '--force',
            dest='force',
            action='store_true',
            default=False,
            help='Force update the pythonbrew.'
        )
    
    def run_command(self, options, args):
        if options.config:
            self._update_config(options, args)
        else:
            self._update_pythonbrew(options, args)
    
    def _update_config(self, options, args):
        # config.cfg update
        # TODO: Automatically create for config.cfg
        download_url = PYTHONBREW_UPDATE_URL_CONFIG
        if not download_url:
            logger.error("Invalid download url in config.cfg. `%s`" % download_url)
            sys.exit(1)
        distname = Link(PYTHONBREW_UPDATE_URL_CONFIG).filename
        download_file = PATH_ETC_CONFIG
        try:
            d = Downloader()
            d.download(distname, download_url, download_file)
        except:
            logger.error("Failed to download. `%s`" % download_url)
            sys.exit(1)
        logger.log("The config.cfg has been updated.")
    
    def _update_pythonbrew(self, options, args):
        if options.master:
            version = 'master'
        else:
            version = get_stable_version()
            # check for version
            if not options.force and Version(version) <= VERSION:
                logger.info("You are already running the installed latest version of pythonbrew.")
                return
        
        download_url = get_pythonbrew_update_url(version)
        if not download_url:
            logger.error("`pythonbrew-%s` was not found in pypi." % version)
            sys.exit(1)
        headinfo = get_headerinfo_from_url(download_url)
        content_type = headinfo['content-type']
        if not options.master:
            if not is_gzip(content_type, Link(download_url).filename):
                logger.error("content type should be gzip. content-type:`%s`" % content_type)
                sys.exit(1)
        
        filename = "pythonbrew-%s" % version
        distname = "%s.tgz" % filename
        download_file = os.path.join(PATH_DISTS, distname)
        try:
            d = Downloader()
            d.download(distname, download_url, download_file)
        except:
            logger.error("Failed to download. `%s`" % download_url)
            sys.exit(1)
        
        extract_dir = os.path.join(PATH_BUILD, filename)
        rm_r(extract_dir)
        if not extract_downloadfile(content_type, download_file, extract_dir):
            sys.exit(1)
        
        try:
            logger.info("Installing %s into %s" % (extract_dir, ROOT))
            s = Subprocess()
            s.check_call([sys.executable, os.path.join(extract_dir,'pythonbrew_install.py'), '--upgrade'])
        except:
            logger.error("Failed to update pythonbrew.")
            sys.exit(1)
        logger.info("The pythonbrew has been updated.")

UpdateCommand()

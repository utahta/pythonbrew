import os
import sys
from pythonbrew.basecommand import Command
from pythonbrew.define import PATH_DISTS, VERSION, ROOT,\
    PATH_BUILD
from pythonbrew.log import logger
from pythonbrew.downloader import Downloader, get_pythonbrew_update_url,\
    get_response_from_url, get_stable_version
from pythonbrew.util import rm_r, unpack_downloadfile, Link, is_gzip
from pythonbrew.installer import PythonbrewInstaller

class UpdateCommand(Command):
    name = "update"
    usage = "%prog"
    summary = "Upgrades pythonbrew to the latest version"
    
    def run_command(self, options, args):
        if args:
            version = args[0]
        else:
            version = get_stable_version()
            
        # check for latest version
        if version <= VERSION:
            logger.info("You are already running the installed latest version of pythonbrew.")
            sys.exit()
        
        download_url = get_pythonbrew_update_url(version)
        if not download_url:
            logger.error("`%s` of pythonbrew not found." % version)
            sys.exit(1)
        resp = get_response_from_url(download_url)
        content_type = resp.info()['content-type']
        if not is_gzip(content_type, Link(download_url).filename):
            logger.error("Invalid content-type: `%s`" % content_type)
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
        if not unpack_downloadfile(content_type, download_file, extract_dir):
            sys.exit(1)
        
        try:
            installer_path = "%s/pythonbrew" % (extract_dir)
            logger.info("Installing %s into %s" % (extract_dir, ROOT))
            PythonbrewInstaller().install(installer_path)
        except:
            logger.error("Failed to update pythonbrew.")
            raise
            sys.exit(1)
        logger.info("The pythonbrew has been updated.")

UpdateCommand()

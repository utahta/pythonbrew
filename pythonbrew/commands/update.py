import os
import sys
import re
from pythonbrew.basecommand import Command
from pythonbrew.define import PATH_DISTS, VERSION, PYTHONBREW_DIRNAME, ROOT
from pythonbrew.log import logger
from pythonbrew.downloader import Downloader, get_pythonbrew_update_url
from pythonbrew.util import Subprocess, rm_r

class UpdateCommand(Command):
    name = "update"
    usage = "%prog"
    summary = "Upgrades pythonbrew to the latest version"
    
    def run_command(self, options, args):
        version = "head"
        if args:
            version = args[0]
            
        # check for latest version
        if version <= VERSION:
            logger.info("You are already running the installed latest version of pythonbrew.")
            sys.exit()
        
        download_url = get_pythonbrew_update_url(version)
        if not download_url:
            logger.error("`%s` of pythonbrew not found." % version)
            sys.exit(1)
        
        distname = "pythonbrew.tgz"
        download_path = "%s/%s" % (PATH_DISTS, distname)
        try:
            d = Downloader()
            d.download(distname, download_url, download_path)
        except:
            logger.error("Failed to download. `%s`" % download_url)
            sys.exit(1)

        _re = re.compile("^%s.*" % PYTHONBREW_DIRNAME)
        for name in os.listdir(PATH_DISTS):
            if _re.match(name):
                rm_r("%s/%s" % (PATH_DISTS, name))
        try:
            s = Subprocess(shell=True, cwd=PATH_DISTS, print_cmd=False)
            logger.info("Extracting %s" % download_path)
            s.check_call("tar zxf %s" % download_path)
        except:
            logger.error("Failed to update pythonbrew.")
            sys.exit(1)
        
        for name in os.listdir(PATH_DISTS):
            if _re.match(name):
                try:
                    installer_path = "%s/%s" % (PATH_DISTS, name)
                    s = Subprocess(shell=True, cwd=PATH_DISTS, print_cmd=False)
                    logger.info("Installing %s into %s" % (installer_path, ROOT))
                    s.check_call("%s %s/pythonbrew_install.py" % (sys.executable, installer_path))
                except:
                    logger.error("Failed to update pythonbrew.")
                    sys.exit(1)
                break
        logger.info("The pythonbrew has been updated.")

UpdateCommand()

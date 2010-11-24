import os
from subprocess import Popen, PIPE
from pythonbrew.basecommand import Command
from pythonbrew.define import PATH_PYTHONS
from pythonbrew.log import logger
from pythonbrew.util import get_current_python_path

class InstalledCommand(Command):
    name = "installed"
    usage = "%prog"
    summary = "List the installed versions of python"
    
    def run_command(self, options, args):
        cur = get_current_python_path()
        for d in sorted(os.listdir('%s/' % PATH_PYTHONS)):
            if cur == os.path.join(PATH_PYTHONS, d, 'bin','python'):
                logger.info('%s (*)' % d)
                cur = None
            else:
                logger.info(d)
        if cur:
            logger.info('%s (*)' % cur)
        
InstalledCommand()

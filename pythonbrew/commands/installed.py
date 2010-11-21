import os
import sys
from subprocess import Popen, PIPE
from pythonbrew.basecommand import Command
from pythonbrew.define import PATH_PYTHONS
from pythonbrew.log import logger

class InstalledCommand(Command):
    name = "installed"
    usage = "%prog"
    summary = "List the installed versions of python"
    
    def run_command(self, options, args):
        cur = None
        if not os.path.islink("%s/current" % PATH_PYTHONS):
            p = Popen('command -v python', stdout=PIPE, shell=True)
            p.wait()
            if p.returncode == 0:
                logger.info("%s (*)" % p.stdout.read().strip())
        elif os.path.islink("%s/current" % PATH_PYTHONS):
            cur = os.path.basename(os.path.realpath("%s/current" % PATH_PYTHONS))
        for d in sorted(os.listdir("%s/" % PATH_PYTHONS)):
            if d == "current":
                continue
            if cur == d:
                logger.info("%s (*)" % cur)
            else:
                logger.info("%s" % (d))

InstalledCommand()

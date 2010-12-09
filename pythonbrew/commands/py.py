import os
import sys
from pythonbrew.basecommand import Command
from pythonbrew.define import PATH_PYTHONS
from pythonbrew.util import Package
from pythonbrew.log import logger
from subprocess import Popen

class PyCommand(Command):
    name = "py"
    usage = "%prog PYTHON_FILE"
    summary = "Runs a named python file against specified and/or all pythons"
    
    def __init__(self):
        super(PyCommand, self).__init__()
        self.parser.add_option(
            "-p", "--python",
            dest="pythons",
            action="append",
            default=[],
            help="Using specified python versions."
        )
        self.parser.add_option(
            "-v", "--verbose",
            dest="verbose",
            action="store_true",
            default=False,
            help="Show python version."
        )
    
    def run_command(self, options, args):
        if not args:
            logger.info("Unrecognized command line argument: argument not found.")
            sys.exit(1)
        python_file = args[0]
        
        pythons = self._get_pythons(options.pythons)
        for d in pythons:
            path = os.path.join(PATH_PYTHONS, d, 'bin', 'python')
            if os.path.isfile(path) and os.access(path, os.X_OK):
                if options.verbose:
                    logger.info('*** %s ***' % d)
                p = Popen("%s %s" % (path, python_file), shell=True)
                p.wait()
    
    def _get_pythons(self, _pythons):
        pythons = [Package(p).name for p in _pythons]
        return [d for d in sorted(os.listdir(PATH_PYTHONS)) 
                if not pythons or d in pythons]

PyCommand()

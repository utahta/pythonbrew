from optparse import OptionParser
from pythonbrew.define import VERSION, PATH_BIN_PYTHONBREW

parser = OptionParser(usage="%prog COMMAND [OPTIONS]",
                      prog=PATH_BIN_PYTHONBREW,
                      version=VERSION,
                      add_help_option=False)
parser.add_option(
    '-h', '--help',
    dest='help',
    action='store_true',
    help='Show help')
parser.disable_interspersed_args()

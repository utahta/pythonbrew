from optparse import OptionParser
from pvm.define import VERSION

parser = OptionParser(usage="%prog COMMAND [OPTIONS]",
                      prog="pvm",
                      version=VERSION,
                      add_help_option=False)
parser.add_option(
    '-h', '--help',
    dest='help',
    action='store_true',
    help='Show help')
parser.disable_interspersed_args()

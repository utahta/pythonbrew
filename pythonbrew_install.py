from pythonbrew.installer import install_pythonbrew, upgrade_pythonbrew
from optparse import OptionParser
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option(
        '-U', '--upgrade',
        dest="upgrade",
        action="store_true",
        default=False,
        help="Upgrade."
    )
    (opt, arg) = parser.parse_args()
    if opt.upgrade:
        upgrade_pythonbrew()
    else:
        install_pythonbrew()

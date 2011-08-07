from pythonbrew.installer import install_pythonbrew, upgrade_pythonbrew, systemwide_pythonbrew
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
    parser.add_option(
        '--systemwide',
        dest="systemwide",
        action="store_true",
        default=False,
        help="systemwide install."
    )
    (opt, arg) = parser.parse_args()
    if opt.systemwide:
        systemwide_pythonbrew()
    elif opt.upgrade:
        upgrade_pythonbrew()
    else:
        install_pythonbrew()

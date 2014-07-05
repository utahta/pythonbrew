import os
import re
try:
    import ConfigParser
except:
    import configparser as ConfigParser

# pythonbrew version
VERSION = "1.3.5"

# pythonbrew installer root path
INSTALLER_ROOT = os.path.dirname(os.path.abspath(__file__))

# Root
# pythonbrew root path
ROOT = os.environ.get("PYTHONBREW_ROOT")
if not ROOT:
    ROOT = os.path.join(os.environ["HOME"],".pythonbrew")

# directories
PATH_PYTHONS = os.path.join(ROOT,"pythons")
PATH_BUILD = os.path.join(ROOT,"build")
PATH_DISTS = os.path.join(ROOT,"dists")
PATH_ETC = os.path.join(ROOT,"etc")
PATH_BIN = os.path.join(ROOT,"bin")
PATH_LOG = os.path.join(ROOT,"log")
PATH_VENVS = os.path.join(ROOT, "venvs")
PATH_SCRIPTS = os.path.join(ROOT,"scripts")
PATH_SCRIPTS_PYTHONBREW = os.path.join(PATH_SCRIPTS,"pythonbrew")
PATH_SCRIPTS_PYTHONBREW_COMMANDS = os.path.join(PATH_SCRIPTS_PYTHONBREW,"commands")
PATH_SCRIPTS_PYTHONBREW_INSTALLER = os.path.join(PATH_SCRIPTS_PYTHONBREW,"installer")
PATH_PATCHES = os.path.join(ROOT,"patches")
PATH_PATCHES_ALL = os.path.join(PATH_PATCHES,"all")
PATH_PATCHES_MACOSX = os.path.join(PATH_PATCHES,"macosx")
PATH_PATCHES_MACOSX_PYTHON27 = os.path.join(PATH_PATCHES_MACOSX,"python27")
PATH_PATCHES_MACOSX_PYTHON26 = os.path.join(PATH_PATCHES_MACOSX,"python26")
PATH_PATCHES_MACOSX_PYTHON25 = os.path.join(PATH_PATCHES_MACOSX,"python25")
PATH_PATCHES_MACOSX_PYTHON24 = os.path.join(PATH_PATCHES_MACOSX,"python24")

# files
PATH_BIN_PYTHONBREW = os.path.join(PATH_BIN,'pythonbrew')
PATH_ETC_CONFIG = os.path.join(PATH_ETC,'config.cfg')

# Home
# pythonbrew home path
PATH_HOME = os.environ.get('PYTHONBREW_HOME')
if not PATH_HOME:
    PATH_HOME = os.path.join(os.environ["HOME"],".pythonbrew")

# directories
PATH_HOME_ETC = os.path.join(PATH_HOME, 'etc')

# files
PATH_HOME_ETC_VENV = os.path.join(PATH_HOME_ETC, 'venv.run')
PATH_HOME_ETC_CURRENT = os.path.join(PATH_HOME_ETC,'current')
PATH_HOME_ETC_TEMP = os.path.join(PATH_HOME_ETC,'temp')

# read config.cfg
config = ConfigParser.SafeConfigParser()
config.read([PATH_ETC_CONFIG, os.path.join(INSTALLER_ROOT,'etc','config.cfg')])
def _get_or_default(section, option, default=''):
    try:
        return config.get(section, option)
    except:
        return default

# setuptools download
DISTRIBUTE_SETUP_DLSITE = _get_or_default('distribute', 'url')

# buildout bootstrap download
BOOTSTRAP_DLSITE = _get_or_default('bootstrap', 'url')

# virtualenv download
VIRTUALENV_DLSITE = _get_or_default('virtualenv', 'url')
VIRTUALENV_CLONE_DLSITE = _get_or_default('virtualenv-clone', 'url')

# pythonbrew download
PYTHONBREW_UPDATE_URL_MASTER = _get_or_default('pythonbrew', 'master')
PYTHONBREW_UPDATE_URL_DEVELOP = _get_or_default('pythonbrew', 'develop')
PYTHONBREW_UPDATE_URL_PYPI = _get_or_default('pythonbrew', 'pypi')
PYTHONBREW_UPDATE_URL_CONFIG = _get_or_default('pythonbrew', 'config')

# stable version text
PYTHONBREW_STABLE_VERSION_URL = _get_or_default('pythonbrew', 'stable-version')

# python download
LATEST_VERSIONS_OF_PYTHON = []
PYTHON_VERSION_URL = {}
PYTHON_VERSION_URL["1.5.2"] = _get_or_default('Python-1.5.2', 'url')
PYTHON_VERSION_URL["1.6.1"] = _get_or_default('Python-1.6.1', 'url')
for section in sorted(config.sections()):
    m = re.search("^Python-(.*)$", section)
    if m:
        version = m.group(1)
        PYTHON_VERSION_URL[version] = config.get(section, 'url')
        if config.has_option(section, 'latest') and config.getboolean(section, 'latest'):
            LATEST_VERSIONS_OF_PYTHON.append(version)

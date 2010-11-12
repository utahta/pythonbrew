import os

VERSION = "0.5"

if os.environ.has_key("PYTHONBREW_ROOT"):
    ROOT = os.environ["PYTHONBREW_ROOT"]
else:
    ROOT = "%s/.pythonbrew" % os.environ["HOME"]

INSTALLER_ROOT = os.path.dirname(os.path.abspath(__file__))

PATH_PYTHONS = "%s/pythons" % ROOT
PATH_BUILD = "%s/build" % ROOT
PATH_DISTS = "%s/dists" % ROOT
PATH_ETC = "%s/etc" % ROOT
PATH_BIN = "%s/bin" % ROOT
PATH_LOG = "%s/log" % ROOT
PATH_SCRIPTS = "%s/scripts" % ROOT
PATH_SCRIPTS_PYTHONBREW = "%s/pythonbrew" % PATH_SCRIPTS
PATH_SCRIPTS_PYTHONBREW_COMMANDS = "%s/commands" % PATH_SCRIPTS_PYTHONBREW

# file path
PATH_BIN_PYTHONBREW = "%s/pythonbrew" % PATH_BIN
PATH_BIN_PYBREW = "%s/pybrew" % PATH_BIN # pybrew is symlink as pythonbrew

# download setuptools url 
DISTRIBUTE_SETUP_DLSITE = "http://python-distribute.org/distribute_setup.py"

# download pythonbrew url
PYTHONBREW_UPDATE_URL = {
    "head": "http://github.com/utahta/pythonbrew/tarball/master"
}
PYTHONBREW_DIRNAME = "utahta-pythonbrew"

# download Python package url
PYTHON_PACKAGE_URL = {}
PYTHON_PACKAGE_URL["1.5.2"] = "http://www.python.org/ftp/python/src/py152.tgz"
PYTHON_PACKAGE_URL["1.6.1"] = "http://www.python.org/download/releases/1.6.1/Python-1.6.1.tar.gz"
_PYTHON_PACKAGE_VERSIONS = [
    "2.0", "2.0.1",
    "2.1", "2.1.1", "2.1.2", "2.1.3",
    "2.2", "2.2.1", "2.2.2", "2.2.3",
    "2.3", "2.3.1", "2.3.2", "2.3.4", "2.3.5", "2.3.6", "2.3.7",
    "2.4", "2.4.1", "2.4.2", "2.4.3", "2.4.4", "2.4.5", "2.4.6",
    "2.5", "2.5.1", "2.5.2", "2.5.3", "2.5.4", "2.5.5",
    "2.6", "2.6.1", "2.6.2", "2.6.3", "2.6.4", "2.6.5", "2.6.6",
    "2.7",
    "3.0", "3.0.1",
    "3.1", "3.1.1", "3.1.2",    
]
for version in _PYTHON_PACKAGE_VERSIONS:
    PYTHON_PACKAGE_URL[version] = "http://www.python.org/ftp/python/%s/Python-%s.tgz" % (version, version)
del _PYTHON_PACKAGE_VERSIONS
PYTHON_PACKAGE_URL["3.2a1"] = "http://www.python.org/ftp/python/3.2/Python-3.2a1.tgz"
PYTHON_PACKAGE_URL["3.2a2"] = "http://www.python.org/ftp/python/3.2/Python-3.2a2.tgz"


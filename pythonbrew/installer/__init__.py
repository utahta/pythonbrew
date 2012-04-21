import os

from pythonbrew.installer.pythonbrewinstaller import PythonbrewInstaller
from pythonbrew.log import logger
from pythonbrew.define import INSTALLER_ROOT, ROOT, PATH_ETC

def install_pythonbrew():
    PythonbrewInstaller.install(INSTALLER_ROOT)
    # for bash
    shrc = yourshrc = "bashrc"
    logger.log("""
Well-done! Congratulations!

The pythonbrew is installed as:
    
  %(ROOT)s

Please add the following line to the end of your ~/.%(yourshrc)s

  [[ -s "%(PATH_ETC)s/%(shrc)s" ]] && source "%(PATH_ETC)s/%(shrc)s"

After that, exit this shell, start a new one, and install some fresh
pythons:

  pythonbrew install 2.7.2
  pythonbrew install 3.2

For further instructions, run:

  pythonbrew help

The default help messages will popup and tell you what to do!

Enjoy pythonbrew at %(ROOT)s!!
""" % {'ROOT':ROOT, 'yourshrc':yourshrc, 'shrc':shrc, 'PATH_ETC':PATH_ETC.replace(os.getenv('HOME'), '$HOME')})

def upgrade_pythonbrew():
    PythonbrewInstaller.install(INSTALLER_ROOT)

def systemwide_pythonbrew():
    PythonbrewInstaller.install(INSTALLER_ROOT)
    PythonbrewInstaller.systemwide_install()
    logger.log("""
Well-done! Congratulations!

The pythonbrew is installed as:
    
  %(ROOT)s

After that, exit this shell, start a new one, and install some fresh
pythons:

  pythonbrew install 2.7.2
  pythonbrew install 3.2

For further instructions, run:

  pythonbrew help

The default help messages will popup and tell you what to do!

Enjoy pythonbrew at %(ROOT)s!!
""" % {'ROOT':ROOT})
        

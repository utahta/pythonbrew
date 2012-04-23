import os

from pvm.installer.pvminstaller import PvmInstaller
from pvm.log import logger
from pvm.define import INSTALLER_ROOT, ROOT, PATH_ETC

def install_pvm():
    PvmInstaller.install(INSTALLER_ROOT)
    # for bash
    shrc = yourshrc = "bashrc"
    logger.log("""
Well-done! Congratulations!

The pvm is installed as:
    
  %(ROOT)s

Please add the following line to the end of your ~/.%(yourshrc)s

  [[ -s "%(PATH_ETC)s/%(shrc)s" ]] && source "%(PATH_ETC)s/%(shrc)s"

After that, exit this shell, start a new one, and install some fresh
pythons:

  pvm install 2.7.2
  pvm install 3.2

For further instructions, run:

  pvm help

The default help messages will popup and tell you what to do!

Enjoy pvm at %(ROOT)s!!
""" % {'ROOT':ROOT, 'yourshrc':yourshrc, 'shrc':shrc, 'PATH_ETC':PATH_ETC.replace(os.getenv('HOME'), '$HOME')})

def upgrade_pvm():
    PvmInstaller.install(INSTALLER_ROOT)

def systemwide_pvm():
    PvmInstaller.install(INSTALLER_ROOT)
    PvmInstaller.systemwide_install()
    logger.log("""
Well-done! Congratulations!

The pvm is installed as:
    
  %(ROOT)s

After that, exit this shell, start a new one, and install some fresh
pythons:

  pvm install 2.7.2
  pvm install 3.2

For further instructions, run:

  pvm help

The default help messages will popup and tell you what to do!

Enjoy pvm at %(ROOT)s!!
""" % {'ROOT':ROOT})
        

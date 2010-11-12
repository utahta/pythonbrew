import os
import sys
import glob
import shutil
from pythonbrew.util import makedirs, symlink
from pythonbrew.define import PATH_BUILD, PATH_BIN, PATH_DISTS, PATH_PYTHONS,\
    PATH_ETC, PATH_SCRIPTS, PATH_SCRIPTS_PYTHONBREW,\
    PATH_SCRIPTS_PYTHONBREW_COMMANDS, INSTALLER_ROOT, PATH_BIN_PYTHONBREW,\
    PATH_BIN_PYBREW, ROOT, PATH_LOG

def install_pythonbrew():
    makedirs(PATH_PYTHONS)
    makedirs(PATH_BUILD)
    makedirs(PATH_DISTS)
    makedirs(PATH_ETC)
    makedirs(PATH_BIN)
    makedirs(PATH_LOG)
    makedirs(PATH_SCRIPTS)
    makedirs(PATH_SCRIPTS_PYTHONBREW)
    makedirs(PATH_SCRIPTS_PYTHONBREW_COMMANDS)

    for path in glob.glob("%s/*.py" % INSTALLER_ROOT):
        shutil.copy(path, PATH_SCRIPTS_PYTHONBREW)

    for path in glob.glob("%s/commands/*.py" % INSTALLER_ROOT):
        shutil.copy(path, PATH_SCRIPTS_PYTHONBREW_COMMANDS)

    fp = open("%s/pythonbrew.py" % PATH_SCRIPTS, "w")
    fp.write("""import pythonbrew
if __name__ == "__main__":
    pythonbrew.main()
""")
    fp.close()

    fp = open(PATH_BIN_PYTHONBREW, "w")
    fp.write("""#!/usr/bin/env bash
%s %s/pythonbrew.py "$@"
""" % (sys.executable, PATH_SCRIPTS))
    fp.close()
    os.chmod(PATH_BIN_PYTHONBREW, 0755)
    symlink(PATH_BIN_PYTHONBREW, PATH_BIN_PYBREW) # pyb as pythonbrew

    os.system("echo 'export PATH=%s/bin:%s/current/bin:${PATH}' > %s/bashrc" % (ROOT, PATH_PYTHONS, PATH_ETC))
    os.system("echo 'setenv PATH %s/bin:%s/current/bin:$PATH' > %s/cshrc" % (ROOT, PATH_PYTHONS, PATH_ETC))
    
    
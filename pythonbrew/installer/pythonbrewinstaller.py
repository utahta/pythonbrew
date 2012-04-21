import os
import sys
import glob
import shutil
from pythonbrew.util import makedirs, rm_r
from pythonbrew.define import PATH_BUILD, PATH_BIN, PATH_DISTS, PATH_PYTHONS,\
    PATH_ETC, PATH_SCRIPTS, PATH_SCRIPTS_PYTHONBREW,\
    PATH_SCRIPTS_PYTHONBREW_COMMANDS, PATH_BIN_PYTHONBREW,\
    PATH_LOG, PATH_PATCHES, PATH_ETC_CONFIG,\
    PATH_SCRIPTS_PYTHONBREW_INSTALLER, PATH_VENVS, PATH_HOME_ETC, ROOT
import stat
import time

class PythonbrewInstaller(object):
    """pythonbrew installer:
    """
    
    @staticmethod
    def install(installer_root):
        # create directories
        makedirs(PATH_PYTHONS)
        makedirs(PATH_BUILD)
        makedirs(PATH_DISTS)
        makedirs(PATH_ETC)
        makedirs(PATH_BIN)
        makedirs(PATH_LOG)
        makedirs(PATH_VENVS)
        makedirs(PATH_HOME_ETC)
        
        # create script directories
        rm_r(PATH_SCRIPTS)
        makedirs(PATH_SCRIPTS)
        makedirs(PATH_SCRIPTS_PYTHONBREW)
        makedirs(PATH_SCRIPTS_PYTHONBREW_COMMANDS)
        makedirs(PATH_SCRIPTS_PYTHONBREW_INSTALLER)
        
        # copy all .py files
        for path in glob.glob(os.path.join(installer_root,"*.py")):
            shutil.copy(path, PATH_SCRIPTS_PYTHONBREW)
        for path in glob.glob(os.path.join(installer_root,"commands","*.py")):
            shutil.copy(path, PATH_SCRIPTS_PYTHONBREW_COMMANDS)
        for path in glob.glob(os.path.join(installer_root,"installer","*.py")):
            shutil.copy(path, PATH_SCRIPTS_PYTHONBREW_INSTALLER)
        
        # create patches direcotry
        rm_r(PATH_PATCHES)
        shutil.copytree(os.path.join(installer_root,"patches"), PATH_PATCHES)
        
        # create a main file
        fp = open("%s/pythonbrew_main.py" % PATH_SCRIPTS, "w")
        fp.write("""import pythonbrew
if __name__ == "__main__":
    pythonbrew.main()
""")
        fp.close()
        
        # create entry point file
        fp = open(PATH_BIN_PYTHONBREW, "w")
        fp.write("""#!/usr/bin/env bash
%s "%s/pythonbrew_main.py" "$@"
""" % (sys.executable, PATH_SCRIPTS))
        fp.close()
        # mode 0755
        os.chmod(PATH_BIN_PYTHONBREW, stat.S_IRUSR|stat.S_IWUSR|stat.S_IXUSR|stat.S_IRGRP|stat.S_IXGRP|stat.S_IROTH|stat.S_IXOTH)
        
        # create a bashrc for pythonbrew
        shutil.copy(os.path.join(installer_root,'etc','bashrc'), os.path.join(PATH_ETC,'bashrc'))
        
        # copy config.cfg
        shutil.copy(os.path.join(installer_root,'etc','config.cfg'), PATH_ETC_CONFIG)
    
    @staticmethod
    def systemwide_install():
        profile = """\
#begin-pythonbrew
if [ -n "${BASH_VERSION:-}" -o -n "${ZSH_VERSION:-}" ] ; then
    export PYTHONBREW_ROOT=%(root)s
    source "${PYTHONBREW_ROOT}/etc/bashrc"
fi
#end-pythonbrew
""" % {'root': ROOT}
        
        if os.path.isdir('/etc/profile.d'):
            fp = open('/etc/profile.d/pythonbrew.sh', 'w')
            fp.write(profile)
            fp.close()
        elif os.path.isfile('/etc/profile'):
            # create backup
            shutil.copy('/etc/profile', '/tmp/profile.pythonbrew.%s' % int(time.time()))
            
            output = []
            is_copy = True
            fp = open('/etc/profile', 'r')
            for line in fp:
                if line.startswith('#begin-pythonbrew'):
                    is_copy = False
                    continue
                elif line.startswith('#end-pythonbrew'):
                    is_copy = True
                    continue
                if is_copy:
                    output.append(line)
            fp.close()
            output.append(profile)
            
            fp = open('/etc/profile', 'w')
            fp.write(''.join(output))
            fp.close()
        

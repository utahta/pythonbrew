from tests import PYTHONBREW_ROOT
import os

BUILDOUT_DIR = os.path.join(PYTHONBREW_ROOT, 'etc', 'buildout')
BUILDOUT_CONF = os.path.join(BUILDOUT_DIR, 'buildout.cfg')

def _create_buildout_cfg():
    if not os.path.isdir(BUILDOUT_DIR):
        os.makedirs(BUILDOUT_DIR)
    fp = open(BUILDOUT_CONF, 'w')
    fp.write("""[buildout]
parts = test
develop =

[test]
recipe = 
eggs =""")
    fp.close()

class BuildoutOptions(object):
    python = '2.6.6'

def test_buildout():
    from pythonbrew.commands.buildout import BuildoutCommand
    
    # Runs the buildout
    _create_buildout_cfg()
    os.chdir(BUILDOUT_DIR)
    c = BuildoutCommand()
    c.run_command(BuildoutOptions(), [])
    
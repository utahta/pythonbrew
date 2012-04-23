# coding=utf-8
#---------------------------------------------------------------------------
# Copyright 2011 utahta
#---------------------------------------------------------------------------
import os
import shutil

#---------------------------------------------------------------------------
# Settings
#---------------------------------------------------------------------------
PYTHONBREW_ROOT = '/tmp/pvm.test'
TESTPY_VERSION = ['2.4.6', '2.5.5', '2.6.6', '3.2']

def _cleanall():
    if os.path.isdir(PYTHONBREW_ROOT):
        shutil.rmtree(PYTHONBREW_ROOT)

def _install_pvm():
    from pvm.installer import install_pvm
    install_pvm()

def setup():
    os.environ['PYTHONBREW_ROOT'] = PYTHONBREW_ROOT
    _cleanall()
    _install_pvm()

def teardown():
    _cleanall()

class Options(object):
    def __init__(self, opts):
        for (k,v) in opts.items():
            setattr(self, k, v)

#---------------------------------------------------------------------------
# Test
#---------------------------------------------------------------------------
def test_00_update():
    from pvm.commands.update import UpdateCommand
    c = UpdateCommand()
    c.run_command(Options({'master':False, 'develop':False, 'config':False, 'force':False}), 
                  None)

def test_01_help():
    from pvm.commands.help import HelpCommand
    c = HelpCommand()
    c.run_command(None, None)

def test_02_version():
    from pvm.commands.version import VersionCommand
    c = VersionCommand()
    c.run_command(None, None)

def test_03_install():
    from pvm.commands.install import InstallCommand
    py_version = TESTPY_VERSION.pop(0)
    o = Options({'force':True, 'test':True, 'verbose':False, 'configure':"",
                 'no_setuptools': False, 'alias':None, 'jobs':2, 
                 'framework':False, 'universal':False, 'static':False})
    c = InstallCommand()
    c.run_command(o, [py_version]) # pybrew install -f -j2 2.4.6
    c.run_command(o, TESTPY_VERSION) # pybrew install -f -j2 2.5.6 2.6.6 3.2

def test_04_switch():
    from pvm.commands.switch import SwitchCommand
    for py_version in TESTPY_VERSION:
        c = SwitchCommand()
        c.run_command(None, [py_version])

def test_05_use():
    from pvm.commands.use import UseCommand
    for py_version in TESTPY_VERSION:
        c = UseCommand()
        c.run_command(None, [py_version])

def test_06_off():
    from pvm.commands.off import OffCommand
    c = OffCommand()
    c.run_command(None, None)

def test_07_list():
    from pvm.commands.list import ListCommand
    c = ListCommand()
    c.run_command(Options({'all_versions':False, 'known':False}), 
                  None)

def test_08_py():
    from pvm.commands.py import PyCommand
    TESTPY_FILE = os.path.join(PYTHONBREW_ROOT, 'etc', 'testfile.py')
    fp = open(TESTPY_FILE, 'w')
    fp.write("print('test')")
    fp.close()
    # Runs the python script
    c = PyCommand()
    c.run_command(Options({'pythons':[], 'verbose':False, 'bin':"python", 'options':""}), 
                  [TESTPY_FILE])

def test_09_buildout():
    from pvm.commands.buildout import BuildoutCommand
    BUILDOUT_DIR = os.path.join(PYTHONBREW_ROOT, 'etc', 'buildout')
    BUILDOUT_CONF = os.path.join(BUILDOUT_DIR, 'buildout.cfg')
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
    # Runs the buildout
    os.chdir(BUILDOUT_DIR)
    c = BuildoutCommand()
    c.run_command(Options({'python':'2.6.6'}), [])

def test_10_venv():
    from pvm.commands.venv import VenvCommand
    c = VenvCommand()
    o = Options({'python':'2.6.6', 'all':False, 'no_site_packages':False})
    c.run_command(o, ['init'])
    c.run_command(o, ['create', 'aaa'])
    c.run_command(o, ['list'])
    c.run_command(o, ['use', 'aaa'])
    c.run_command(o, ['delete', 'aaa'])

def test_11_uninstall():
    from pvm.commands.uninstall import UninstallCommand
    for py_version in TESTPY_VERSION:
        c = UninstallCommand()
        c.run_command(None, [py_version])

def test_12_clean():
    from pvm.commands.cleanup import CleanupCommand
    c = CleanupCommand()
    c.run_command(None, None)


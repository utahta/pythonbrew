import os
import shutil
from unittest import TestCase
from nose.tools import ok_, eq_

class PythonbrewTestCast(TestCase):
    class Options(object):
        def __init__(self, opts):
            for (k,v) in opts.items():
                setattr(self, k, v)

    def setUp(self):
        os.environ['PYTHONBREW_ROOT'] = '/tmp/pythonbrew.test'
        os.environ['PYTHONBREW_HOME'] = '/tmp/pythonbrew.test'
        self._cleanall()
        from pythonbrew.define import PATH_DISTS, PATH_LOG, PATH_ETC, PATH_PYTHONS, PATH_VENVS, PATH_BIN, PATH_BUILD
        for path in [PATH_DISTS, PATH_LOG, PATH_ETC, PATH_PYTHONS, PATH_VENVS, PATH_BIN, PATH_BUILD]:
            if not os.path.exists(path):
                os.makedirs(path)

    def tearDown(self):
        self._cleanall()

    def _cleanall(self):
        from pythonbrew.define import ROOT
        shutil.rmtree(ROOT, True)

    def test_update(self):
        from pythonbrew.commands.update import UpdateCommand
        c = UpdateCommand()
        c.run_command(self.Options({'master': True, 'develop': False, 'config': False, 'force': False}), None)

    def test_help(self):
        from pythonbrew.commands.help import HelpCommand
        c = HelpCommand()
        c.run_command(None, None)

    def test_version(self):
        from pythonbrew.commands.version import VersionCommand
        c = VersionCommand()
        c.run_command(None, None)

    def test_install_2_7_10(self):
        from pythonbrew.commands.install import InstallCommand
        from pythonbrew.util import is_installed
        o = self.Options({'force': True, 'test': False, 'verbose': False, 'configure': "",
                          'no_setuptools': False, 'alias': None, 'jobs': 2,
                          'framework': False, 'universal': False, 'static': False})
        c = InstallCommand()
        c.run_command(o, ['2.7.10'])
        ok_(is_installed('2.7.10'))

    def test_install_3_4_3(self):
        from pythonbrew.commands.install import InstallCommand
        from pythonbrew.util import is_installed
        o = self.Options({'force': True, 'test': False, 'verbose': False, 'configure': "",
                          'no_setuptools': False, 'alias': None, 'jobs': 2,
                          'framework': False, 'universal': False, 'static': False})
        c = InstallCommand()
        c.run_command(o, ['3.4.3'])
        ok_(is_installed('3.4.3'))

    def test_switch(self):
        from pythonbrew.commands.switch import SwitchCommand
        from pythonbrew.define import PATH_HOME_ETC_CURRENT
        self._create_dummy('2.7.5')
        eq_(False, os.path.isfile(PATH_HOME_ETC_CURRENT))
        c = SwitchCommand()
        c.run_command(None, ['2.7.5'])
        ok_(os.path.isfile(PATH_HOME_ETC_CURRENT))

    def test_use(self):
        from pythonbrew.commands.use import UseCommand
        from pythonbrew.define import PATH_HOME_ETC_TEMP
        self._create_dummy('2.7.5')
        eq_(False, os.path.isfile(PATH_HOME_ETC_TEMP))
        c = UseCommand()
        c.run_command(None, ['2.7.5'])
        ok_(os.path.isfile(PATH_HOME_ETC_TEMP))

    def test_off(self):
        from pythonbrew.commands.off import OffCommand
        from pythonbrew.define import PATH_HOME_ETC_CURRENT
        eq_(False, os.path.isfile(PATH_HOME_ETC_CURRENT))
        c = OffCommand()
        c.run_command(None, None)
        ok_(os.path.isfile(PATH_HOME_ETC_CURRENT))

    def test_list(self):
        from pythonbrew.commands.list import ListCommand
        c = ListCommand()
        c.run_command(self.Options({'all_versions': False, 'known': False}), None)

    def test_py(self):
        from pythonbrew.commands.py import PyCommand
        from pythonbrew.define import PATH_ETC
        testpy_file = os.path.join(PATH_ETC, 'testfile.py')
        fp = open(testpy_file, 'w')
        fp.write("print('test')")
        fp.close()
        c = PyCommand()
        c.run_command(self.Options({'pythons': [], 'verbose': False, 'bin': "python", 'options': ""}), [testpy_file])

    def test_venv(self):
        from pythonbrew.commands.venv import VenvCommand
        from pythonbrew.commands.install import InstallCommand
        o = self.Options({'force': True, 'test': False, 'verbose': False, 'configure': "",
                          'no_setuptools': False, 'alias': None, 'jobs': 2,
                          'framework': False, 'universal': False, 'static': False})
        c = InstallCommand()
        c.run_command(o, ['3.4.3'])
        c = VenvCommand()
        o = self.Options({'python': '3.4.3', 'no_site_packages': False, 'system_site_packages': False})
        c.run_command(o, ['init'])
        c.run_command(o, ['create', 'aaa'])
        c.run_command(o, ['list'])
        c.run_command(o, ['use', 'aaa'])
        c.run_command(o, ['delete', 'aaa'])

    def test_uninstall(self):
        from pythonbrew.commands.uninstall import UninstallCommand
        from pythonbrew.util import is_installed
        self._create_dummy('2.7.5')
        c = UninstallCommand()
        c.run_command(None, ['2.7.5'])
        eq_(False, is_installed('2.7.5'))

    def test_clean(self):
        from pythonbrew.commands.cleanup import CleanupCommand
        from pythonbrew.define import PATH_BUILD, PATH_DISTS
        for path in [PATH_BUILD, PATH_DISTS]:
            fp = open(os.path.join(path, 'dummy.txt'), 'w')
            fp.write('')
            fp.close()
        c = CleanupCommand()
        c.run_command(None, None)
        eq_(0, len(os.listdir(PATH_BUILD)))
        eq_(0, len(os.listdir(PATH_DISTS)))

    def _create_dummy(self, version):
        from pythonbrew.define import PATH_PYTHONS
        from pythonbrew.util import Package
        pkgname = Package(version).name
        os.makedirs(os.path.join(PATH_PYTHONS, pkgname))
        os.makedirs(os.path.join(PATH_PYTHONS, pkgname, 'bin'))
        os.makedirs(os.path.join(PATH_PYTHONS, pkgname, 'lib'))

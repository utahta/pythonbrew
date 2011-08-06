class VenvOptions(object):
    python = '2.6.6'
    all = False
    no_site_packages = False

def test_venv():
    import os
    from pythonbrew.commands.venv import VenvCommand
    from pythonbrew.util import Subprocess
    from pythonbrew.define import PATH_HOME_ETC_VENV
    s = Subprocess()
    c = VenvCommand()
    c.run_command(VenvOptions(), ['init'])
    c.run_command(VenvOptions(), ['create', 'aaa'])
    s.shell('source %s' % PATH_HOME_ETC_VENV)
    c.run_command(VenvOptions(), ['list'])
    c.run_command(VenvOptions(), ['use', 'aaa'])
    c.run_command(VenvOptions(), ['delete', 'aaa'])
    s.shell('source %s' % PATH_HOME_ETC_VENV)
    # finish
    os.unlink(PATH_HOME_ETC_VENV)

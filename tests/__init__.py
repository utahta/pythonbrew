import os
import shutil

PYTHONBREW_ROOT = '/tmp/pythonbrew.test'
TESTPY_VERSION = ['2.4.6', '2.5.5', '2.6.6', '3.2']
def cleanall():
    if os.path.isdir(PYTHONBREW_ROOT):
        shutil.rmtree(PYTHONBREW_ROOT)

def setup():
    os.environ['PYTHONBREW_ROOT'] = PYTHONBREW_ROOT
    cleanall()
    from pythonbrew.installer import install_pythonbrew
    install_pythonbrew()
    
def teardown():
    cleanall()

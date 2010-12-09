import os
import shutil

PYTHONBREW_ROOT = '/tmp/pythonbrew.test'
TESTPY_FILE = '/tmp/pythonbrew_test.py'
TESTPY_VERSION = '2.6.6'
def cleanall():
    if os.path.isdir(PYTHONBREW_ROOT):
        shutil.rmtree(PYTHONBREW_ROOT)
    if os.path.isfile(TESTPY_FILE):
        os.remove(TESTPY_FILE)

def setup():
    os.environ['PYTHONBREW_ROOT'] = PYTHONBREW_ROOT
    cleanall()
    fp = open(TESTPY_FILE, 'w')
    fp.write("print 'test'")
    fp.close()
    
def teardown():
    cleanall()

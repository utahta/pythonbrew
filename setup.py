import os
from setuptools import setup, find_packages
from pythonbrew.define import VERSION

README = os.path.join(os.path.dirname(__file__),'PKG-INFO')
long_description = open(README).read() + "\n"

setup(name='pythonbrew',
      version=VERSION,
      description="Manage python installations in your $HOME",
      long_description=long_description,
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
      ],
      keywords='pythonbrew pip easy_install distutils setuptools virtualenv',
      author='utahta',
      author_email='labs.ninxit@gmail.com',
      url='https://github.com/utahta/pythonbrew',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      entry_points=dict(console_scripts=['pythonbrew_install=pythonbrew.installer:install_pythonbrew']),
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)

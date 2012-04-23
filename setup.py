import os
from setuptools import setup, find_packages
from pvm.define import VERSION

README = os.path.join(os.path.dirname(__file__),'PKG-INFO')
long_description = open(README).read() + "\n"

setup(name='pvm',
      version=VERSION,
      description="Manage python installations in your $HOME",
      long_description=long_description,
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
      ],
      keywords='pvm pip easy_install distutils setuptools virtualenv',
      author='utahta',
      author_email='labs.ninxit@gmail.com',
      url='https://github.com/utahta/pvm',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      entry_points=dict(console_scripts=['pvm_install=pvm.installer:install_pvm']),
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)

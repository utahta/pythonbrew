Overview
========

pythonbrew is a program to automate the building and installation of Python in the users HOME.

pythonbrew is based on `perlbrew <http://github.com/gugod/App-perlbrew>`_.

Installation
============

Following python version is required to use pythonbrew:
 2.4 <= Python < 3

The recommended way to download and install pythonbrew is to run these statements in your shell.::

  curl -LO http://github.com/utahta/pythonbrew/raw/master/pythonbrew
  chmod +x pythonbrew
  ./pythonbrew install

After that, pythonbrew installs itself to ~/python/pythonbrew/bin, and you should follow the instruction on screen to setup your .bashrc or .cshrc to put it in your PATH.

If you need to install pythonbrew into somewhere else, you can do that by setting a PYTHONBREW_ROOT environment variable.::

  export PYTHONBREW_ROOT=/path/to/pythonbrew
  ./pythonbrew install

Usage
=====

pythonbrew [options] [init|install|installed|switch|search|uninstall|off|version]
    
Initialize::

  pythonbrew init
    
Install some Pythons::

  pythonbrew install Python-3.1.2
  pythonbrew install Python-2.6.6
  pythonbrew install --build-options="CC=gcc_4.1" Python-2.6.6
  pythonbrew install --no-setuptools Python-2.6.6
  pythonbrew install http://www.python.org/ftp/python/2.6.6/Python-2.6.6.tgz
  pythonbrew install /path/to/Python-2.6.6.tgz
    
Switch python in the $PATH::

  pythonbrew switch Python-2.6.6
  pythonbrew switch /path/to/python

Search python packages::

  pythonbrew search Python-2.6
  pythonbrew search Python-3

Uninstall some Pythons::

  pythonbrew uninstall Python-2.6.6

Disable pythonbrew::

  pythonbrew off

Show version::

  pythonbrew version

COMMANDS
========

init
  Run this once to setup the pythonbrew directory ready for installing.
  
  pythons into. Run it again if you decide to change PYTHONBREW_ROOT.

install Python-<version>
  Build and install the given version of Python.
  
  Setuptools and pip is automatically installed.
  
  options: --force, --no-setuptools or --build-options.

installed
  List the installed versions of python.

switch Python-<version>
  Switch to the given version.

switch /path/to/Python-dir/
  Switch to the given version of python in directory.

switch /path/to/python
  Switch to the given version of python.

search Python-<version>
  Search Python packages.
  
uninstall Python-<version>
  Uninstall the given version of python.

off
  Disable pythonbrew.

version
  Show version.

Options
=======

\-f --force
  Force installation of a Python.

\-b --build-options
  Configure options of Python.

\-n --no-setuptools
  Skip installation of setuptools.

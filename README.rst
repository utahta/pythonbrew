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

pythonbrew [options] [init|install|installed|switch|off|version]
    
Initialize::

  pythonbrew init
    
Install some Pythons::

  pythonbrew install Python-2.6.6
  pythonbrew install Python-2.5.5
  pythonbrew --build-options="CC=gcc_4.1" install Python-2.5.4
  pythonbrew --no-setuptools install Python-2.5.3
    
Switch python in the $PATH::

  pythonbrew switch Python-2.6.6
  pythonbrew switch /path/to/Python-2.5.5/
  pythonbrew switch /path/to/python
    
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
  
  Setuptools is automatically installed.
  
  options: --force, --no-setuptools or --build-options.

installed
  List the installed versions of python.

switch Python-<version>
  Switch to the given version.

switch /path/to/Python-dir/
  Switch to the given version of python in directory.

switch /path/to/python
  Switch to the given version of python.

off
  Disable pythonbrew.

version
  Show version.

Options
=======

\--force
  Force installation of a Python.

\--build-options
  Configure options.

\--no-setuptools
  Skip installation of setuptools.

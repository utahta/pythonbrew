.. image:: https://travis-ci.org/utahta/pythonbrew.svg?branch=master
    :target: https://travis-ci.org/utahta/pythonbrew

Deprecated
==========

This project is no longer under active development.

You are encouraged to try out `pyenv <https://github.com/yyuu/pyenv>`_ instead.

Overview
========

pythonbrew is a program to automate the building and installation of Python in the users $HOME.

pythonbrew is inspired by `perlbrew <http://github.com/gugod/App-perlbrew>`_ and `rvm <https://github.com/wayneeseguin/rvm>`_.

Installation
============

The recommended way to download and install pythonbrew is to run these statements in your shell::

  curl -kL http://xrl.us/pythonbrewinstall | bash

After that, pythonbrew installs itself to ~/.pythonbrew. 

Please add the following line to the end of your ~/.bashrc::

  [[ -s $HOME/.pythonbrew/etc/bashrc ]] && source $HOME/.pythonbrew/etc/bashrc

If you need to install pythonbrew into somewhere else, you can do that by setting a PYTHONBREW_ROOT environment variable::

  export PYTHONBREW_ROOT=/path/to/pythonbrew
  curl -kLO http://xrl.us/pythonbrewinstall
  chmod +x pythonbrewinstall
  ./pythonbrewinstall

Readline Support
----------------

Python uses a library called `readline` to allow line editing and command history.  If you use Python interactively, it is recommended to install both the `readline` library and its headers.  Otherwise, the arrow keys won't work in the Python interactive shell.

On Debian and Ubuntu systems, the required package is called `libreadline-dev`.  On Fedora, Red Hat, and CentOS, the package is called `readline-devel`.  No extra packages are required on Arch or Gentoo.

The `readline` support package must be installed before Python in order to work properly.

For Systemwide(Multi-User) installation
---------------------------------------

If the install script is run as root, pythonbrew will automatically install into /usr/local/pythonbrew.

The pythonbrew will be automatically configured for every user on the system if you install as root.

After installation, where you would normally use `sudo`, non-root users will need to use `sudopybrew`::

  sudopybrew install -v -j2 2.7.2

Usage
=====

pythonbrew command [options]
    
Install some pythons::

  pythonbrew install 2.7.2
  pythonbrew install --verbose 2.7.2
  pythonbrew install --test 2.7.2
  pythonbrew install --test --force 2.7.2
  pythonbrew install --configure="CC=gcc_4.1" 2.7.2
  pythonbrew install --no-setuptools 2.7.2
  pythonbrew install http://www.python.org/ftp/python/2.7/Python-2.7.2.tgz
  pythonbrew install /path/to/Python-2.7.2.tgz
  pythonbrew install /path/to/Python-2.7.2
  pythonbrew install 2.7.2 3.2
  
Permanently use the specified python::

  pythonbrew switch 2.7.2
  pythonbrew switch 3.2

Use the specified python in current shell::

  pythonbrew use 2.7.2

Runs a named python file against specified and/or all pythons::

  pythonbrew py test.py
  pythonbrew py -v test.py # Show verbose output
  pythonbrew py -p 2.7.2 -p 3.2 test.py # Use the specified pythons

List the installed pythons::

  pythonbrew list

List the available installation pythons::

  pythonbrew list -k

Uninstall the specified python::

  pythonbrew uninstall 2.7.2
  pythonbrew uninstall 2.7.2 3.2

Remove stale source folders and archives::

  pythonbrew cleanup

Upgrades pythonbrew to the latest version::

  pythonbrew update
  pythonbrew update --master
  pythonbrew update --develop

Disable pythonbrew::

  pythonbrew off
  
Create/Remove a symbolic link to python (in a directory on your $PATH)::

  pythonbrew symlink # Create a symbolic link, like "py2.7.2", for each installed version
  pythonbrew symlink -p 2.7.2
  pythonbrew symlink pip # Create a symbolic link to the specified script in bin directory
  pythonbrew symlink -r # Remove a symbolic link
  pythonbrew symlink -v foo # Create a symbolic link to the specified virtual environment python in bin directory

Runs the buildout with specified or current using python::
  
  pythonbrew buildout
  pythonbrew buildout -p 2.6.6

Create isolated python environments (uses virtualenv)::
  
  pythonbrew venv init
  pythonbrew venv create proj
  pythonbrew venv list
  pythonbrew venv use proj
  pythonbrew venv delete proj
  pythonbrew venv rename proj proj2
  pythonbrew venv clone proj proj2

Show version::

  pythonbrew version

COMMANDS
========

install <version>
  Build and install the given version of python.
  Install setuptools and pip automatically.

switch <version>
  Permanently use the specified python as default.

use <version>
  Use the specified python in current shell.

py <python file>
  Runs a named python file against specified and/or all pythons.

list
  List the installed all pythons.
  
list -k <version>
  List the available install pythons.
  
uninstall <version>
  Uninstall the given version of python.

cleanup
  Remove stale source folders and archives.

update
  Upgrades pythonbrew to the latest version.

off
  Disable pythonbrew.
  
symlink
  Create/Remove a symbolic link to python (in a directory on your $PATH)
  
buildout
  Runs the buildout with specified or current using python.
  
venv
  Create isolated python environments (uses virtualenv)
  
version
  Show version.
  
See more details below
  `pythonbrew help <command>`

LICENCE
=======

The MIT License

Copyright (c) <2010-2012> <utahta>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

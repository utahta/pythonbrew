Overview
========

pythonbrew is a program to automate the building and installation of Python in the users $HOME.

pythonbrew is inspired by `perlbrew <http://github.com/gugod/App-perlbrew>`_ and `rvm <https://github.com/wayneeseguin/rvm>`_.

Installation
============

The recommended way to download and install pythonbrew is to run these statements in your shell::

  curl -kL http://xrl.us/pythonbrewinstall | bash

After that, pythonbrew installs itself to ~/.pythonbrew, and you should follow the instruction on screen to setup your .bashrc to put it in your PATH.

If you need to install pythonbrew into somewhere else, you can do that by setting a PYTHONBREW_ROOT environment variable::

  export PYTHONBREW_ROOT=/path/to/pythonbrew
  curl -kLO http://xrl.us/pythonbrewinstall
  chmod +x pythonbrewinstall
  ./pythonbrewinstall

Usage
=====

pythonbrew command [options]
    
Install some pythons::

  pythonbrew install 2.7.2
  pythonbrew install --verbose 2.7.2
  pythonbrew install --force 2.7.2
  pythonbrew install --no-test 2.7.2
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

Runs the buildout with specified or current using python::
  
  pythonbrew buildout
  pythonbrew buildout -p 2.6.6

Create isolated python environments::
  
  pythonbrew venv create proj1
  pythonbrew venv list
  pythonbrew venv use proj1
  pythonbrew venv delete proj1

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
  Create isolated python environments.
  
version
  Show version.
  
See more details below:

  pythonbrew help <command>

LICENCE
=======

The MIT License

Copyright (c) <2010-2011> <utahta>

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

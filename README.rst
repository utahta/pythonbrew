Overview
========

pythonbrew is a program to automate the building and installation of Python in the users HOME.

pythonbrew is inspired by `perlbrew <http://github.com/gugod/App-perlbrew>`_ and `rvm <https://github.com/wayneeseguin/rvm>`_.

Installation
============

The recommended way to download and install pythonbrew is to run these statements in your shell::

  curl -kLO http://github.com/utahta/pythonbrew/raw/master/pythonbrew-install
  chmod +x pythonbrew-install
  ./pythonbrew-install

or more simply like this::

  curl -kL http://github.com/utahta/pythonbrew/raw/master/pythonbrew-install | bash

After that, pythonbrew installs itself to ~/.pythonbrew, and you should follow the instruction on screen to setup your .bashrc to put it in your PATH.

If you need to install pythonbrew into somewhere else, you can do that by setting a PYTHONBREW_ROOT environment variable::

  export PYTHONBREW_ROOT=/path/to/pythonbrew
  ./pythonbrew-install

Usage
=====

pythonbrew command [options]
    
Install some pythons::

  pythonbrew install 2.6.6
  pythonbrew install --force 2.6.6
  pythonbrew install --configure="CC=gcc_4.1" 2.6.6
  pythonbrew install --no-setuptools 2.6.6
  pythonbrew install http://www.python.org/ftp/python/2.7/Python-2.6.6.tgz
  pythonbrew install file:///path/to/Python-2.6.6.tgz
  pythonbrew install /path/to/Python-2.6.6.tgz
  pythonbrew install 2.5.5 2.6.6
  
Permanently use the specified python as default::

  pythonbrew switch 2.6.6
  pythonbrew switch 2.5.5

Use the specified python in current shell::

  pythonbrew use 2.6.6

Runs a named python file against specified and/or all pythons::

  pythonbrew py test.py
  pythonbrew py -v test.py # Show running python version
  pythonbrew py -p 2.6.6 -p 3.1.2 test.py # Use the specified pythons

List the installed pythons::

  pythonbrew list

List the available install pythons::

  pythonbrew list -k

Uninstall the specified python::

  pythonbrew uninstall 2.6.6
  pythonbrew uninstall 2.5.5 2.6.6

Remove stale source folders and archives::

  pythonbrew clean

Upgrades pythonbrew to the latest version::

  pythonbrew update

Disable pythonbrew::

  pythonbrew off
  
Create/Remove a symbolic link to python::

  pythonbrew symlink # Create a symbolic link, like "py2.5.5"
  pythonbrew symlink -p 2.5.5
  pythonbrew symlink -b pip # Create a symbolic link to the specified script in bin directory
  pythonbrew symlink -r # Remove a symbolic link

Show version::

  pythonbrew version

COMMANDS
========

install <version>
  Build and install the given version of python.
  
  Setuptools and pip is automatically installed.
  
  options: --force, --no-setuptools, --configure and --as.

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

clean
  Remove stale source folders and archives.

update
  Upgrades pythonbrew to the latest version.

off
  Disable pythonbrew.

version
  Show version.

Options
=======

\-f | --force
  Force installation of a python. (skip `make test`)

\-C | --configure
  Custom configure options.

\-n | --no-setuptools
  Skip installation of setuptools.

\--as
  Install a python under an alias.

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

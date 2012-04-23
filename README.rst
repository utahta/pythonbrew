Overview
========

pvm is a program to automate the building and installation of Python in the users $HOME.

pvm is inspired by `perlbrew <http://github.com/gugod/App-perlbrew>`_ and `rvm <https://github.com/wayneeseguin/rvm>`_.

:Forked: `pythonz <https://github.com/saghul/pythonz>`_

Installation
============

The recommended way to download and install pvm is to run these statements in your shell::

  curl -kL http://xrl.us/pvminstall | bash

After that, pvm installs itself to ~/.pvm. 

Please add the following line to the end of your ~/.bashrc::

  [[ -s $HOME/.pvm/etc/bashrc ]] && source $HOME/.pvm/etc/bashrc

If you need to install pvm into somewhere else, you can do that by setting a PYTHONBREW_ROOT environment variable::

  export PYTHONBREW_ROOT=/path/to/pvm
  curl -kLO http://xrl.us/pvminstall
  chmod +x pvminstall
  ./pvminstall

For Systemwide(Multi-User) installation
---------------------------------------

If the install script is run as root, pvm will automatically install into /usr/local/pvm.

The pvm will be automatically configured for every user on the system if you install as root.

After installation, where you would normally use `sudo`, non-root users will need to use `sudopybrew`::

  sudopybrew install -n -v -j2 2.7.2

Usage
=====

pvm command [options]
    
Install some pythons::

  pvm install 2.7.2
  pvm install --verbose 2.7.2
  pvm install --test 2.7.2
  pvm install --test --force 2.7.2
  pvm install --configure="CC=gcc_4.1" 2.7.2
  pvm install --no-setuptools 2.7.2
  pvm install http://www.python.org/ftp/python/2.7/Python-2.7.2.tgz
  pvm install /path/to/Python-2.7.2.tgz
  pvm install /path/to/Python-2.7.2
  pvm install 2.7.2 3.2
  
Permanently use the specified python::

  pvm switch 2.7.2
  pvm switch 3.2

Use the specified python in current shell::

  pvm use 2.7.2

Runs a named python file against specified and/or all pythons::

  pvm py test.py
  pvm py -v test.py # Show verbose output
  pvm py -p 2.7.2 -p 3.2 test.py # Use the specified pythons

List the installed pythons::

  pvm list

List the available installation pythons::

  pvm list -k

Uninstall the specified python::

  pvm uninstall 2.7.2
  pvm uninstall 2.7.2 3.2

Remove stale source folders and archives::

  pvm cleanup

Upgrades pvm to the latest version::

  pvm update
  pvm update --master
  pvm update --develop

Disable pvm::

  pvm off
  
Create/Remove a symbolic link to python (in a directory on your $PATH)::

  pvm symlink # Create a symbolic link, like "py2.7.2", for each installed version
  pvm symlink -p 2.7.2
  pvm symlink pip # Create a symbolic link to the specified script in bin directory
  pvm symlink -r # Remove a symbolic link
  pvm symlink -v foo # Create a symbolic link to the specified virtual environment python in bin directory

Runs the buildout with specified or current using python::
  
  pvm buildout
  pvm buildout -p 2.6.6

Create isolated python environments (uses virtualenv)::
  
  pvm venv init
  pvm venv create proj
  pvm venv list
  pvm venv use proj
  pvm venv delete proj
  pvm venv rename proj proj2

Show version::

  pvm version

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
  Upgrades pvm to the latest version.

off
  Disable pvm.
  
symlink
  Create/Remove a symbolic link to python (in a directory on your $PATH)
  
buildout
  Runs the buildout with specified or current using python.
  
venv
  Create isolated python environments (uses virtualenv)
  
version
  Show version.
  
See more details below
  `pvm help <command>`

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

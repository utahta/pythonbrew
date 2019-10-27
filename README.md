# pythonbrew

[![CircleCI](https://circleci.com/gh/utahta/pythonbrew/tree/master.svg?style=svg)](https://circleci.com/gh/utahta/pythonbrew/tree/master)
[![Go Report Card](https://goreportcard.com/badge/github.com/utahta/pythonbrew)](https://goreportcard.com/report/github.com/utahta/pythonbrew)
[![GitHub release](https://img.shields.io/github/release/utahta/pythonbrew.svg)](https://github.com/utahta/pythonbrew/releases)

## Note

This project is no longer under active development.

You can try to [pyenv](https://github.com/pyenv/pyenv)(under active development) instead of pythonbrew.

# Overview

pythonbrew is the Python environments manager. it's easy to switch between them.

Inspired by [perlbrew](http://github.com/gugod/App-perlbrew) and [rvm](https://github.com/wayneeseguin/rvm).

# Installation

The recommended way to download from [each releases](https://github.com/utahta/pythonbrew/releases) and put it somewhere in your PATH.

Or you can get as below
```sh
go get -u github.com/utahta/pythonbrew/cmd/pythonbrew
```

Typically, pythonbrew install packages into ~/.pythonbrew.  
If you want to install packages into somewhere else, you can do that by setting a PYTHONBREW_ROOT environment variable
```sh
export PYTHONBREW_ROOT=/path/to/.pythonbrew
```

# Setup

## Bash

Add the following line at the end of the ~/.bashrc file
```sh
eval "$(pythonbrew init)"
```

## Zsh

Add the following line at the end of the ~/.zshrc file
```sh
eval "$(pythonbrew init)"
```

# Usage

pythonbrew(pybrew) command [options]

Install some pythons
```
pythonbrew install 3.6.4
pythonbrew install -v 3.6.4
pythonbrew install -f 3.6.4
pythonbrew install -C "CFLAGS=-I/path/to/include" -C "LDFLAGS=-L/path/to/lib" 3.6.4
pythonbrew install --no-ensurepip 3.6.4
pythonbrew install --no-symlink 3.6.4
pythonbrew install https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tgz
pythonbrew install 2.7.14 3.6.4
```

Use a specific Python version permanently
```
pythonbrew switch 2.7.14
pythonbrew switch 3.6.4
```

Use a specific Python version in the current shell
```
pythonbrew use 3.6.4
```

List all installed Python versions
```
pythonbrew list
```

List all known installable Python versions
```
pythonbrew list -k
```

Uninstall specific Python versions
```
pythonbrew uninstall 2.7.14
```

Disable pythonbrew
```
pythonbrew off
```

Manage environments (using virtualenv)
```
pythonbrew venv proj             # Create proj if not exists, Use proj if exists
pythonbrew venv -p 2.7.14 proj2
pythonbrew venv -l
pythonbrew venv --rm proj
```

Remove all cache
```
pythonbrew cleanup
```

Update pythonbrew to the latest version
```
pythonbrew update
```

Show version
```
pythonbrew -v
```

See more details
```
pythonbrew -h
pythonbrew <command> -h
```

# Recommended Packages

## Debian and Ubuntu

```
apt-get install zlib1g-dev libssl-dev libreadline-dev
```

## Fedora, Red Hat and CentOS

```
yum install zlib-devel openssl-devel readline-devel
```

## macOS

```
brew install openssl
brew install readline
```

# Uninstallation

```sh
rm /path/to/pythonbrew
rm -rf ~/.pythonbrew
```
Remove `eval "$(pythonbrew init)"` line at the setup file.

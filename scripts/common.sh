#!/bin/bash

trim() {
    local trimmed=$1
    trimmed="${trimmed#"${trimmed%%[![:space:]]*}"}"   # remove leading whitespace characters
    trimmed="${trimmed%"${trimmed##*[![:space:]]}"}"   # remove trailing whitespace characters
    echo ${trimmed}
}

version() {
    local curdir=$(dirname $0)
    local v=`cat ${curdir}/../version.txt`
    v=`trim ${v}`
    echo ${v}
}

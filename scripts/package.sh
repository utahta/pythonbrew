#!/bin/bash

curdir=$(dirname $0)
distdir=${curdir}/../dist

source ${curdir}/common.sh

export GOFLAGS="-trimpath"
gox -ldflags="-X github.com/utahta/pythonbrew/subcmd.Version=$(version)" github.com/utahta/pythonbrew/cmd/pythonbrew/

rm -rf ${distdir}
mkdir -p ${distdir}
mv pythonbrew_* ${distdir}/

cd ${distdir}
for name in pythonbrew_*; do
    if [ "${name#*.}" = "exe" ]; then
        command="pythonbrew.exe"
    else
        command="pythonbrew"
    fi

    mv "${name}" "${command}"
    zip "${name}.zip" "${command}"
    rm "${command}"
done

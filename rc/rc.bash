# run command for bash

if [ -z "${PYTHONBREW_BIN}" ]; then
    export PYTHONBREW_BIN=$(command -v pythonbrew)
fi

__pythonbrew_get_root_path() {
    local path_root="${PYTHONBREW_ROOT}"
    if [ -z "${path_root}" ]; then
        path_root="${HOME}/.pythonbrew"
    fi
    echo ${path_root}
}

__pythonbrew_get_home_path() {
    local path_home="${PYTHONBREW_HOME}"
    if [ -z "${path_home}" ]; then
        path_home="${HOME}/.pythonbrew"
    fi
    echo ${path_home}
}

__pythonbrew_export_path() {
    local path_root=$(__pythonbrew_get_root_path)
    local path_env=$(__pythonbrew_get_home_path)/$1

    if [ -e "${path_env}" ]; then
        PYTHONBREW_VERSION=""
        PYTHONBREW_VERSION_BIN=""
        PYTHONBREW_VERSION_LIB=""

        source "${path_env}"
        local path_version_bin="${PYTHONBREW_VERSION_BIN}"
        local path_version_lib="${PYTHONBREW_VERSION_LIB}"

        local path_without_version=$(printf "%s" "${PATH}" |
        awk -v path_root="${path_root//\\//\\/}" 'BEGIN{RS=ORS=":"} $0 !~ path_root' |
        sed -e 's#:$##')

        export PYTHONBREW_VERSION="${PYTHONBREW_VERSION}"
        if [ -n "${path_version_bin}" ]; then
            export PATH="${path_version_bin}:${path_without_version}"
        else
            export PATH="${path_without_version}"
        fi
        if [ -n "${path_version_lib}" ]; then
            export PYTHONPATH="${path_version_lib}"
        else
            unset PYTHONPATH
        fi
    fi
}

__pythonbrew_venv() {
    local path_env=$(__pythonbrew_get_home_path)/env/venv

    if [ -s "${path_env}" ]; then
        source ${path_env}
        cat /dev/null > ${path_env}
    fi
}

pythonbrew() {
    local subcommand
    for arg in "$@" ; do
        case ${arg} in
            --*) continue;;
            -*) continue;;
            *)
            subcommand=${arg}
            break
            ;;
        esac
    done

    ${PYTHONBREW_BIN} "$@"

    local exitcode=$?
    if [ ${exitcode} = 0 ]; then
        case ${subcommand} in
            use)    __pythonbrew_export_path "env/tmp" ;;
            switch) __pythonbrew_export_path "env/permanent" ;;
            off)    __pythonbrew_export_path "env/permanent" ;;
            venv)   __pythonbrew_venv ;;
        esac
        builtin hash -r
    fi
    return ${exitcode}
}

pybrew() {
    pythonbrew "$@"
}

# main
__pythonbrew_export_path "env/permanent"

package rc

import (
	"time"

	"github.com/jessevdk/go-assets"
)

var _Assetse92f762c9de0ef0082f8c57509509f135541430e = "# run command for bash\n\nif [ -z \"${PYTHONBREW_BIN}\" ]; then\n    export PYTHONBREW_BIN=$(command -v pythonbrew)\nfi\n\n__pythonbrew_get_root_path() {\n    local path_root=\"${PYTHONBREW_ROOT}\"\n    if [ -z \"${path_root}\" ]; then\n        path_root=\"${HOME}/.pythonbrew\"\n    fi\n    echo ${path_root}\n}\n\n__pythonbrew_get_home_path() {\n    local path_home=\"${PYTHONBREW_HOME}\"\n    if [ -z \"${path_home}\" ]; then\n        path_home=\"${HOME}/.pythonbrew\"\n    fi\n    echo ${path_home}\n}\n\n__pythonbrew_export_path() {\n    local path_root=$(__pythonbrew_get_root_path)\n    local path_env=$(__pythonbrew_get_home_path)/$1\n\n    if [ -e \"${path_env}\" ]; then\n        PYTHONBREW_VERSION=\"\"\n        PYTHONBREW_VERSION_BIN=\"\"\n        PYTHONBREW_VERSION_LIB=\"\"\n\n        source \"${path_env}\"\n        local path_version_bin=\"${PYTHONBREW_VERSION_BIN}\"\n        local path_version_lib=\"${PYTHONBREW_VERSION_LIB}\"\n\n        local path_without_version=$(printf \"%s\" \"${PATH}\" |\n        awk -v path_root=\"${path_root//\\\\//\\\\/}\" 'BEGIN{RS=ORS=\":\"} $0 !~ path_root' |\n        sed -e 's#:$##')\n\n        export PYTHONBREW_VERSION=\"${PYTHONBREW_VERSION}\"\n        if [ -n \"${path_version_bin}\" ]; then\n            export PATH=\"${path_version_bin}:${path_without_version}\"\n        else\n            export PATH=\"${path_without_version}\"\n        fi\n        if [ -n \"${path_version_lib}\" ]; then\n            export PYTHONPATH=\"${path_version_lib}\"\n        else\n            unset PYTHONPATH\n        fi\n    fi\n}\n\n__pythonbrew_venv() {\n    local path_env=$(__pythonbrew_get_home_path)/env/venv\n\n    if [ -s \"${path_env}\" ]; then\n        source ${path_env}\n        cat /dev/null > ${path_env}\n    fi\n}\n\npythonbrew() {\n    local subcommand\n    for arg in \"$@\" ; do\n        case ${arg} in\n            --*) continue;;\n            -*) continue;;\n            *)\n            subcommand=${arg}\n            break\n            ;;\n        esac\n    done\n\n    ${PYTHONBREW_BIN} \"$@\"\n    if [ $? = 0 ]; then\n        case ${subcommand} in\n            use)    __pythonbrew_export_path \"env/tmp\" ;;\n            switch) __pythonbrew_export_path \"env/permanent\" ;;\n            off)    __pythonbrew_export_path \"env/permanent\" ;;\n            venv)   __pythonbrew_venv ;;\n        esac\n        builtin hash -r\n    fi\n}\n\npybrew() {\n    pythonbrew \"$@\"\n}\n\n# main\n__pythonbrew_export_path \"env/permanent\"\n"

// Assets returns go-assets FileSystem
var Assets = assets.NewFileSystem(map[string][]string{"/": []string{"rc.bash"}}, map[string]*assets.File{
	"/": &assets.File{
		Path:     "/",
		FileMode: 0x800001ed,
		Mtime:    time.Unix(1515687259, 1515687259000000000),
		Data:     nil,
	}, "/rc.bash": &assets.File{
		Path:     "/rc.bash",
		FileMode: 0x1a4,
		Mtime:    time.Unix(1515687259, 1515687259000000000),
		Data:     []byte(_Assetse92f762c9de0ef0082f8c57509509f135541430e),
	}}, "")

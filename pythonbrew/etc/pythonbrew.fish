# settings
set PATH_ROOT "$PYTHONBREW_ROOT"
if test -z "$PATH_ROOT" 
    set PATH_ROOT "$HOME/.pythonbrew"
end
set PATH_ETC "$PATH_ROOT/etc"

set PATH_HOME "$PYTHONBREW_HOME"
if test -z "$PATH_HOME"
    set PATH_HOME "$HOME/.pythonbrew"
end

set PATH_HOME_ETC "$PATH_HOME/etc"

# py file
set PY_PYTHONBREW "$PATH_ROOT/bin/pythonbrew"

# functions
function __pythonbrew_set_default
    set PATH_PYTHONBREW "$PATH_ROOT/bin"
end

function __pythonbrew_set_path
    set PATH_WITHOUT_PYTHONBREW ""
    for p in $PATH
        if test $p != $PATH_PYTHONBREW
            set PATH_WITHOUT_PYTHONBREW $PATH_WITHOUT_PYTHONBREW $p
        end        
    end
    set -x PATH $PATH_PYTHONBREW $PATH_WITHOUT_PYTHONBREW
end

function __bash_as_set
    set fname $argv[1]
    eval (perl -ne 's/(^\w*)=(.*)$/set $1 $2/g;print $_;' < "$fname")
end

set PATH_PYTHONBREW_TEMP ""
function __pythonbrew_set_temp_path
    if test -s "$PATH_HOME_ETC/temp"
        __bash_as_set "$PATH_HOME_ETC/temp"
        set PATH_PYTHONBREW $PATH_ROOT/bin $PATH_PYTHONBREW_TEMP
    else
        __pythonbrew_set_default
    end
    __pythonbrew_set_path
end

set PATH_PATH_PYTHONBREW_CURRENT ""
function __pythonbrew_set_current_path
    if test -s "$PATH_HOME_ETC/current"
        __bash_as_set "$PATH_HOME_ETC/current"
        set PATH_PYTHONBREW $PATH_ROOT/bin $PATH_PYTHONBREW_CURRENT
    else
        __pythonbrew_set_default
    end
    __pythonbrew_set_path
end

function __pythonbrew_reload
    test -s "$PATH_ETC/bashrc"; and . "$PATH_ETC/bashrc"
end

function __pythonbrew_use
    eval $pythonbrew $argv
    test $status -eq 0; and __pythonbrew_set_temp_path
end

function __pythonbrew_switch
    eval $pythonbrew $argv
    test $status -eq 0; and  __pythonbrew_set_current_path
end

function __pythonbrew_off
    eval $pythonbrew $argv
    test $status -eq 0; and  __pythonbrew_set_current_path
end

function __pythonbrew_update
    eval $pythonbrew $argv
    test $status -eq 0; and  __pythonbrew_reload
end

function __pythonbrew_venv
    pythonbrew $argv    
    if $status
        if test -s "$PATH_HOME_ETC/venv.run" 
            . "$PATH_HOME_ETC/venv.run"
            cat /dev/null > "$PATH_HOME_ETC/venv.run"
        end
    end
end

set command_name ""
function __pythonbrew_find_command
    set command_name ""
    for arg in $argv
        switch $arg
            case '--*'
                continue
            case '-*'
                continue
            case '*'
                set command_name $arg 
                break
        end        
    end
end

function __pythonbrew_run
    __pythonbrew_find_command $argv
    switch $command_name
        case 'use'
            __pythonbrew_use $argv
        case 'switch'
            __pythonbrew_switch $argv
        case 'off'
            __pythonbrew_off $argv
        case 'update'
            __pythonbrew_update $argv
        case 'venv'
            __pythonbrew_venv $argv
        case '*'
            eval $pythonbrew $argv
    end
end

set pythonbrew ""
function pythonbrew
    set pythonbrew $PY_PYTHONBREW
    __pythonbrew_run $argv
end

function pybrew
    pythonbrew $argv
end

function sudopybrew
    set pythonbrew "sudo PYTHONBREW_ROOT=$PATH_ROOT PATH=$PATH_PYTHONBREW:$PATH_WITHOUT_PYTHONBREW $PY_PYTHONBREW"
    __pythonbrew_run $argv
end

# main
__pythonbrew_set_current_path

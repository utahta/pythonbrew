_pybrew_complete()
{
  local commands
 
  COMPREPLY=()

  commands=`pythonbrew help |grep -e "^ .*: " | cut -d ":" -f 1 | tr -d " " |tr "\n" " "`
   
  if [ $COMP_CWORD -eq 1 ]; then
	
	_pybrew_compreply $commands
  
  elif [ $COMP_CWORD -eq 2 ]; then
	
	case "${COMP_WORDS[COMP_CWORD-1]}" in
		
		help)
			commands=$( echo $commands | sed -e "s/help//g" )
			_pybrew_compreply $commands
		;;
		
		install)
			_pybrew_available_versions
      _pybrew_compreply $available_versions
		;;
		use|switch|uninstall)
			_pybrew_installed_versions
			_pybrew_compreply $installed_versions
		;;
		venv)
			_pybrew_venv_commands
			_pybrew_compreply $venv_commands
		;;
		*)
		;;
	esac

  elif [ $COMP_CWORD -eq 3 ]; then

 	
	case "${COMP_WORDS[COMP_CWORD-1]}" in
		use|delete|rename|clone|print_activate)
			_pybrew_venv_current
			_pybrew_compreply $venv_current
		;;
			
		*)
		;;
	esac
  fi


  return 0
}

_pybrew_venv_commands()
{
	venv_commands=$( pythonbrew venv |head -n 1 | awk '{print $4}' | sed -e 's/\[\|\]//g' -e 's/|/ /g' )
}

_pybrew_venv_current()
{
	venv_current=$(pythonbrew venv list |sed -n -e '/\(*\)/,/Python/p'|sed -e '/Python/d')
}

_pybrew_available_versions()
{
	_pybrew_installed_regex
	_pybrew_known_versions

  if [ -n "$installed_regex" ];then
	  available_versions=$( echo $known_versions | sed -e "s/$installed_regex//g" )
  else 
    available_versions=$known_versions
  fi 

}

_pybrew_installed_versions()
{
	installed_versions=$( pythonbrew list |grep -v ^# | awk '{print $1}' )
}

_pybrew_installed_regex()
{
	_pybrew_installed_versions

  installed_regex=""
  if [ -n "$installed_versions" ];then
    installed_regex=$( echo $installed_versions |sed -e "s/\n\| /|/g" -e "s/|$//" -e "s/|/\\\|/g") 
  fi
}

_pybrew_known_versions()
{
	known_versions=$( pythonbrew list -k |grep -v ^# )
}

_pybrew_compreply()
{
	COMPREPLY=( $( compgen -W "$*" -- ${COMP_WORDS[COMP_CWORD]}) )
}

complete -F _pybrew_complete pythonbrew

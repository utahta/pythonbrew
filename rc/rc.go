package rc

import "io/ioutil"

//go:generate go-assets-builder -p rc -o assets.go rc.bash

type ShellType string

const (
	ShellTypeBash ShellType = "bash"
)

// Shell returns `run commands` for given type of shell
func Shell(s ShellType) string {
	switch s {
	case ShellTypeBash:
		return readAll("/rc.bash")
	default:
		return readAll("/rc.bash")
	}
}

func readAll(filename string) string {
	f, err := Assets.Open(filename)
	if err != nil {
		panic(err)
	}
	defer f.Close()

	b, err := ioutil.ReadAll(f)
	if err != nil {
		panic(err)
	}
	return string(b)
}

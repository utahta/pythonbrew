package subcmd

import (
	"fmt"
	"os"
	"path/filepath"
	"regexp"

	"github.com/blang/semver"
	"github.com/pkg/errors"
)

var (
	Version string

	reVersion = regexp.MustCompile(`\d+\.\d+\.\d+`)
)

type (
	// Command sub command interface
	Command interface {
		Name() string
		Summary() string
		Usage()
		Run([]string) error
	}

	// CommandRepository sub command repository interface
	CommandRepository interface {
		Find(string) (Command, error)
		Commands() []Command
	}

	repository struct {
		commands   []Command
		commandMap map[string]Command
	}
)

func Repository() CommandRepository {
	repo := &repository{
		commandMap: make(map[string]Command),
	}
	repo.commands = []Command{
		NewHelp(),
		NewInit(),
		NewInstall(),
		NewUninstall(),
		NewList(),
		NewSwitch(),
		NewUse(),
		NewOff(),
		NewVenv(),
		NewCleanup(),
		NewUpdate(),
	}
	for _, c := range repo.commands {
		repo.commandMap[c.Name()] = c
	}
	return repo
}

func (repo *repository) Find(name string) (Command, error) {
	c, ok := repo.commandMap[name]
	if !ok {
		return nil, errors.New("command is missing")
	}
	return c, nil
}

func (repo *repository) Commands() []Command {
	return repo.commands[:]
}

func writeEnvPython(filename string, installdir string) error {
	env := fmt.Sprintf(`PYTHONBREW_VERSION=%s
PYTHONBREW_VERSION_BIN=%s
PYTHONBREW_VERSION_LIB=%s
`, installdir, filepath.Join(installdir, "bin"), filepath.Join(installdir, "lib"))

	fp, err := os.Create(filename)
	if err != nil {
		return err
	}
	defer fp.Close()

	fp.WriteString(env)
	return nil
}

func semverVersion() semver.Version {
	v := Version
	if loc := reVersion.FindStringIndex(v); loc != nil && loc[0] > 0 {
		v = v[loc[0]:]
	}
	return semver.MustParse(v)
}

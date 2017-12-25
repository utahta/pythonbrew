package installer

import (
	"os/exec"
	"strings"

	"github.com/pkg/errors"
	"github.com/utahta/pythonbrew/log"
)

func commandRun(log log.Logger, cwd string, name string, args ...string) error {
	log.Verbosef("Run %s %s", name, strings.Join(args, " "))
	cmd := exec.Command(name, args...)
	cmd.Dir = cwd
	cmd.Stdout = log.Stdout()
	cmd.Stderr = log.Stderr()
	if err := cmd.Run(); err != nil {
		return errors.WithStack(err)
	}
	return nil
}

func commandOutput(name string, args ...string) (string, error) {
	cmd := exec.Command(name, args...)
	b, err := cmd.Output()
	if err != nil {
		return "", errors.WithStack(err)
	}
	return strings.TrimSpace(string(b)), nil
}

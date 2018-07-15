package installer

import (
	"fmt"
	"io"
	"os/exec"
	"strings"

	"github.com/pkg/errors"
	"github.com/utahta/go-cronowriter"
	"github.com/utahta/pythonbrew/path"
)

type (
	commandRunner struct {
		stdout io.Writer
		stderr io.Writer
	}
)

func newCommandRunner() *commandRunner {
	w := cronowriter.MustNew(path.Log())
	return &commandRunner{stdout: w, stderr: w}
}

func (c *commandRunner) EnableVerbose() {
	c.stdout = cronowriter.MustNew(path.Log(), cronowriter.WithStdout())
	c.stderr = cronowriter.MustNew(path.Log(), cronowriter.WithStderr())
}

func (c *commandRunner) Run(cwd string, name string, args ...string) error {
	fmt.Fprintf(c.stdout, "Run %s %s", name, strings.Join(args, " "))
	cmd := exec.Command(name, args...)
	cmd.Dir = cwd
	cmd.Stdout = c.stdout
	cmd.Stderr = c.stderr
	if err := cmd.Run(); err != nil {
		return errors.WithStack(err)
	}
	return nil
}

func (c *commandRunner) Output(name string, args ...string) (string, error) {
	cmd := exec.Command(name, args...)
	b, err := cmd.Output()
	if err != nil {
		return "", errors.WithStack(err)
	}
	return strings.TrimSpace(string(b)), nil
}

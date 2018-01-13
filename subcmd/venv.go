package subcmd

import (
	"flag"
	"fmt"
	"io/ioutil"
	"os"
	"os/exec"
	"path/filepath"
	"strings"

	"github.com/pkg/errors"
	"github.com/utahta/pythonbrew/flagset"
	"github.com/utahta/pythonbrew/log"
	"github.com/utahta/pythonbrew/path"
)

type (
	// Venv command
	Venv struct {
		flagSet *flag.FlagSet
		opts    VenvOptions
		log     log.Logger
	}

	// VenvOptions flag set
	VenvOptions struct {
		ShowHelp           bool
		Python             string
		SystemSitePackages bool
		List               bool
		Remove             bool
	}
)

// NewVenv returns Venv command
func NewVenv() *Venv {
	c := &Venv{log: log.NewLogger()}
	c.flagSet = flagset.New(c.Name(), "[OPTIONS] [DEST_DIR]")
	c.flagSet.BoolVar(&c.opts.ShowHelp, "h", false, "Show command usage")
	c.flagSet.StringVar(&c.opts.Python, "p", "", "Use a specific Python version")
	c.flagSet.BoolVar(&c.opts.SystemSitePackages, "g", false, "Give the virtual environment access to the global site-packages")
	c.flagSet.BoolVar(&c.opts.List, "l", false, "List all of the environments")
	c.flagSet.BoolVar(&c.opts.Remove, "rm", false, "Remove an environment")
	return c
}

// Name returns command name
func (c *Venv) Name() string {
	return "venv"
}

// Summary returns command summary
func (c *Venv) Summary() string {
	return "Manage environments (using virtualenv)"
}

// Usage shows command usage
func (c *Venv) Usage() {
	c.flagSet.Usage()
}

// Run runs venv command
func (c *Venv) Run(args []string) error {
	const tag = "venv.run"
	c.flagSet.Parse(args[1:])
	if c.opts.ShowHelp || len(args[1:]) == 0 {
		c.Usage()
		return nil
	}

	if c.opts.List {
		return errors.Wrap(c.runList(), tag)
	}
	if c.opts.Remove {
		return errors.Wrap(c.runRemove(), tag)
	}

	if c.flagSet.NArg() == 0 {
		c.log.Noticef("DEST_DIR argument required")
		c.Usage()
		return nil
	}
	name := c.flagSet.Arg(0)

	venv, err := c.findVirtualenvPath()
	if err != nil {
		cmd := exec.Command("pip", "install", "virtualenv")
		cmd.Stdout = os.Stdout
		cmd.Stderr = os.Stderr
		if err := cmd.Run(); err != nil {
			return errors.Wrap(err, tag)
		}

		venv, err = c.findVirtualenvPath()
		if err != nil {
			return errors.Wrap(err, tag)
		}
	}

	dir := filepath.Join(path.VenvsDir(), name)
	if _, err := os.Stat(dir); err != nil {
		// Create virtual environment if not exists
		var args []string
		if c.opts.Python != "" {
			pythonPath, err := c.findPythonPath()
			if err != nil {
				return errors.Wrap(err, tag)
			}
			args = append(args, "-p", pythonPath)
		}
		if c.opts.SystemSitePackages {
			args = append(args, "--system-site-packages")
		}
		args = append(args, dir)

		cmd := exec.Command(venv, args...)
		cmd.Stdout = os.Stdout
		cmd.Stderr = os.Stderr
		if err := cmd.Run(); err != nil {
			return errors.Wrap(err, tag)
		}
	}

	// activate code
	fp, err := os.Create(path.EnvVenv())
	if err != nil {
		return errors.Wrap(err, tag)
	}
	defer fp.Close()
	fp.WriteString(fmt.Sprintf(`source %s`, filepath.Join(dir, "bin", "activate")))

	c.log.Infof("Using %s environment (found in %s)", name, path.VenvsDir())
	c.log.Infof("To leave an environment, simply run deactivate")

	return nil
}

func (c *Venv) runList() error {
	fs, err := ioutil.ReadDir(path.VenvsDir())
	if err != nil {
		return errors.WithStack(err)
	}

	for _, f := range fs {
		c.log.Printf(f.Name())
	}
	return nil
}

func (c *Venv) runRemove() error {
	if c.flagSet.NArg() == 0 {
		c.log.Noticef("DEST_DIR argument required")
		c.Usage()
		return nil
	}

	name := c.flagSet.Arg(0)
	dir := filepath.Join(path.VenvsDir(), name)
	if _, err := os.Stat(dir); err != nil {
		c.log.Warnf("%s is not found", name)
		return nil
	}

	if err := os.RemoveAll(dir); err != nil {
		return errors.WithStack(err)
	}
	return nil
}

func (c *Venv) findVirtualenvPath() (string, error) {
	cmd := exec.Command("/usr/bin/env", "bash", "-c", "command -v virtualenv")
	b, err := cmd.Output()
	if err != nil {
		return "", errors.WithStack(err)
	}
	return strings.TrimSpace(string(b)), nil
}

func (c *Venv) findPythonPath() (string, error) {
	if c.opts.Python == "" {
		return "", errors.New("invalid argument")
	}

	if _, err := os.Stat(c.opts.Python); err == nil {
		return c.opts.Python, nil
	}

	filename := filepath.Join(path.InstallDir(), c.opts.Python, "bin", "python")
	if _, err := os.Stat(filename); err == nil {
		return filename, nil
	}

	return "", errors.New("Python is not found")
}

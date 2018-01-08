package subcmd

import (
	"flag"
	"os"
	"path/filepath"

	"github.com/pkg/errors"
	"github.com/utahta/pythonbrew/flagset"
	"github.com/utahta/pythonbrew/log"
	"github.com/utahta/pythonbrew/path"
)

type (
	// Uninstall command
	Uninstall struct {
		flagSet *flag.FlagSet
		opts    UninstallOptions
		log     log.Logger
	}

	// UninstallOptions flag set
	UninstallOptions struct {
		ShowHelp bool
	}
)

// NewUninstall returns Uninstall command
func NewUninstall() *Uninstall {
	c := &Uninstall{log: log.NewLogger()}
	c.flagSet = flagset.New(c.Name(), "[OPTIONS] VERSION")
	c.flagSet.BoolVar(&c.opts.ShowHelp, "h", false, "Show command usage")
	return c
}

// Name returns command name
func (c *Uninstall) Name() string {
	return "uninstall"
}

// Summary returns command summary
func (c *Uninstall) Summary() string {
	return "Uninstall specific Python versions"
}

// Usage shows command usage
func (c *Uninstall) Usage() {
	c.flagSet.Usage()
}

// Run runs uninstall command
func (c *Uninstall) Run(args []string) error {
	const tag = "uninstall.run"
	c.flagSet.Parse(args[1:])
	if c.opts.ShowHelp {
		c.Usage()
		return nil
	}

	if c.flagSet.NArg() == 0 {
		c.log.Noticef("VERSION argument required")
		c.Usage()
		return nil
	}

	for _, name := range c.flagSet.Args() {
		filename := filepath.Join(path.InstallDir(), name)
		if _, err := os.Stat(filename); err != nil {
			c.log.Warnf("%s is not installed", name)
			continue
		}

		if err := os.RemoveAll(filename); err != nil {
			return errors.Wrap(err, tag)
		}

		c.log.Infof("%s has been removed", name)
	}

	return nil
}

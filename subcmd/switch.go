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
	// Switch command
	Switch struct {
		flagSet *flag.FlagSet
		opts    SwitchOptions
		log     log.Logger
	}

	// SwitchOptions flag set
	SwitchOptions struct {
		ShowHelp bool
	}
)

// NewSwitch returns Switch command
func NewSwitch() *Switch {
	c := &Switch{log: log.NewLogger()}
	c.flagSet = flagset.New(c.Name(), "[OPTIONS] VERSION")
	c.flagSet.BoolVar(&c.opts.ShowHelp, "h", false, "Show command usage")
	return c
}

// Name returns command name
func (c *Switch) Name() string {
	return "switch"
}

// Summary returns command summary
func (c *Switch) Summary() string {
	return "Use a specific Python version permanently"
}

// Usage shows command usage
func (c *Switch) Usage() {
	c.flagSet.Usage()
}

// Run runs switch command
func (c *Switch) Run(args []string) error {
	const tag = "switch.run"
	c.flagSet.Parse(args[1:])
	if c.opts.ShowHelp {
		c.Usage()
		return nil
	}

	if c.flagSet.NArg() == 0 {
		c.log.Noticef("A version is missing")
		c.Usage()
		return nil
	}

	name := c.flagSet.Arg(0)
	dir := filepath.Join(path.InstallDir(), name)
	if _, err := os.Stat(dir); err != nil {
		c.log.Warnf("%s is not installed", name)
		return nil
	}

	if err := writeEnvPython(path.EnvPermanent(), dir); err != nil {
		return errors.Wrap(err, tag)
	}

	c.log.Infof("Switch to %s", name)

	return nil
}

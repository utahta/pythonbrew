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
	// Use command
	Use struct {
		flagSet *flag.FlagSet
		opts    UseOptions
		log     log.Logger
	}

	// UseOptions flag set
	UseOptions struct {
		ShowHelp bool
	}
)

// NewUse returns Use command
func NewUse() *Use {
	c := &Use{log: log.NewLogger()}
	c.flagSet = flagset.New(c.Name(), "[OPTIONS] VERSION")
	c.flagSet.BoolVar(&c.opts.ShowHelp, "h", false, "Show command usage")
	return c
}

// Name returns command name
func (c *Use) Name() string {
	return "use"
}

// Summary returns command summary
func (c *Use) Summary() string {
	return "Use a specific Python version in the current shell"
}

// Usage shows command usage
func (c *Use) Usage() {
	c.flagSet.Usage()
}

// Run runs use command
func (c *Use) Run(args []string) error {
	const tag = "use.run"
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

	if err := writeEnvPython(path.EnvTmp(), dir); err != nil {
		return errors.Wrap(err, tag)
	}

	c.log.Infof("Switch to %s in the current shell", name)

	return nil
}

package subcmd

import (
	"flag"
	"os"

	"github.com/pkg/errors"
	"github.com/utahta/pythonbrew/flagset"
	"github.com/utahta/pythonbrew/log"
	"github.com/utahta/pythonbrew/path"
)

type (
	// Off command
	Off struct {
		flagSet *flag.FlagSet
		opts    OffOptions
		log     log.Logger
	}

	// OffOptions flag set
	OffOptions struct {
		ShowHelp bool
	}
)

// NewOff returns Off command
func NewOff() *Off {
	c := &Off{log: log.NewLogger()}
	c.flagSet = flagset.New(c.Name(), "[OPTIONS]")
	c.flagSet.BoolVar(&c.opts.ShowHelp, "h", false, "Show command usage")
	return c
}

// Name returns command name
func (c *Off) Name() string {
	return "off"
}

// Summary returns command summary
func (c *Off) Summary() string {
	return "Disable pythonbrew"
}

// Usage shows command usage
func (c *Off) Usage() {
	c.flagSet.Usage()
}

// Run runs use command
func (c *Off) Run(args []string) error {
	const tag = "off.run"
	c.flagSet.Parse(args[1:])
	if c.opts.ShowHelp {
		c.Usage()
		return nil
	}

	fp, err := os.Create(path.EnvPermanent())
	if err != nil {
		return errors.Wrap(err, tag)
	}
	defer fp.Close()
	fp.WriteString("")

	return nil
}

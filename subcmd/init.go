package subcmd

import (
	"flag"
	"fmt"

	"github.com/pkg/errors"
	"github.com/utahta/pythonbrew/flagset"
	"github.com/utahta/pythonbrew/log"
	"github.com/utahta/pythonbrew/path"
	"github.com/utahta/pythonbrew/rc"
)

type (
	// Init command
	Init struct {
		flagSet *flag.FlagSet
		opts    InitOptions
		log     log.Logger
	}

	// InitOptions flag set
	InitOptions struct {
		ShowHelp  bool
		ShellType string
	}
)

// NewInit returns Init command
func NewInit() *Init {
	c := &Init{log: log.NewLogger()}
	c.flagSet = flagset.New(c.Name(), "[OPTIONS]")
	c.flagSet.BoolVar(&c.opts.ShowHelp, "h", false, "Show command usage")
	c.flagSet.StringVar(&c.opts.ShellType, "s", "bash", "Type of shell")
	return c
}

// Name returns command name
func (c *Init) Name() string {
	return "init"
}

// Summary returns command summary
func (c *Init) Summary() string {
	return "Please refer to README.md"
}

// Usage shows command usage
func (c *Init) Usage() {
	c.flagSet.Usage()
}

// Run runs init command
func (c *Init) Run(args []string) error {
	const tag = "init.run"
	c.flagSet.Parse(args[1:])
	if c.opts.ShowHelp {
		c.Usage()
		return nil
	}

	if err := path.MkdirAll(); err != nil {
		return errors.Wrap(err, tag)
	}

	fmt.Print(rc.Shell(rc.ShellType(c.opts.ShellType)))

	return nil
}

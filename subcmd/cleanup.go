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
	// Cleanup command
	Cleanup struct {
		flagSet *flag.FlagSet
		opts    CleanupOptions
		log     log.Logger
	}

	// CleanupOptions flag set
	CleanupOptions struct {
		ShowHelp bool
	}
)

// NewCleanup returns Cleanup command
func NewCleanup() *Cleanup {
	c := &Cleanup{log: log.NewLogger()}
	c.flagSet = flagset.New(c.Name(), "[OPTIONS]")
	c.flagSet.BoolVar(&c.opts.ShowHelp, "h", false, "Show command usage")
	return c
}

// Name returns command name
func (c *Cleanup) Name() string {
	return "cleanup"
}

// Summary returns command summary
func (c *Cleanup) Summary() string {
	return "Remove all cache"
}

// Usage shows command usage
func (c *Cleanup) Usage() {
	c.flagSet.Usage()
}

// Run runs cleanup command
func (c *Cleanup) Run(args []string) error {
	const tag = "cleanup.run"
	c.flagSet.Parse(args[1:])
	if c.opts.ShowHelp {
		c.Usage()
		return nil
	}

	if err := os.RemoveAll(path.CacheDir()); err != nil {
		return errors.Wrap(err, tag)
	}
	return nil
}

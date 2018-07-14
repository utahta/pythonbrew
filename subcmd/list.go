package subcmd

import (
	"flag"
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"

	"github.com/fatih/color"
	"github.com/pkg/errors"
	"github.com/utahta/pythonbrew/flagset"
	"github.com/utahta/pythonbrew/log"
	"github.com/utahta/pythonbrew/origin"
	"github.com/utahta/pythonbrew/path"
)

type (
	// List command
	List struct {
		flagSet *flag.FlagSet
		opts    ListOptions
		log     log.Logger
	}

	// ListOptions flag set
	ListOptions struct {
		ShowHelp         bool
		KnownInstallable bool
	}
)

// NewList returns List command
func NewList() *List {
	c := &List{log: log.NewLogger()}
	c.flagSet = flagset.New(c.Name(), "[OPTIONS]")
	c.flagSet.BoolVar(&c.opts.ShowHelp, "h", false, "Show command usage")
	c.flagSet.BoolVar(&c.opts.KnownInstallable, "k", false, "Show known installable versions")
	return c
}

// Name returns command name
func (c *List) Name() string {
	return "list"
}

// Summary returns command summary
func (c *List) Summary() string {
	return "List all installed or known installable Python versions"
}

// Usage shows command usage
func (c *List) Usage() {
	c.flagSet.Usage()
}

// Run runs cleanup command
func (c *List) Run(args []string) error {
	const tag = "list.run"
	c.flagSet.Parse(args[1:])
	if c.opts.ShowHelp {
		c.Usage()
		return nil
	}

	if c.opts.KnownInstallable {
		c.log.Printf("# Python")
		for _, v := range origin.KnownInstallablePythons() {
			c.log.Printf(v)
		}
	} else {
		current := os.Getenv("PYTHONBREW_VERSION")

		fs, err := ioutil.ReadDir(path.InstallDir())
		if err != nil {
			return errors.Wrap(err, tag)
		}

		for _, f := range fs {
			var name string
			if filepath.Join(path.InstallDir(), f.Name()) == current {
				name = color.New(color.FgYellow, color.BgBlack).Sprintf("%s", f.Name())
			} else {
				name = fmt.Sprintf("%s", f.Name())
			}
			c.log.Printf(name)
		}
	}

	return nil
}

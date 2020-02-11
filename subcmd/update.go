package subcmd

import (
	"flag"

	"github.com/pkg/errors"
	"github.com/rhysd/go-github-selfupdate/selfupdate"
	"github.com/utahta/pythonbrew/flagset"
	"github.com/utahta/pythonbrew/log"
)

type (
	// Update command
	Update struct {
		flagSet *flag.FlagSet
		opts    UpdateOptions
		log     log.Logger
	}

	// UpdateOptions flag set
	UpdateOptions struct {
		ShowHelp bool
	}
)

// NewUpdate returns Update command
func NewUpdate() *Update {
	c := &Update{log: log.NewLogger()}
	c.flagSet = flagset.New(c.Name(), "[OPTIONS]")
	c.flagSet.BoolVar(&c.opts.ShowHelp, "h", false, "Show command usage")
	return c
}

// Name returns command name
func (c *Update) Name() string {
	return "update"
}

// Summary returns command summary
func (c *Update) Summary() string {
	return "Update pythonbrew to the latest version"
}

// Usage shows command usage
func (c *Update) Usage() {
	c.flagSet.Usage()
}

// Run runs update command
func (c *Update) Run(args []string) error {
	const tag = "update.run"
	c.flagSet.Parse(args[1:])
	if c.opts.ShowHelp {
		c.Usage()
		return nil
	}

	previous := semverVersion()
	latest, err := selfupdate.UpdateSelf(previous, "utahta/pythonbrew")
	if err != nil {
		return errors.Wrap(err, tag)
	}

	if previous.Equals(latest.Version) {
		c.log.Printf("Current binary is the latest version")
	} else {
		c.log.Infof("Update successfully done to %s", latest.Version)
		c.log.Infof("Release note:")
		c.log.Infof(latest.ReleaseNotes)
	}

	return nil
}

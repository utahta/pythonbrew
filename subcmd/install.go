package subcmd

import (
	"flag"
	"os"

	"github.com/pkg/errors"
	"github.com/utahta/pythonbrew/flagset"
	"github.com/utahta/pythonbrew/installer"
	"github.com/utahta/pythonbrew/log"
	"github.com/utahta/pythonbrew/origin"
	"github.com/utahta/pythonbrew/path"
)

type (
	// Install command
	Install struct {
		flagSet *flag.FlagSet
		opts    InstallOptions
		log     log.Logger
	}

	// InstallOptions flag set
	InstallOptions struct {
		ShowHelp      bool
		Force         bool
		Verbose       bool
		ConfigureOpts []string
		NoEnsurepip   bool
		NoSymlink     bool
		Jobs          int
	}
)

// NewInstall returns Install command
func NewInstall() *Install {
	c := &Install{log: log.NewLogger()}
	c.flagSet = flagset.New(c.Name(), "[OPTIONS] {VERSION | URL}")
	c.flagSet.BoolVar(&c.opts.ShowHelp, "h", false, "Show command usage")
	c.flagSet.BoolVar(&c.opts.Force, "f", false, "Reinstall a specific Python version")
	c.flagSet.BoolVar(&c.opts.Verbose, "v", false, "Show logs about the results of installing Python")
	c.flagSet.Var(flagset.NewStringsValue(nil, &c.opts.ConfigureOpts), "C", "Pass options to configure (e.g. -C foo -C bar)")
	c.flagSet.BoolVar(&c.opts.NoEnsurepip, "no-ensurepip", false, "Skip installing pip")
	c.flagSet.BoolVar(&c.opts.NoSymlink, "no-symlink", false, "Skip creating symlink")
	c.flagSet.IntVar(&c.opts.Jobs, "j", 1, "Number of job slots (for build)")
	return c
}

// Name returns command name
func (c *Install) Name() string {
	return "install"
}

// Summary returns command summary
func (c *Install) Summary() string {
	return "Install specific Python versions"
}

// Usage shows command usage
func (c *Install) Usage() {
	c.flagSet.Usage()
}

// Run runs install command
func (c *Install) Run(args []string) error {
	const tag = "install.run"
	c.flagSet.Parse(args[1:])
	if c.opts.ShowHelp {
		c.Usage()
		return nil
	}

	pkgs, err := origin.FindPackages(c.flagSet.Args())
	if err != nil {
		return errors.Wrap(err, tag)
	}
	if len(pkgs) == 0 {
		c.log.Noticef("VERSION argument required")
		c.Usage()
		return nil
	}

	if err := path.MkdirAll(); err != nil {
		return errors.Wrap(err, tag)
	}

	for _, pkg := range pkgs {
		if c.opts.Force {
			if err := os.RemoveAll(pkg.InstallDir()); err != nil {
				return errors.Wrap(err, tag)
			}
		} else {
			if _, err := os.Stat(pkg.InstallDir()); err == nil {
				c.log.Infof("%s is already installed", pkg.Name())
				continue
			}
		}

		var err error
		switch pkg.Type() {
		case origin.PackageTypePython:
			i := installer.NewPython()
			err = i.Install(pkg, installer.PythonOptions{
				Force:         c.opts.Force,
				Verbose:       c.opts.Verbose,
				ConfigureOpts: c.opts.ConfigureOpts,
				NoEnsurepip:   c.opts.NoEnsurepip,
				NoSymlink:     c.opts.NoSymlink,
				Jobs:          c.opts.Jobs,
			})
		default:
			err = errors.Errorf("%v: unknown package %#v", tag, pkg)
		}

		if err != nil {
			return errors.Wrap(err, tag)
		}
	}
	return nil
}

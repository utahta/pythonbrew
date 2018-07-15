package installer

import (
	"fmt"
	"net/url"
	"os"
	"path/filepath"
	"runtime"
	"strconv"
	"strings"

	"github.com/pkg/errors"
	"github.com/utahta/pythonbrew/log"
	"github.com/utahta/pythonbrew/origin"
	"github.com/utahta/pythonbrew/path"
)

type (
	// Python installer
	Python struct {
		downloader Downloader
		extractor  Extractor
		cmd        *commandRunner
		log        log.Logger
	}

	// PythonOptions represents Python installer options
	PythonOptions struct {
		Force         bool
		Verbose       bool
		ConfigureOpts []string
		NoEnsurepip   bool
		NoSymlink     bool
		Jobs          int
	}
)

// NewPython returns Python installer
func NewPython() *Python {
	return &Python{
		downloader: NewDownloader(),
		extractor:  NewExtractor(),
		cmd:        newCommandRunner(),
		log:        log.NewFileLogger(),
	}
}

// Install installs given Python version
func (p *Python) Install(pkg origin.Package, o PythonOptions) error {
	const tag = "installer.python"

	if o.Verbose {
		p.cmd.EnableVerbose()
	}
	p.log.Noticef("Logging %s", path.Log())

	if err := p.download(pkg); err != nil {
		return errors.Wrap(err, tag)
	}

	if err := p.extract(pkg); err != nil {
		return errors.Wrap(err, tag)
	}

	if err := p.build(pkg, o); err != nil {
		return errors.Wrap(err, tag)
	}

	if err := p.install(pkg, o); err != nil {
		return errors.Wrap(err, tag)
	}

	if err := p.ensurePip(pkg, o); err != nil {
		return errors.Wrap(err, tag)
	}

	if err := p.symlink(pkg, o); err != nil {
		return errors.Wrap(err, tag)
	}

	p.log.Infof("")
	p.log.Infof("%s has been successfully installed", pkg.Name())
	p.log.Infof("Run the following command to switch to %s", pkg.Name())
	p.log.Infof("  pythonbrew switch %s", pkg.Version().String())

	return nil
}

func (p *Python) download(pkg origin.Package) error {
	if _, err := os.Stat(pkg.Filename()); err == nil {
		p.log.Infof("Using cached %s", pkg.Filename())
		return nil
	}

	if err := p.downloader.Download(pkg.URL(), pkg.Filename()); err != nil {
		return err
	}
	return nil
}

func (p *Python) extract(pkg origin.Package) error {
	if err := os.RemoveAll(pkg.BuildDir()); err != nil {
		return errors.WithStack(err)
	}

	if err := p.extractor.Extract(path.BuildDir(), pkg.Filename()); err != nil {
		return err
	}
	return nil
}

func (p *Python) build(pkg origin.Package, o PythonOptions) error {
	p.log.Infof("Building %s", pkg.BuildDir())

	opts, err := p.buildConfigureOptions(pkg, o)
	if err != nil {
		return err
	}
	if err := p.cmd.Run(pkg.BuildDir(), "./configure", opts...); err != nil {
		return err
	}

	opts = opts[:0]
	if o.Jobs > 0 {
		opts = append(opts, "-j", strconv.Itoa(o.Jobs))
	}
	if err := p.cmd.Run(pkg.BuildDir(), "make", opts...); err != nil {
		return err
	}
	return nil
}

func (p *Python) buildConfigureOptions(pkg origin.Package, o PythonOptions) ([]string, error) {
	var opts []string
	opts = append(opts, fmt.Sprintf("--prefix=%s", pkg.InstallDir()))

	if pkg.Version().GreaterThanString("3.1") {
		opts = append(opts, "--with-computed-gotos")
	}

	if (pkg.Version().Major() == 3 && pkg.Version().GreaterThanString("3.4")) ||
		(pkg.Version().Major() == 2 && pkg.Version().GreaterThanString("2.7.9")) {
		opts = append(opts, "--without-ensurepip")
	}

	var (
		cflags  []string
		ldflags []string
	)

	// for macOS
	if runtime.GOOS == "darwin" {
		dir, err := p.cmd.Output("brew", "--prefix", "openssl")
		if err == nil {
			p.log.Noticef("Using homebrew openssl (%s)", dir)
			cflags = append(cflags, fmt.Sprintf("-I%s/include", dir))
			ldflags = append(ldflags, fmt.Sprintf("-L%s/lib", dir))
		}
		dir, err = p.cmd.Output("brew", "--prefix", "readline")
		if err == nil {
			p.log.Noticef("Using homebrew readline (%s)", dir)
			cflags = append(cflags, fmt.Sprintf("-I%s/include", dir))
			ldflags = append(ldflags, fmt.Sprintf("-L%s/lib", dir))
		}
	}

	if len(cflags) > 0 {
		opts = append(opts, fmt.Sprintf("CFLAGS=%s", strings.Join(cflags, " ")))
	}
	if len(ldflags) > 0 {
		opts = append(opts, fmt.Sprintf("LDFLAGS=%s", strings.Join(ldflags, " ")))
	}

	if len(o.ConfigureOpts) > 0 {
		opts = append(opts, o.ConfigureOpts...)
	}
	return opts, nil
}

func (p *Python) install(pkg origin.Package, o PythonOptions) error {
	p.log.Infof("Installing %s into %s", pkg.Name(), pkg.InstallDir())

	if err := os.RemoveAll(pkg.InstallDir()); err != nil {
		return errors.WithStack(err)
	}

	if err := p.cmd.Run(pkg.BuildDir(), "make", "install"); err != nil {
		return err
	}
	return nil
}

func (p *Python) ensurePip(pkg origin.Package, o PythonOptions) error {
	if o.NoEnsurepip {
		p.log.Infof("Skip ensuring pip")
		return nil
	}
	if pkg.Version().Major() == 3 && pkg.Version().LessThanString("3.2") {
		p.log.Warnf("Skip ensuring pip. Python 3.2 or later is required")
		return nil
	}
	if pkg.Version().Major() == 2 && pkg.Version().LessThanString("2.7") {
		p.log.Warnf("Skip ensuring pip. Python 2.7 or later is required")
		return nil
	}

	pipurl := "https://bootstrap.pypa.io/get-pip.py"
	pipfile := path.PipPy()
	if pkg.Version().Major() == 3 && pkg.Version().Minor() == 2 {
		pipfile = path.PipPy32()
		pipurl = "https://bootstrap.pypa.io/3.2/get-pip.py"
	}
	p.log.Infof("Ensuring pip")

	if _, err := os.Stat(pipfile); err == nil {
		p.log.Infof("Using cached %s", pipfile)
	} else {
		u, err := url.Parse(pipurl)
		if err != nil {
			return errors.WithStack(err)
		}
		if err := p.downloader.Download(u, pipfile); err != nil {
			return err
		}
	}

	name := filepath.Join("bin", fmt.Sprintf("python%d.%d", pkg.Version().Major(), pkg.Version().Minor()))
	if err := p.cmd.Run(pkg.InstallDir(), name, pipfile); err != nil {
		return err
	}
	return nil
}

func (p *Python) symlink(pkg origin.Package, o PythonOptions) error {
	if o.NoSymlink {
		p.log.Infof("Skip creating symlink")
		return nil
	}

	names := []string{
		"python",
		"pip",
		"pydoc",
	}
	for _, name := range names {
		filename := filepath.Join(pkg.InstallDir(), "bin", name)

		// create symlink if `name` not found
		if _, err := os.Stat(filename); err != nil {
			oldname := fmt.Sprintf("%s%d.%d", name, pkg.Version().Major(), pkg.Version().Minor())
			if err := os.Symlink(oldname, filename); err != nil {
				p.log.Errorf("failed to create %s symlink err:%v", name, err)
				// go on
			}
		}
	}
	return nil
}

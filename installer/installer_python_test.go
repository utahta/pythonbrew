// +build e2e

package installer_test

import (
	"os"
	"runtime"
	"testing"

	"github.com/utahta/pythonbrew/installer"
	"github.com/utahta/pythonbrew/origin"
	"github.com/utahta/pythonbrew/path"
)

func TestPython_Install(t *testing.T) {
	os.Setenv(path.OSEnvPythonbrewRoot, path.TempDir())
	os.Setenv(path.OSEnvPythonbrewHome, path.TempDir())

	if err := path.MkdirAll(); err != nil {
		t.Fatal(err)
	}

	testcases := []struct {
		version string
	}{
		{"3.6.4"},
		{"https://www.python.org/ftp/python/3.7.0/Python-3.7.0b1.tgz"},
	}

	for _, testcase := range testcases {
		pkg, err := origin.FindPackage(testcase.version)
		if err != nil {
			t.Fatal(err)
		}

		p := installer.NewPython()
		if err := p.Install(pkg, installer.PythonOptions{Jobs: runtime.NumCPU()}); err != nil {
			t.Fatal(err)
		}
	}
}

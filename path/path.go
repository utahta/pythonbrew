package path

import (
	"io/ioutil"
	"os"
	"path/filepath"
	"sync"

	"github.com/pkg/errors"
)

const (
	OSEnvPythonbrewRoot = "PYTHONBREW_ROOT"
	OSEnvPythonbrewHome = "PYTHONBREW_HOME"
)

var (
	mux     sync.Mutex
	tempDir string
)

// RootDir returns root directory path (system-wide)
func RootDir() string {
	v := os.Getenv(OSEnvPythonbrewRoot)
	if v == "" {
		v = filepath.Join(os.Getenv("HOME"), ".pythonbrew")
	}
	return v
}

// HomeDir returns home directory path
func HomeDir() string {
	v := os.Getenv(OSEnvPythonbrewHome)
	if v == "" {
		v = filepath.Join(os.Getenv("HOME"), ".pythonbrew")
	}
	return v
}

// TempDir returns temporary directory
func TempDir() string {
	mux.Lock()
	defer mux.Unlock()

	d, err := ioutil.TempDir("", "pythonbrew")
	if err != nil {
		panic(err)
	}
	tempDir = d
	return tempDir
}

// InstallDir returns install directory path
func InstallDir() string {
	return filepath.Join(RootDir(), "versions")
}

// CacheDir returns cache directory path
func CacheDir() string {
	return filepath.Join(RootDir(), "cache")
}

// BuildDir returns build directory path
func BuildDir() string {
	return filepath.Join(CacheDir(), "build")
}

// EnvDir returns env directory path
func EnvDir() string {
	return filepath.Join(HomeDir(), "env")
}

// VenvsDir returns venv directory path
func VenvsDir() string {
	return filepath.Join(HomeDir(), "venvs")
}

// Log returns log file path
func Log() string {
	return filepath.Join(TempDir(), "pythonbrew.log")
}

// PipPy32 returns pip installer file path (for Python-3.2)
func PipPy32() string {
	return filepath.Join(CacheDir(), "get-pip-32.py")
}

// PipPy returns pip installer file path
func PipPy() string {
	return filepath.Join(CacheDir(), "get-pip.py")
}

// EnvTmp returns temporary environment file path
func EnvTmp() string {
	return filepath.Join(EnvDir(), "tmp")
}

// EnvPermanent returns permanently environment file path
func EnvPermanent() string {
	return filepath.Join(EnvDir(), "permanent")
}

// EnvVenv returns venv run command file path
func EnvVenv() string {
	return filepath.Join(EnvDir(), "venv")
}

// MkdirAll makes all directories
func MkdirAll() error {
	dirs := []string{
		CacheDir(),
		BuildDir(),
		InstallDir(),
		EnvDir(),
		VenvsDir(),
	}
	for _, dir := range dirs {
		if err := os.MkdirAll(dir, os.ModePerm); err != nil {
			return errors.Wrap(err, dir)
		}
	}
	return nil
}

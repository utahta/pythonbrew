package origin

import (
	"net/url"
	"strings"

	"github.com/pkg/errors"
)

type (
	// Package installation interface
	Package interface {
		Type() PackageType
		URL() *url.URL
		Name() string
		Filename() string
		BuildDir() string
		InstallDir() string
		Version() *Version
	}

	// PackageType type
	PackageType string

	// SortablePackages implements sort interface
	SortablePackages []Package
)

const (
	PackageTypePython PackageType = "python"
)

func (p SortablePackages) Len() int {
	return len(p)
}

func (p SortablePackages) Less(i, j int) bool {
	return p[i].Version().LessThan(p[j].Version())
}

func (p SortablePackages) Swap(i, j int) {
	p[i], p[j] = p[j], p[i]
}

// FindPackage returns installation package given version
func FindPackage(v string) (Package, error) {
	if strings.HasPrefix(v, "http://www.python.org") || strings.HasPrefix(v, "https://www.python.org") {
		return NewPythonPackage(v), nil
	}

	if p, ok := pythonPackages[v]; ok {
		return p, nil
	}
	return nil, errors.Errorf("missing package %v", v)
}

// FindPackages returns installation packages given versions
func FindPackages(vs []string) ([]Package, error) {
	pkgs := make([]Package, 0, len(vs))
	for _, v := range vs {
		pkg, err := FindPackage(v)
		if err != nil {
			return nil, err
		}
		pkgs = append(pkgs, pkg)
	}
	return pkgs, nil
}

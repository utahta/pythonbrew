package origin

import (
	"net/url"
	"path/filepath"
	"sort"
	"strings"

	"github.com/utahta/pythonbrew/path"
)

type (
	pythonPackage struct {
		url        *url.URL
		name       string
		filename   string
		buildDir   string
		installDir string
		version    *Version
	}
)

// refs EOL https://devguide.python.org/#branchstatus
var pythonPackages = map[string]Package{
	"2.7":    NewPythonPackage("https://www.python.org/ftp/python/2.7/Python-2.7.tgz#35f56b092ecf39a6bd59d64f142aae0f"),
	"2.7.1":  NewPythonPackage("https://www.python.org/ftp/python/2.7.1/Python-2.7.1.tgz#15ed56733655e3fab785e49a7278d2fb"),
	"2.7.2":  NewPythonPackage("https://www.python.org/ftp/python/2.7.2/Python-2.7.2.tgz#0ddfe265f1b3d0a8c2459f5bf66894c7"),
	"2.7.3":  NewPythonPackage("https://www.python.org/ftp/python/2.7.3/Python-2.7.3.tgz#2cf641732ac23b18d139be077bd906cd"),
	"2.7.4":  NewPythonPackage("https://www.python.org/ftp/python/2.7.4/Python-2.7.4.tgz#592603cfaf4490a980e93ecb92bde44a"),
	"2.7.5":  NewPythonPackage("https://www.python.org/ftp/python/2.7.5/Python-2.7.5.tgz#b4f01a1d0ba0b46b05c73b2ac909b1df"),
	"2.7.6":  NewPythonPackage("https://www.python.org/ftp/python/2.7.6/Python-2.7.6.tgz#1d8728eb0dfcac72a0fd99c17ec7f386"),
	"2.7.7":  NewPythonPackage("https://www.python.org/ftp/python/2.7.7/Python-2.7.7.tgz#cf842800b67841d64e7fb3cd8acb5663"),
	"2.7.8":  NewPythonPackage("https://www.python.org/ftp/python/2.7.8/Python-2.7.8.tgz#d4bca0159acb0b44a781292b5231936f"),
	"2.7.9":  NewPythonPackage("https://www.python.org/ftp/python/2.7.9/Python-2.7.9.tgz#5eebcaa0030dc4061156d3429657fb83"),
	"2.7.10": NewPythonPackage("https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tgz#d7547558fd673bd9d38e2108c6b42521"),
	"2.7.11": NewPythonPackage("https://www.python.org/ftp/python/2.7.11/Python-2.7.11.tgz#6b6076ec9e93f05dd63e47eb9c15728b"),
	"2.7.12": NewPythonPackage("https://www.python.org/ftp/python/2.7.12/Python-2.7.12.tgz#88d61f82e3616a4be952828b3694109d"),
	"2.7.13": NewPythonPackage("https://www.python.org/ftp/python/2.7.13/Python-2.7.13.tgz#17add4bf0ad0ec2f08e0cae6d205c700"),
	"2.7.14": NewPythonPackage("https://www.python.org/ftp/python/2.7.14/Python-2.7.14.tgz#cee2e4b33ad3750da77b2e85f2f8b724"),

	"3.2":   NewPythonPackage("https://www.python.org/ftp/python/3.2/Python-3.2.tgz#5efe838a7878b170f6728d7e5d7517af"),
	"3.2.1": NewPythonPackage("https://www.python.org/ftp/python/3.2.1/Python-3.2.1.tgz#6c2aa3481cadb7bdf74e625fffc352b2"),
	"3.2.2": NewPythonPackage("https://www.python.org/ftp/python/3.2.2/Python-3.2.2.tgz#3c63a6d97333f4da35976b6a0755eb67"),
	"3.2.3": NewPythonPackage("https://www.python.org/ftp/python/3.2.3/Python-3.2.3.tgz#dcf3a738e7028f1deb41b180bf0e2cbc"),
	"3.2.4": NewPythonPackage("https://www.python.org/ftp/python/3.2.4/Python-3.2.4.tgz#3af05758d0bc2b1a27249e8d622c3e91"),
	"3.2.5": NewPythonPackage("https://www.python.org/ftp/python/3.2.5/Python-3.2.5.tgz#ed8d5529d2aebc36b53f4e0a0c9e6728"),
	"3.2.6": NewPythonPackage("https://www.python.org/ftp/python/3.2.6/Python-3.2.6.tgz#23815d82ae706e9b781ca65865353d39"),

	"3.3.0": NewPythonPackage("https://www.python.org/ftp/python/3.3.0/Python-3.3.0.tgz#198a64f7a04d1d5e95ce2782d5fd8254"),
	"3.3.1": NewPythonPackage("https://www.python.org/ftp/python/3.3.1/Python-3.3.1.tgz#c19bfd6ea252b61779a4f2996fb3b330"),
	"3.3.2": NewPythonPackage("https://www.python.org/ftp/python/3.3.2/Python-3.3.2.tgz#0a2ea57f6184baf45b150aee53c0c8da"),
	"3.3.3": NewPythonPackage("https://www.python.org/ftp/python/3.3.3/Python-3.3.3.tgz#831d59212568dc12c95df222865d3441"),
	"3.3.4": NewPythonPackage("https://www.python.org/ftp/python/3.3.4/Python-3.3.4.tgz#9f7df0dde690132c63b1dd2b640ed3a6"),
	"3.3.5": NewPythonPackage("https://www.python.org/ftp/python/3.3.5/Python-3.3.5.tgz#803a75927f8f241ca78633890c798021"),
	"3.3.6": NewPythonPackage("https://www.python.org/ftp/python/3.3.6/Python-3.3.6.tgz#cdb3cd08f96f074b3f3994ccb51063e9"),
	"3.3.7": NewPythonPackage("https://www.python.org/ftp/python/3.3.7/Python-3.3.7.tgz#c54f93b012320871e6cbd0902ecb5769"),

	"3.4.0": NewPythonPackage("https://www.python.org/ftp/python/3.4.0/Python-3.4.0.tgz#3ca973eb72bb06ed5cadde0e28eaaaca"),
	"3.4.1": NewPythonPackage("https://www.python.org/ftp/python/3.4.1/Python-3.4.1.tgz#26695450087f8587b26d0b6a63844af5"),
	"3.4.2": NewPythonPackage("https://www.python.org/ftp/python/3.4.2/Python-3.4.2.tgz#5566bc7e1fdf6bed45f9a750d5f80fc2"),
	"3.4.3": NewPythonPackage("https://www.python.org/ftp/python/3.4.3/Python-3.4.3.tgz#4281ff86778db65892c05151d5de738d"),
	"3.4.4": NewPythonPackage("https://www.python.org/ftp/python/3.4.4/Python-3.4.4.tgz#e80a0c1c71763ff6b5a81f8cc9bb3d50"),
	"3.4.5": NewPythonPackage("https://www.python.org/ftp/python/3.4.5/Python-3.4.5.tgz#5f2ef90b1adef35a64df14d4bb7af733"),
	"3.4.6": NewPythonPackage("https://www.python.org/ftp/python/3.4.6/Python-3.4.6.tgz#74a7cbe1bd9652013ae6087ef346b9da"),
	"3.4.7": NewPythonPackage("https://www.python.org/ftp/python/3.4.7/Python-3.4.7.tgz#47bc789829ca7fc06eaa46588a261624"),

	"3.5.0": NewPythonPackage("https://www.python.org/ftp/python/3.5.0/Python-3.5.0.tgz#a56c0c0b45d75a0ec9c6dee933c41c36"),
	"3.5.1": NewPythonPackage("https://www.python.org/ftp/python/3.5.1/Python-3.5.1.tgz#be78e48cdfc1a7ad90efff146dce6cfe"),
	"3.5.2": NewPythonPackage("https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz#3fe8434643a78630c61c6464fe2e7e72"),
	"3.5.3": NewPythonPackage("https://www.python.org/ftp/python/3.5.3/Python-3.5.3.tgz#6192f0e45f02575590760e68c621a488"),
	"3.5.4": NewPythonPackage("https://www.python.org/ftp/python/3.5.4/Python-3.5.4.tgz#2ed4802b7a2a7e40d2e797272bf388ec"),

	"3.6.0": NewPythonPackage("https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tgz#3f7062ccf8be76491884d0e47ac8b251"),
	"3.6.1": NewPythonPackage("https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tgz#2d0fc9f3a5940707590e07f03ecb08b9"),
	"3.6.2": NewPythonPackage("https://www.python.org/ftp/python/3.6.2/Python-3.6.2.tgz#e1a36bfffdd1d3a780b1825daf16e56c"),
	"3.6.3": NewPythonPackage("https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tgz#e9180c69ed9a878a4a8a3ab221e32fa9"),
	"3.6.4": NewPythonPackage("https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tgz#9de6494314ea199e3633211696735f65"),
}

func (p *pythonPackage) Type() PackageType {
	return PackageTypePython
}

func (p *pythonPackage) URL() *url.URL {
	return p.url
}

// Name returns name like x.x.x
func (p *pythonPackage) Name() string {
	return p.name
}

// Filename returns filename like /path/to/Python-x.x.x.tgz
func (p *pythonPackage) Filename() string {
	return p.filename
}

// BuildDir returns build dir like /path/to/Python-x.x.x
func (p *pythonPackage) BuildDir() string {
	return p.buildDir
}

// InstallDir returns install dir like /path/to/x.x.x
func (p *pythonPackage) InstallDir() string {
	return p.installDir
}

func (p *pythonPackage) Version() *Version {
	return p.version
}

func NewPythonPackage(rawurl string) *pythonPackage {
	u, err := url.Parse(rawurl)
	if err != nil {
		panic(err)
	}
	p := &pythonPackage{}
	p.url = u
	basenameExt := filepath.Base(u.Path)                                  // expect Python-x.x.x.tgz
	basename := strings.TrimRight(basenameExt, filepath.Ext(basenameExt)) // expect Python-x.x.x
	p.name = strings.TrimLeft(basename, "Python-")                        // expect x.x.x

	v, err := ParseVersion(p.name)
	if err != nil {
		panic(err)
	}
	p.version = v
	p.filename = filepath.Join(path.CacheDir(), basenameExt)
	p.buildDir = filepath.Join(path.BuildDir(), basename)
	p.installDir = filepath.Join(path.InstallDir(), p.name)

	return p
}

// KnownInstallablePythons returns list all known installable pythons
func KnownInstallablePythons() []string {
	var pkgs SortablePackages
	for _, pkg := range pythonPackages {
		pkgs = append(pkgs, pkg)
	}
	sort.Sort(pkgs)

	names := make([]string, len(pkgs))
	for i, v := range pkgs {
		names[i] = v.Name()
	}
	return names
}

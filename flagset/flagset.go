package flagset

import (
	"flag"
	"fmt"
	"strings"
)

// New returns flag.Flagset
func New(name string, usage string) *flag.FlagSet {
	f := flag.NewFlagSet(name, flag.ExitOnError)
	f.Usage = func() {
		fmt.Printf("Usage: pythonbrew %s %s\n", name, usage)
		f.PrintDefaults()
	}
	return f
}

// string array flag.Value
type stringsValue []string

// NewStringsValue returns stringsValue that implemented flag.Value
func NewStringsValue(val []string, p *[]string) *stringsValue {
	*p = val
	return (*stringsValue)(p)
}

func (s *stringsValue) Set(val string) error {
	*s = append(*s, val)
	return nil
}

func (s *stringsValue) String() string {
	return strings.Join(*s, " ")
}

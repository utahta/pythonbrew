package log

import (
	"fmt"
	"io"
	"io/ioutil"

	"github.com/fatih/color"
	"github.com/mattn/go-colorable"
	"github.com/utahta/go-cronowriter"
	"github.com/utahta/pythonbrew/path"
)

type (
	// Logger is a interface that output log.
	Logger interface {
		Progressf(format string, args ...interface{})
		Printf(format string, args ...interface{})
		Infof(format string, args ...interface{})
		Noticef(format string, args ...interface{})
		Warnf(format string, args ...interface{})
		Errorf(format string, args ...interface{})
		Debugf(format string, args ...interface{})
	}

	logger struct {
		w io.Writer
	}
)

var (
	colorableStdout = colorable.NewColorableStdout()
	colorableStderr = colorable.NewColorableStderr()
)

// NewLogger returns a logger
func NewLogger() Logger {
	return &logger{
		w: ioutil.Discard,
	}
}

// NewFileLogger returns a logger with file writer
func NewFileLogger() Logger {
	return &logger{
		w: cronowriter.MustNew(path.Log()),
	}
}

// Progressf is a function to standard output progressive.
func (l *logger) Progressf(format string, args ...interface{}) {
	fmt.Fprintf(colorableStdout, "\r\033[K%s", color.GreenString(format, args...))
}

// Printf is a function to standard output.
func (l *logger) Printf(format string, args ...interface{}) {
	fmt.Fprintln(colorableStdout, fmt.Sprintf(format, args...))
}

func (l *logger) Infof(format string, args ...interface{}) {
	s := fmt.Sprintf(format, args...)
	fmt.Fprintln(colorableStdout, color.GreenString(s))
	fmt.Fprintln(l.w, s)
}

func (l *logger) Noticef(format string, args ...interface{}) {
	s := fmt.Sprintf(format, args...)
	fmt.Fprintln(colorableStdout, color.YellowString(s))
	fmt.Fprintln(l.w, s)
}

func (l *logger) Warnf(format string, args ...interface{}) {
	s := fmt.Sprintf(format, args...)
	fmt.Fprintln(colorableStdout, color.YellowString(s))
	fmt.Fprintln(l.w, s)
}

func (l *logger) Errorf(format string, args ...interface{}) {
	s := fmt.Sprintf(format, args...)
	fmt.Fprintln(colorableStderr, color.RedString(s))
	fmt.Fprintln(l.w, s)
}

func (l *logger) Debugf(format string, args ...interface{}) {
	s := fmt.Sprintf(format, args...)
	fmt.Fprintln(l.w, s)
}

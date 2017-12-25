package log

import (
	"fmt"
	"io"
	"os"

	"github.com/fatih/color"
	"github.com/mattn/go-colorable"
	"github.com/utahta/go-cronowriter"
	"github.com/utahta/pythonbrew/path"
)

type (
	// Logger output log interface
	Logger interface {
		Progressf(format string, args ...interface{})
		Printf(format string, args ...interface{})
		Infof(format string, args ...interface{})
		Noticef(format string, args ...interface{})
		Warnf(format string, args ...interface{})
		Errorf(format string, args ...interface{})
		Verbosef(format string, args ...interface{})
		Path() string
		Stdout() io.Writer
		Stderr() io.Writer
	}

	logger struct {
		fw *cronowriter.CronoWriter
	}

	verboseLogger struct {
		Logger
		stdout io.Writer
		stderr io.Writer
	}
)

// NewLogger returns logger
func NewLogger() Logger {
	return &logger{}
}

// NewFileLogger returns logger with file writer
func NewFileLogger() Logger {
	return &logger{
		fw: cronowriter.MustNew(path.Log(), cronowriter.WithInit()),
	}
}

// NewVerboseLogger returns verbose logger
func NewVerboseLogger() Logger {
	return &verboseLogger{
		Logger: NewFileLogger(),
		stdout: cronowriter.MustNew(path.Log(), cronowriter.WithInit(), cronowriter.WithStdout()),
		stderr: cronowriter.MustNew(path.Log(), cronowriter.WithInit(), cronowriter.WithStderr()),
	}
}

func (l *logger) Progressf(format string, args ...interface{}) {
	fmt.Fprintf(colorable.NewColorableStdout(), "\r\033[K%s", color.GreenString(format, args...))
}

func (l *logger) Printf(format string, args ...interface{}) {
	fmt.Fprintln(os.Stdout, fmt.Sprintf(format, args...))
}

func (l *logger) Infof(format string, args ...interface{}) {
	s := fmt.Sprintf(format, args...)
	fmt.Fprintln(colorable.NewColorableStdout(), color.GreenString(s))
	l.writeFile(s)
}

func (l *logger) Noticef(format string, args ...interface{}) {
	s := fmt.Sprintf(format, args...)
	fmt.Fprintln(colorable.NewColorableStdout(), color.YellowString(s))
	l.writeFile(s)
}

func (l *logger) Warnf(format string, args ...interface{}) {
	s := fmt.Sprintf(format, args...)
	fmt.Fprintln(colorable.NewColorableStdout(), color.YellowString(s))
	l.writeFile(s)
}

func (l *logger) Errorf(format string, args ...interface{}) {
	s := fmt.Sprintf(format, args...)
	fmt.Fprintln(colorable.NewColorableStderr(), color.RedString(s))
	l.writeFile(s)
}

func (l *logger) Verbosef(format string, args ...interface{}) {
	s := fmt.Sprintf(format, args...)
	l.writeFile(s)
}

func (l *logger) Path() string {
	return l.fw.Path()
}

func (l *logger) Stdout() io.Writer {
	return l.fw
}

func (l *logger) Stderr() io.Writer {
	return l.fw
}

func (l *logger) writeFile(s string) {
	if l.fw == nil {
		return
	}
	fmt.Fprintln(l.fw, s)

}

func (l *verboseLogger) Verbosef(format string, args ...interface{}) {
	l.Logger.Verbosef(format, args...)
	fmt.Fprintln(os.Stdout, fmt.Sprintf(format, args...))
}

func (l *verboseLogger) Stdout() io.Writer {
	return l.stdout
}

func (l *verboseLogger) Stderr() io.Writer {
	return l.stderr
}

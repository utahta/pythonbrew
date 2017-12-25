package installer

import (
	"archive/tar"
	"compress/gzip"
	"io"
	"os"
	"path/filepath"

	"github.com/pkg/errors"
	"github.com/utahta/pythonbrew/log"
)

type (
	// Extractor extract tar gzip
	Extractor interface {
		Extract(dst string, src string) error
	}

	extractor struct {
		log log.Logger
	}
)

// NewExtractor returns Extractor
func NewExtractor() Extractor {
	return &extractor{
		log: log.NewFileLogger(),
	}
}

func (e *extractor) Extract(dst string, src string) error {
	const tag = "extractor.extract"

	fp, err := os.Open(src)
	if err != nil {
		return errors.Wrap(err, tag)
	}
	defer fp.Close()

	gr, err := gzip.NewReader(fp)
	if err != nil {
		return errors.Wrap(err, tag)
	}
	defer gr.Close()

	defer e.log.Infof("")
	tr := tar.NewReader(gr)
	for {
		header, err := tr.Next()
		if err == io.EOF {
			break
		} else if err != nil {
			return errors.Wrap(err, tag)
		}

		filename := filepath.Join(dst, header.Name)
		e.log.Progressf("Extracting %s into %s", filepath.Base(src), filename)

		switch header.Typeflag {
		case tar.TypeDir:
			if err := os.Mkdir(filename, os.FileMode(header.Mode)); err != nil {
				return errors.Wrap(err, tag)
			}
			if err := os.Chtimes(filename, header.ModTime, header.ModTime); err != nil {
				return errors.Wrap(err, tag)
			}
		case tar.TypeReg:
			err = func() error {
				fp, err := os.OpenFile(filename, os.O_CREATE|os.O_RDWR, os.FileMode(header.Mode))
				if err != nil {
					return errors.WithStack(err)
				}
				defer fp.Close()

				if _, err := io.Copy(fp, tr); err != nil {
					return errors.WithStack(err)
				}
				return nil
			}()
			if err != nil {
				return errors.Wrap(err, tag)
			}

			if err := os.Chtimes(filename, header.ModTime, header.ModTime); err != nil {
				return errors.Wrap(err, tag)
			}
		default:
			return errors.Errorf("%v: invalid type flag %v", tag, header.Typeflag)
		}
	}
	return nil
}

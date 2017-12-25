package installer

import (
	"crypto/md5"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
	"path/filepath"

	"github.com/pkg/errors"
	"github.com/utahta/pythonbrew/log"
)

type (
	// Downloader fetches a file given url
	Downloader interface {
		WithHTTPClient(c *http.Client)
		Download(u *url.URL, filename string) error
	}

	downloader struct {
		httpClient *http.Client
		log        log.Logger
	}
)

// NewDownloader returns downloader
func NewDownloader() Downloader {
	return &downloader{
		httpClient: http.DefaultClient,
		log:        log.NewFileLogger(),
	}
}

func (d *downloader) WithHTTPClient(c *http.Client) {
	d.httpClient = c
}

func (d *downloader) Download(u *url.URL, filename string) error {
	const tag = "downloader.download"
	if u == nil {
		return errors.Errorf("%v: invalid url", tag)
	}

	resp, err := d.httpClient.Get(u.String())
	if err != nil {
		return errors.Wrap(err, tag)
	}
	defer resp.Body.Close()

	fp, err := os.Create(filename)
	if err != nil {
		return errors.Wrap(err, tag)
	}
	defer fp.Close()

	err = d.copy(fp, resp.Body, func(written int64) {
		d.log.Progressf("Downloading %s as %s %dKB of %dKB", filepath.Base(filename), filename, written/1024, resp.ContentLength/1024)
	})
	d.log.Infof("")
	if err != nil {
		defer os.Remove(filename)
		return errors.Wrap(err, tag)
	}

	if err := d.validate(fp, u.Fragment); err != nil {
		defer os.Remove(filename)
		return errors.Wrap(err, tag)
	}
	return nil
}

func (d *downloader) copy(dst io.Writer, src io.Reader, log func(int64)) error {
	const limit = 32 * 1024
	var written int64
	for {
		nw, err := io.CopyN(dst, src, limit)
		if nw > 0 {
			written += nw
			log(written)
		}

		if err != nil {
			if err != io.EOF {
				return errors.WithStack(err)
			}
			break
		}
	}
	return nil
}

func (d *downloader) validate(fp *os.File, fragment string) error {
	if fragment == "" {
		return nil
	}

	if _, err := fp.Seek(0, 0); err != nil {
		return errors.WithStack(err)
	}

	hash := md5.New()
	if _, err := io.Copy(hash, fp); err != nil {
		return errors.WithStack(err)
	}

	hashStr := fmt.Sprintf("%x", hash.Sum(nil))
	if hashStr != fragment {
		return errors.Errorf("incorrect checksum:%s", hashStr)
	}
	return nil
}

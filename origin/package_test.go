package origin

import (
	"strings"
	"testing"
)

func TestFindPackage(t *testing.T) {
	tests := []struct {
		arg      string
		expected string
	}{
		{"2.7.15", "2.7.15"},
		{"3.6.8", "3.6.8"},
		{"3.7.2", "3.7.2"},
		{"https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tgz", "3.6.4"},
	}
	for _, test := range tests {
		pkg, err := FindPackage(test.arg)
		if err != nil {
			t.Fatal(err)
		}

		if pkg.Version().String() != test.expected {
			t.Errorf("Expected %v, got %v", test.expected, pkg.Version().String())
		}
	}

	_, err := FindPackage("1.0.0")
	if !strings.HasPrefix(err.Error(), "missing package") {
		t.Errorf("Expected missing package error, got %v", err)
	}
}

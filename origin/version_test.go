package origin

import "testing"

func TestParseVersion(t *testing.T) {
	tests := []struct {
		version  string
		expected string
		major    int
		minor    int
	}{
		{"1.2", "1.2", 1, 2},
		{"1.2-dev", "1.2-dev", 1, 2},
		{"1.2.3", "1.2.3", 1, 2},
		{"1.2.3-dev", "1.2.3-dev", 1, 2},
	}

	for _, test := range tests {
		v, err := ParseVersion(test.version)
		if err != nil {
			t.Error(err)
		}

		if v.String() != test.expected {
			t.Errorf("Expected %s, got %v", test.expected, v)
		}

		if v.Major() != test.major {
			t.Errorf("Expected %v, got %v", test.major, v.Major())
		}

		if v.Minor() != test.minor {
			t.Errorf("Expected %v, got %v", test.minor, v.Minor())
		}
	}
}

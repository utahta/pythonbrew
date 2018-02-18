package origin

import "testing"

func TestParseVersion(t *testing.T) {
	testcases := []struct {
		version  string
		expected string
		major    int
		minor    int
	}{
		{"1.2", "1.2", 1, 2},
		{"1.2-dev", "1.2-dev", 1, 2},
		{"1.2.3", "1.2.3", 1, 2},
		{"1.2.3-dev", "1.2.3-dev", 1, 2},
		{"1.2.3rc1", "1.2.3rc1", 1, 2},
	}

	for _, testcase := range testcases {
		v, err := ParseVersion(testcase.version)
		if err != nil {
			t.Error(err)
		}

		if v.String() != testcase.expected {
			t.Errorf("Expected %s, got %v", testcase.expected, v)
		}

		if v.Major() != testcase.major {
			t.Errorf("Expected %v, got %v", testcase.major, v.Major())
		}

		if v.Minor() != testcase.minor {
			t.Errorf("Expected %v, got %v", testcase.minor, v.Minor())
		}
	}
}

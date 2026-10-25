// MailTester Ninja, email verification in Go. Standard library only.
// Run:  go run mailtester.go   (free tier, key=free, 10 checks a day, one request every 30 s)
//       MAILTESTER_KEY=your_key go run mailtester.go
// Free token (50 a day): https://mailtester.ninja/free-email-verification-api/
// Paid key (full speed):  https://mailtester.ninja/verify-emails-unlimited/
package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
	"strings"
	"time"
)

const endpoint = "https://happy.mailtester.ninja/ninja"

// freeKey uses the free tier without signup. Free calls are limited to one every 30 s.
const freeKey = "free"

// IsFree reports whether key is the keyless free tier or a free token (mtf_...).
func IsFree(key string) bool { return key == freeKey || strings.HasPrefix(key, "mtf_") }

// Result is the API response. The useful field is Code: "ok", "ko" or "mb".
type Result struct {
	Email   string `json:"email"`
	User    string `json:"user"`
	Domain  string `json:"domain"`
	MX      string `json:"mx"`
	Code    string `json:"code"`
	Message string `json:"message"`
}

// Verify checks a single address. A free limit (HTTP 429) is returned as an error:
// it is not a verdict, its message says how long to wait.
func Verify(email, key string) (*Result, error) {
	u, _ := url.Parse(endpoint)
	q := u.Query()
	q.Set("email", email)
	q.Set("key", key)
	u.RawQuery = q.Encode()

	client := &http.Client{Timeout: 30 * time.Second}
	resp, err := client.Get(u.String())
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	body, _ := io.ReadAll(resp.Body)
	if resp.StatusCode == http.StatusTooManyRequests {
		var lim Result
		_ = json.Unmarshal(body, &lim)
		return nil, fmt.Errorf("free limit: %s", lim.Message)
	}
	if resp.StatusCode < 200 || resp.StatusCode >= 300 {
		return nil, fmt.Errorf("HTTP %d", resp.StatusCode)
	}
	var r Result
	if err := json.Unmarshal(body, &r); err != nil {
		return nil, err
	}
	return &r, nil
}

func main() {
	key := os.Getenv("MAILTESTER_KEY")
	if key == "" {
		key = freeKey
	}
	delay := time.Second // respect the rate limit
	if IsFree(key) {
		delay = 30 * time.Second
		fmt.Println("Free tier: one request every 30 s. Paid keys go full speed: https://mailtester.ninja/verify-emails-unlimited/")
	}

	emails := []string{"info@apple.com", "test@gmail.com", "someone@example.com"}
	for _, email := range emails {
		r, err := Verify(email, key)
		if err != nil {
			fmt.Printf("  %-30s error: %v\n", email, err)
		} else {
			fmt.Printf("  %-30s %-6s %s\n", r.Email, r.Code, r.Message)
		}
		time.Sleep(delay)
	}
}

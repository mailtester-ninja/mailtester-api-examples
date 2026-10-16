// MailTester Ninja, email verification in Go. Standard library only.
// Run:  MAILTESTER_KEY=xxx go run mailtester.go
// Get a key: https://mailtester.ninja/verify-emails-unlimited/
package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
	"time"
)

const endpoint = "https://happy.mailtester.ninja/ninja"

// Result is the API response. The useful field is Code: "ok", "ko" or "mb".
type Result struct {
	Email   string `json:"email"`
	User    string `json:"user"`
	Domain  string `json:"domain"`
	MX      string `json:"mx"`
	Code    string `json:"code"`
	Message string `json:"message"`
}

// Verify checks a single address.
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
	if resp.StatusCode < 200 || resp.StatusCode >= 300 {
		return nil, fmt.Errorf("HTTP %d", resp.StatusCode)
	}
	body, _ := io.ReadAll(resp.Body)
	var r Result
	if err := json.Unmarshal(body, &r); err != nil {
		return nil, err
	}
	return &r, nil
}

func main() {
	key := os.Getenv("MAILTESTER_KEY")
	if key == "" {
		fmt.Fprintln(os.Stderr, "Set MAILTESTER_KEY. Get one at https://mailtester.ninja/verify-emails-unlimited/")
		os.Exit(1)
	}

	emails := []string{"info@apple.com", "test@gmail.com", "someone@example.com"}
	for _, email := range emails {
		r, err := Verify(email, key)
		if err != nil {
			fmt.Printf("  %-30s error: %v\n", email, err)
			continue
		}
		fmt.Printf("  %-30s %-6s %s\n", r.Email, r.Code, r.Message)
		time.Sleep(time.Second) // respect the rate limit
	}
}

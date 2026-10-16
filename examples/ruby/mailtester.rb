# MailTester Ninja, email verification in Ruby. Standard library only.
# Run:  MAILTESTER_KEY=xxx ruby mailtester.rb
# Get a key: https://mailtester.ninja/verify-emails-unlimited/

require "net/http"
require "uri"
require "json"
require "cgi"

ENDPOINT = "https://happy.mailtester.ninja/ninja"

# Verify a single email address. Returns a Hash (the parsed API response).
# The useful key is "code": "ok" valid, "ko" invalid, "mb" uncertain.
def verify(email, key)
  uri = URI(ENDPOINT)
  uri.query = URI.encode_www_form(email: email, key: key)
  res = Net::HTTP.get_response(uri)
  raise "HTTP #{res.code}" unless res.is_a?(Net::HTTPSuccess)
  JSON.parse(res.body)
end

# True only when the address is clearly valid and deliverable.
def deliverable?(email, key)
  verify(email, key)["code"] == "ok"
end

if __FILE__ == $PROGRAM_NAME
  key = ENV["MAILTESTER_KEY"]
  abort "Set MAILTESTER_KEY. Get one at https://mailtester.ninja/verify-emails-unlimited/" unless key

  ["info@apple.com", "test@gmail.com", "someone@example.com"].each do |email|
    begin
      r = verify(email, key)
      printf("  %-30s %-6s %s\n", r["email"], r["code"], r["message"])
    rescue => e
      printf("  %-30s error: %s\n", email, e.message)
    end
    sleep 1 # respect the rate limit
  end
end

# MailTester Ninja, email verification in Ruby. Standard library only.
# Run:  ruby mailtester.rb   (free tier, key=free, 10 checks a day, one request every 30 s)
#       MAILTESTER_KEY=your_key ruby mailtester.rb
# Free token (50 a day): https://mailtester.ninja/free-email-verification-api/
# Paid key (full speed):  https://mailtester.ninja/verify-emails-unlimited/

require "net/http"
require "uri"
require "json"
require "cgi"

ENDPOINT = "https://happy.mailtester.ninja/ninja"
FREE_KEY = "free"

# True for the keyless free tier and for free tokens (mtf_...).
def free?(key)
  key == FREE_KEY || key.start_with?("mtf_")
end

# Verify a single email address. Returns a Hash (the parsed API response).
# The useful key is "code": "ok" valid, "ko" invalid, "mb" uncertain.
# A free limit (HTTP 429) raises: it is not a verdict, the message says how long to wait.
def verify(email, key = FREE_KEY)
  uri = URI(ENDPOINT)
  uri.query = URI.encode_www_form(email: email, key: key)
  res = Net::HTTP.get_response(uri)
  raise "free limit: #{JSON.parse(res.body)["message"]}" if res.code == "429"
  raise "HTTP #{res.code}" unless res.is_a?(Net::HTTPSuccess)
  JSON.parse(res.body)
end

# True only when the address is clearly valid and deliverable.
def deliverable?(email, key = FREE_KEY)
  verify(email, key)["code"] == "ok"
end

if __FILE__ == $PROGRAM_NAME
  key = ENV.fetch("MAILTESTER_KEY", FREE_KEY)
  delay = free?(key) ? 30 : 1 # respect the rate limit
  puts "Free tier: one request every 30 s. Paid keys go full speed: https://mailtester.ninja/verify-emails-unlimited/" if free?(key)

  ["info@apple.com", "test@gmail.com", "someone@example.com"].each do |email|
    begin
      r = verify(email, key)
      printf("  %-30s %-6s %s\n", r["email"], r["code"], r["message"])
    rescue => e
      printf("  %-30s error: %s\n", email, e.message)
    end
    sleep delay
  end
end

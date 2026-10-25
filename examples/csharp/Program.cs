// MailTester Ninja, email verification in C# (.NET 6+). Uses HttpClient + System.Text.Json.
// Run:  dotnet run   (free tier, key=free, 10 checks a day, one request every 30 s)
//       MAILTESTER_KEY=your_key dotnet run
// Free token (50 a day): https://mailtester.ninja/free-email-verification-api/
// Paid key (full speed):  https://mailtester.ninja/verify-emails-unlimited/

using System.Net;
using System.Text.Json;
using System.Web;

string key = Environment.GetEnvironmentVariable("MAILTESTER_KEY") ?? "free";
bool isFree = key == "free" || key.StartsWith("mtf_");
int delayMs = isFree ? 30000 : 1000; // respect the rate limit
if (isFree) Console.WriteLine("Free tier: one request every 30 s. Paid keys go full speed: https://mailtester.ninja/verify-emails-unlimited/");

const string endpoint = "https://happy.mailtester.ninja/ninja";
using var http = new HttpClient();

async Task<JsonElement> Verify(string email)
{
    var url = $"{endpoint}?email={HttpUtility.UrlEncode(email)}&key={HttpUtility.UrlEncode(key)}";
    using var res = await http.GetAsync(url);
    var body = await res.Content.ReadAsStringAsync();
    var json = JsonDocument.Parse(body).RootElement;
    if (res.StatusCode == HttpStatusCode.TooManyRequests)
    {
        // Free limit reached: not a verdict, the message says how long to wait.
        throw new InvalidOperationException("free limit: " + json.GetProperty("message").GetString());
    }
    res.EnsureSuccessStatusCode();
    return json;
}

string[] emails = { "info@apple.com", "test@gmail.com", "someone@example.com" };
foreach (var email in emails)
{
    try
    {
        var r = await Verify(email);
        var code = r.GetProperty("code").GetString();
        var message = r.GetProperty("message").GetString();
        Console.WriteLine($"  {email,-30} {code,-6} {message}");
    }
    catch (Exception e)
    {
        Console.WriteLine($"  {email,-30} error: {e.Message}");
    }
    await Task.Delay(delayMs);
}

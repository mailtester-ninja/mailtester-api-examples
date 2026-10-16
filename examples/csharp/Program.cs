// MailTester Ninja, email verification in C# (.NET 6+). Uses HttpClient + System.Text.Json.
// Run:  MAILTESTER_KEY=xxx dotnet run
// Get a key: https://mailtester.ninja/verify-emails-unlimited/

using System.Text.Json;
using System.Web;

string key = Environment.GetEnvironmentVariable("MAILTESTER_KEY")
    ?? throw new InvalidOperationException(
        "Set MAILTESTER_KEY. Get one at https://mailtester.ninja/verify-emails-unlimited/");

const string endpoint = "https://happy.mailtester.ninja/ninja";
using var http = new HttpClient();

async Task<JsonElement> Verify(string email)
{
    var url = $"{endpoint}?email={HttpUtility.UrlEncode(email)}&key={HttpUtility.UrlEncode(key)}";
    var body = await http.GetStringAsync(url);
    return JsonDocument.Parse(body).RootElement;
}

string[] emails = { "info@apple.com", "test@gmail.com", "someone@example.com" };
foreach (var email in emails)
{
    var r = await Verify(email);
    var code = r.GetProperty("code").GetString();
    var message = r.GetProperty("message").GetString();
    Console.WriteLine($"  {email,-30} {code,-6} {message}");
    await Task.Delay(1000); // respect the rate limit
}

// MailTester Ninja, email verification in Java (11+). No dependencies, uses java.net.http.
// Run:  java MailTester.java   (single-file source, Java 11+; free tier, key=free, 10 checks a day)
//       MAILTESTER_KEY=your_key java MailTester.java
// Free token (50 a day): https://mailtester.ninja/free-email-verification-api/
// Paid key (full speed):  https://mailtester.ninja/verify-emails-unlimited/

import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class MailTester {

    static final String ENDPOINT = "https://happy.mailtester.ninja/ninja";
    static final String FREE_KEY = "free";

    // True for the keyless free tier and for free tokens (mtf_...). Free calls: one every 30 s.
    static boolean isFree(String key) {
        return FREE_KEY.equals(key) || key.startsWith("mtf_");
    }

    // Minimal field extractor so the example stays dependency free.
    // In a real project use Jackson or Gson to parse the JSON response.
    static String field(String json, String name) {
        Matcher m = Pattern.compile("\"" + name + "\"\\s*:\\s*\"([^\"]*)\"").matcher(json);
        return m.find() ? m.group(1) : "";
    }

    static String verify(String email, String key) throws Exception {
        String url = ENDPOINT
                + "?email=" + URLEncoder.encode(email, StandardCharsets.UTF_8)
                + "&key=" + URLEncoder.encode(key, StandardCharsets.UTF_8);
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest req = HttpRequest.newBuilder(URI.create(url)).GET().build();
        HttpResponse<String> res = client.send(req, HttpResponse.BodyHandlers.ofString());
        if (res.statusCode() == 429) {
            // Free limit reached: not a verdict, the message says how long to wait.
            throw new RuntimeException("free limit: " + field(res.body(), "message"));
        }
        if (res.statusCode() < 200 || res.statusCode() >= 300) {
            throw new RuntimeException("HTTP " + res.statusCode());
        }
        return res.body();
    }

    public static void main(String[] args) throws Exception {
        String key = System.getenv("MAILTESTER_KEY");
        if (key == null || key.isEmpty()) {
            key = FREE_KEY;
        }
        long delayMs = isFree(key) ? 30000 : 1000; // respect the rate limit
        if (isFree(key)) {
            System.out.println("Free tier: one request every 30 s. Paid keys go full speed: https://mailtester.ninja/verify-emails-unlimited/");
        }
        String[] emails = {"info@apple.com", "test@gmail.com", "someone@example.com"};
        for (String email : emails) {
            try {
                String json = verify(email, key);
                System.out.printf("  %-30s %-6s %s%n", email, field(json, "code"), field(json, "message"));
            } catch (RuntimeException e) {
                System.out.printf("  %-30s error: %s%n", email, e.getMessage());
            }
            Thread.sleep(delayMs);
        }
    }
}

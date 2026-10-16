// MailTester Ninja, email verification in Java (11+). No dependencies, uses java.net.http.
// Run:  MAILTESTER_KEY=xxx java MailTester.java   (single-file source, Java 11+)
// Get a key: https://mailtester.ninja/verify-emails-unlimited/

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
        if (res.statusCode() < 200 || res.statusCode() >= 300) {
            throw new RuntimeException("HTTP " + res.statusCode());
        }
        return res.body();
    }

    public static void main(String[] args) throws Exception {
        String key = System.getenv("MAILTESTER_KEY");
        if (key == null || key.isEmpty()) {
            System.err.println("Set MAILTESTER_KEY. Get one at https://mailtester.ninja/verify-emails-unlimited/");
            System.exit(1);
        }
        String[] emails = {"info@apple.com", "test@gmail.com", "someone@example.com"};
        for (String email : emails) {
            String json = verify(email, key);
            String code = field(json, "code");
            String message = field(json, "message");
            System.out.printf("  %-30s %-6s %s%n", email, code, message);
            Thread.sleep(1000); // respect the rate limit
        }
    }
}

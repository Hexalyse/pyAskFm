import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Map.Entry;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;

/* This class is just a decompiled version of the AskFM bytecode from the APK, with minimum rework to make it work.
It would be convenient to re-implement it in Python, so we don't have to call a Java jar.
*/

public class Signature {
    public static String generateHash(String method, String host, String path, Map<String, Object> params) {
        // Replace the "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX" with the API key present in the AskFM apk.
        // I won't include it in this code for intellectual property reasons.
        return generateHashWithKey("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX", method, host, path, params);
    }

    public static String generateHashWithKey(String key, String method, String host, String path, Map<String, Object> params) {
        String result = null;
        try {
            result = sha1(method + "%" + host + "%" + path + "%" + serializeParams(params), key);
        } catch (Exception e) {
            System.out.println("Network" + "Error generating hash" + e);
        }
        return result;
    }

    public static String sha1(String s, String keyString) throws Exception {
        Mac mac = Mac.getInstance("HmacSHA1");
        mac.init(new SecretKeySpec(keyString.getBytes(), "HmacSHA1"));
        byte[] digest = mac.doFinal(s.getBytes());
        StringBuffer result = new StringBuffer(digest.length * 2);
        for (byte aDigest : digest) {
            appendHex(result, aDigest);
        }
        return result.toString().toLowerCase(Locale.US);
    }

    private static void appendHex(StringBuffer sb, byte b) {
        sb.append("0123456789ABCDEF".charAt((b >> 4) & 15)).append("0123456789ABCDEF".charAt(b & 15));
    }

    private static String serializeParams(Map<String, Object> params) {
        List<String> pairs = new ArrayList();
        for (Entry<String, Object> entry : params.entrySet()) {
            if (entry.getValue() != null) {
                pairs.add((encode((String) entry.getKey()) + "%" + encode(entry.getValue().toString())).replace("+", "%20"));
            }
        }
        Collections.sort(pairs);
        return concatenateList(pairs, "%");
    }

    private static String concatenateList(List<String> inputArray, String glueString) {
        String output = "";
        if (inputArray.isEmpty()) {
            return output;
        }
        StringBuilder builder = new StringBuilder((String) inputArray.get(0));
        for (int i = 1; i < inputArray.size(); i++) {
            builder.append(glueString);
            builder.append((String) inputArray.get(i));
        }
        return builder.toString();
    }

    public static String encode(String s) {
        String result = "";
        if (s == null) {
            return result;
        }
        try {
            return URLEncoder.encode(s, "UTF-8").replaceAll("\\+", "%20").replaceAll("%21", "!").replaceAll("%27", "'").replaceAll("%28", "(").replaceAll("%29", ")").replaceAll("%7E", "~");
        } catch (UnsupportedEncodingException e) {
            System.out.println("Network" + "Unsupported encoding while encoding" + e);
            return s;
        }
    }
}
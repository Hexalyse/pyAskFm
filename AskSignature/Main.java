import java.util.HashMap;
import java.util.Map;

/*
This is just a very ugly main class implemented to call the Java HMAC key generation code from another app.

-- How to use it ?
-> You must first compile *.java files into their corresponding *.class file... and it should be okay

It would be much better to re-implement it in Python but I was too lazy for it :)
You're more than welcome to do it, and submit a PR.
*/

public class Main {

    public static void main(String[] args) {

        Map argsMap = new HashMap();
        for (int i = 3; i < args.length; i+=2) {
            argsMap.put(args[i], args[i + 1]);
        }
        System.out.println(Signature.generateHash(args[0], args[1], args[2], argsMap));
    }
}

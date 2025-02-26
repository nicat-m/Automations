import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLSocket;
import javax.net.ssl.SSLSocketFactory;
import java.io.FileOutputStream;
import java.security.cert.Certificate;
import java.security.cert.X509Certificate;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);
        System.out.println("Enter domain name please...(example.com)");
        String hostname = sc.nextLine(); // Replace with the website's hostname
        int port = 443;

        try {
            SSLContext sslContext = SSLContext.getInstance("TLS");
            sslContext.init(null, null, null);
            SSLSocketFactory sslSocketFactory = sslContext.getSocketFactory();

            try (SSLSocket sslSocket = (SSLSocket) sslSocketFactory.createSocket(hostname, port)) {
                sslSocket.startHandshake();
                Certificate[] certificates = sslSocket.getSession().getPeerCertificates();

                for (int i = 0; i < certificates.length; i++) {
                    X509Certificate certificate = (X509Certificate) certificates[i];
                    String fileName = hostname  + "_" + i + ".cer";
                    try (FileOutputStream fos = new FileOutputStream(fileName)) {
                        fos.write(certificate.getEncoded());
                        System.out.println("Certificate " + i + " exported to " + fileName);
                    }
                    System.out.println("---------------------------------------");
                    System.out.println("Certificate " + i + " Information:");
                    System.out.println("---------------------------------------");
                    System.out.println("Subject: " + certificate.getSubjectDN());
                    System.out.println("---------------------------------------");
                    System.out.println("Issuer: " + certificate.getIssuerDN());
                    System.out.println("---------------------------------------");
                    System.out.println("Serial Number: " + certificate.getSerialNumber());
                    System.out.println("---------------------------------------");
                    System.out.println("Valid From: " + certificate.getNotBefore());
                    System.out.println("---------------------------------------");
                    System.out.println("Valid Until: " + certificate.getNotAfter());
                    System.out.println("---------------------------------------");

                }
                System.out.println("Domain certificate exported successfully...");
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

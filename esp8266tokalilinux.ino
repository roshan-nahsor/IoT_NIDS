

// // #include <ESP8266WiFi.h>
// // #include <WiFiUdp.h>

// // // Replace with your Wi-Fi credentials
// // const char* ssid = "Airtel_kcma_8185";
// // const char* password = "Arati123";

// // // UDP object
// // WiFiUDP udp;

// // // LED pin (built-in)
// // const int ledPin = LED_BUILTIN;

// // // Define the packet structure
// // struct Packet {
// //   const char* dst_ip;
// //   int dst_port;
// //   const char* data;
// // };

// // // Hardcoded packets from your CSV (shortened for demonstration)
// // Packet packets[] = {
// //   {"192.168.0.128", 80, "X-JUTVUlecM3bjrcC6: HskTfwXiB"},
// //   {"192.168.0.128", 80, "X-5ezTl: m6cLZ4WSW59y74"},
// //   {"192.168.0.128", 80, "X-CmhTFUonVKgx7zZFZThls: 58wy8it2gveBChVoKryqcu"},
// //   {"192.168.0.170", 37614, ""},
// //   {"192.168.0.170", 37616, ""},
// //   {"192.168.0.170", 37618, ""},
// //   {"192.168.0.128", 80, "X-1: 2LXb1vW0fKy"},
// //   {"192.168.0.128", 80, "X-2zluA: K0rgqMpcNgEt"},
// //   {"192.168.0.128", 80, "X-KOtvG8gmC: mxvbWdaSn"}
// // };

// // void setup() {
// //   Serial.begin(115200);
// //   delay(1000);

// //   // Setup LED pin
// //   pinMode(ledPin, OUTPUT);
// //   digitalWrite(ledPin, HIGH); // OFF initially (inverted logic)

// //   // Connect to Wi-Fi
// //   Serial.println("Connecting to Wi-Fi...");
// //   WiFi.begin(ssid, password);

// //   int retryCount = 0;
// //   while (WiFi.status() != WL_CONNECTED && retryCount < 20) {
// //     delay(1000);
// //     Serial.print(".");
// //     retryCount++;
// //   }

// //   if (WiFi.status() != WL_CONNECTED) {
// //     Serial.println("\n❌ Failed to connect to Wi-Fi.");
// //     return;
// //   }

// //   Serial.println("\n✅ Wi-Fi connected!");
// //   Serial.print("ESP8266 IP: ");
// //   Serial.println(WiFi.localIP());
// // }

// // void loop() {
// //   for (int i = 0; i < sizeof(packets) / sizeof(Packet); i++) {
// //     IPAddress ip;

// //     if (ip.fromString(packets[i].dst_ip)) {
// //       // Blink LED ON
// //       digitalWrite(ledPin, LOW);

// //       // Send UDP packet
// //       udp.beginPacket(ip, packets[i].dst_port);
// //       udp.write((const uint8_t*)packets[i].data, strlen(packets[i].data));
// //       udp.endPacket();

// //       // Blink LED OFF after short delay
// //       delay(100);
// //       digitalWrite(ledPin, HIGH);

// //       Serial.printf("Sent to %s:%d -> \"%s\"\n",
// //                     packets[i].dst_ip,
// //                     packets[i].dst_port,
// //                     packets[i].data);
// //     } else {
// //       Serial.printf("❌ Invalid IP format: %s\n", packets[i].dst_ip);
// //     }

// //     delay(300); // Optional pause between packets
// //   }

// //   delay(2000); // Delay before repeating the whole sequence
// // }


// #include <ESP8266WiFi.h>
// const char* ssid = "Airtel_kcma_8185";
// const char* password = "Arati123";

// void setup() {
//   Serial.begin(115200);
//   WiFi.begin(ssid, password);

//   Serial.print("Connecting to WiFi");
//   while (WiFi.status() != WL_CONNECTED) {
//     delay(500);
//     Serial.print(".");
//   }

//   Serial.println("\nConnected to WiFi");
//   Serial.print("IP address: ");
//   Serial.println(WiFi.localIP());
// }

// void loop() {
//   // nothing here
// }


#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

const char* ssid = "Airtel_nahi_hai";
const char* password = "505aur202se201";


// Kali Linux IP and port number
// const char* kali_ip = "192.168.1.10";
const char* ras_pi = "192.168.1.12";

const int port = 12345;


WiFiUDP udp;

// Packet data (JSON strings from your packet headers)
String packets[15] = {
  "{\"frame.time\":\"Apr 16, 2024 18:11:44.926343000 IST\",\"tcp.ack\":\"1\",\"tcp.ack_raw\":\"2655894636\",\"tcp.checksum\":\"0xe628\",\"tcp.connection.fin\":\"0\",\"tcp.connection.rst\":\"0\",\"tcp.connection.syn\":\"0\",\"tcp.connection.synack\":\"0\",\"tcp.dstport\":\"443\",\"tcp.flags\":\"0x010\",\"tcp.flags.ack\":\"1\",\"tcp.len\":\"0\",\"tcp.options\":\"\",\"tcp.payload\":\"\",\"tcp.seq\":\"1730987345\",\"tcp.srcport\":\"35960\"}",
  "{\"frame.time\":\"Apr 16, 2024 18:11:44.926367000 IST\",\"tcp.ack\":\"1\",\"tcp.ack_raw\":\"2655894636\",\"tcp.checksum\":\"0xd44a\",\"tcp.connection.fin\":\"0\",\"tcp.connection.rst\":\"0\",\"tcp.connection.syn\":\"0\",\"tcp.connection.synack\":\"0\",\"tcp.dstport\":\"443\",\"tcp.flags\":\"0x018\",\"tcp.flags.ack\":\"1\",\"tcp.len\":\"0\",\"tcp.options\":\"\",\"tcp.payload\":\"\",\"tcp.seq\":\"1730987345\",\"tcp.srcport\":\"35960\"}",
  "{\"frame.time\":\"Apr 16, 2024 18:11:44.942007000 IST\",\"tcp.ack\":\"1\",\"tcp.ack_raw\":\"1730987346\",\"tcp.checksum\":\"0x5936\",\"tcp.connection.fin\":\"0\",\"tcp.connection.rst\":\"0\",\"tcp.connection.syn\":\"0\",\"tcp.connection.synack\":\"0\",\"tcp.dstport\":\"35960\",\"tcp.flags\":\"0x011\",\"tcp.flags.ack\":\"1\",\"tcp.len\":\"1\",\"tcp.options\":\"\",\"tcp.payload\":\"17\",\"tcp.seq\":\"2655894635\",\"tcp.srcport\":\"443\"}",
  "{\"frame.time\":\"Apr 16, 2024 18:11:44.942026000 IST\",\"tcp.ack\":\"1\",\"tcp.ack_raw\":\"1730987346\",\"tcp.checksum\":\"0xfde4\",\"tcp.connection.fin\":\"0\",\"tcp.connection.rst\":\"0\",\"tcp.connection.syn\":\"0\",\"tcp.connection.synack\":\"0\",\"tcp.dstport\":\"35960\",\"tcp.flags\":\"0x010\",\"tcp.flags.ack\":\"1\",\"tcp.len\":\"0\",\"tcp.options\":\"\",\"tcp.payload\":\"\",\"tcp.seq\":\"2655894636\",\"tcp.srcport\":\"443\"}",
  "{\"frame.time\":\"Apr 16, 2024 18:11:44.951167000 IST\",\"tcp.ack\":\"1\",\"tcp.ack_raw\":\"2655894637\",\"tcp.checksum\":\"0xccc7\",\"tcp.connection.fin\":\"0\",\"tcp.connection.rst\":\"0\",\"tcp.connection.syn\":\"0\",\"tcp.connection.synack\":\"0\",\"tcp.dstport\":\"443\",\"tcp.flags\":\"0x018\",\"tcp.flags.ack\":\"1\",\"tcp.len\":\"0\",\"tcp.options\":\"\",\"tcp.payload\":\"\",\"tcp.seq\":\"1730987346\",\"tcp.srcport\":\"35960\"}",
  "{\"frame.time\":\"Apr 16, 2024 18:11:45.024073000 IST\",\"tcp.ack\":\"1\",\"tcp.ack_raw\":\"1730987346\",\"tcp.checksum\":\"0x7fb1\",\"tcp.connection.fin\":\"0\",\"tcp.connection.rst\":\"0\",\"tcp.connection.syn\":\"0\",\"tcp.connection.synack\":\"0\",\"tcp.dstport\":\"35960\",\"tcp.flags\":\"0x018\",\"tcp.flags.ack\":\"1\",\"tcp.len\":\"3\",\"tcp.options\":\"\",\"tcp.payload\":\"160303\",\"tcp.seq\":\"2655894637\",\"tcp.srcport\":\"443\"}",
  "{\"frame.time\":\"Apr 16, 2024 18:11:45.027435000 IST\",\"tcp.ack\":\"1\",\"tcp.ack_raw\":\"2655894640\",\"tcp.checksum\":\"0xd445\",\"tcp.connection.fin\":\"0\",\"tcp.connection.rst\":\"0\",\"tcp.connection.syn\":\"0\",\"tcp.connection.synack\":\"0\",\"tcp.dstport\":\"443\",\"tcp.flags\":\"0x010\",\"tcp.flags.ack\":\"1\",\"tcp.len\":\"0\",\"tcp.options\":\"\",\"tcp.payload\":\"\",\"tcp.seq\":\"1730987346\",\"tcp.srcport\":\"35960\"}",
  "{\"frame.time\":\"Apr 16, 2024 18:11:45.231364000 IST\",\"tcp.ack\":\"1\",\"tcp.ack_raw\":\"1730987346\",\"tcp.checksum\":\"0x921f\",\"tcp.connection.fin\":\"0\",\"tcp.connection.rst\":\"0\",\"tcp.connection.syn\":\"0\",\"tcp.connection.synack\":\"0\",\"tcp.dstport\":\"35960\",\"tcp.flags\":\"0x018\",\"tcp.flags.ack\":\"1\",\"tcp.len\":\"9\",\"tcp.options\":\"\",\"tcp.payload\":\"16030300\",\"tcp.seq\":\"2655894640\",\"tcp.srcport\":\"443\"}",
  "{\"frame.time\":\"Apr 16, 2024 18:11:45.235341000 IST\",\"tcp.ack\":\"1\",\"tcp.ack_raw\":\"2655894649\",\"tcp.checksum\":\"0xd43b\",\"tcp.connection.fin\":\"0\",\"tcp.connection.rst\":\"0\",\"tcp.connection.syn\":\"0\",\"tcp.connection.synack\":\"0\",\"tcp.dstport\":\"443\",\"tcp.flags\":\"0x010\",\"tcp.flags.ack\":\"1\",\"tcp.len\":\"0\",\"tcp.options\":\"\",\"tcp.payload\":\"\",\"tcp.seq\":\"1730987346\",\"tcp.srcport\":\"35960\"}",
  "{\"frame.time\":\"Apr 16, 2024 18:11:45.238437000 IST\",\"tcp.ack\":\"1\",\"tcp.ack_raw\":\"2655894649\",\"tcp.checksum\":\"0x7d1c\",\"tcp.connection.fin\":\"0\",\"tcp.connection.rst\":\"0\",\"tcp.connection.syn\":\"0\",\"tcp.connection.synack\":\"0\",\"tcp.dstport\":\"443\",\"tcp.flags\":\"0x018\",\"tcp.flags.ack\":\"1\",\"tcp.len\":\"3\",\"tcp.options\":\"\",\"tcp.payload\":\"160301\",\"tcp.seq\":\"1730987346\",\"tcp.srcport\":\"35960\"}",
  "{\"frame.time\":\"Apr 16, 2024 18:11:45.422998000 IST\",\"tcp.ack\":\"1\",\"tcp.ack_raw\":\"2655894649\",\"tcp.checksum\":\"0xced4\",\"tcp.connection.fin\":\"0\",\"tcp.connection.rst\":\"0\",\"tcp.connection.syn\":\"0\",\"tcp.connection.synack\":\"0\",\"tcp.dstport\":\"443\",\"tcp.flags\":\"0x018\",\"tcp.flags.ack\":\"1\",\"tcp.len\":\"3\",\"tcp.options\":\"\",\"tcp.payload\":\"010000\",\"tcp.seq\":\"1730987349\",\"tcp.srcport\":\"35960\"}",
  "{\"frame.time\":\"Apr 16, 2024 18:11:45.527227000 IST\",\"tcp.ack\":\"1\",\"tcp.ack_raw\":\"1730987352\",\"tcp.checksum\":\"0x78cf\",\"tcp.connection.fin\":\"0\",\"tcp.connection.rst\":\"0\",\"tcp.connection.syn\":\"0\",\"tcp.connection.synack\":\"0\",\"tcp.dstport\":\"35960\",\"tcp.flags\":\"0x010\",\"tcp.flags.ack\":\"1\",\"tcp.len\":\"0\",\"tcp.options\":\"\",\"tcp.payload\":\"\",\"tcp.seq\":\"2655894649\",\"tcp.srcport\":\"443\"}",
  "{\"frame.time\":\"Apr 16, 2024 18:11:45.529335000 IST\",\"tcp.ack\":\"1\",\"tcp.ack_raw\":\"2655894649\",\"tcp.checksum\":\"0x7d12\",\"tcp.connection.fin\":\"0\",\"tcp.connection.rst\":\"0\",\"tcp.connection.syn\":\"0\",\"tcp.connection.synack\":\"0\",\"tcp.dstport\":\"443\",\"tcp.flags\":\"0x018\",\"tcp.flags.ack\":\"1\",\"tcp.len\":\"3\",\"tcp.options\":\"\",\"tcp.payload\":\"010000\",\"tcp.seq\":\"1730987352\",\"tcp.srcport\":\"35960\"}"
};

// Delay between packets in milliseconds (calculated from frame.time differences)
unsigned long delays_ms[15] = {
  0, 0, 15, 0, 9, 72, 3, 203, 4, 3, 185, 104, 2, 0, 0 // last two slots padded for safety
};

void setup() {
  Serial.begin(115200);
  Serial.println("ESP8266 UDP Packet Replayer");

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi");
  Serial.print("ESP8266 IP Address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  for (int i = 0; i < 15; i++) {
    delay(delays_ms[i]);

    udp.beginPacket(ras_pi, port);
    udp.write(packets[i].c_str());
    udp.endPacket();

    Serial.print("Sent packet ");
    Serial.print(i + 1);
    Serial.print(": ");
    Serial.println(packets[i]);
  }

  Serial.println("Finished one round. Restarting...\n");
}


#include <Wire.h>
#include <String.h>
#define Vcc 5
#define echoPin 19
#define trigPin 18
#define valve 12

long duration, distance;
bool filling=false;

int tank_height, empty, to_fill, lower_threshold, upper_limit, tank_status, water_level;

bool timed=false;
int currentHour, currentMinute;
int start_time_h, start_time_m, end_time_h, end_time_m;

const char *ntpServer = "pool.ntp.org";
const long gmtOffset_sec = 19800; // IST (UTC+5:30)
const int daylightOffset_sec = 0; // No daylight saving



//----------------------------------------------------//
#include <WiFi.h>
#include "credentials.h"
#include <PubSubClient.h>
#include <ArduinoJson.h>
JsonDocument metrics_jsonDoc, time_jsonDoc;

// Add your MQTT Broker IP address
//const char* mqtt_server = "192.168.1.144";
// const char* mqtt_server = "192.168.0.249";
// const char* mqtt_server = "192.168.200.82";
const char* mqtt_server = "192.168.1.12";            // Airtel_nahi_hai
// const char* mqtt_server = "172.20.10.3";                // adithyA

WiFiClient espClient;
PubSubClient client(espClient);
char msg[50];
int value = 0;

const char* device_name="esp32";
//----------------------------------------------------//

#include <DHT.h>
DHT dht(13, DHT11);
 


void setup(){
  Serial.begin(115200);
  pinMode(Vcc, OUTPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(valve, OUTPUT);

  tank_status=0;
  tank_height=20;
  lower_threshold=4;
  upper_limit=13;
  empty=(tank_height-upper_limit);
  to_fill=(tank_height-lower_threshold);

//----------------------------------------------------//
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  pinMode(2, OUTPUT);                   //Built in LED
//----------------------------------------------------//

  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  pinMode(valve, OUTPUT);

  dht.begin();
  delay(2000);
}

//----------------------------------------------------//
void setup_wifi() {
  Serial.println();

  for (int i = 0; i < numNetworks; i++) {
    Serial.print("Connecting to ");
    Serial.print(ssid[i]);
    WiFi.begin(ssid[i], password[i]);
    
    int attempts = 0;
    while ((WiFi.status() != WL_CONNECTED) && (attempts < 10)) {
      delay(500);
      Serial.print(".");
      attempts++;
    }
    if (WiFi.status() == WL_CONNECTED) {
      Serial.print(" ");
      Serial.print(ssid[i]);
      Serial.print("connected ");
      Serial.print("IP address: ");
      Serial.println(WiFi.localIP());
      delay(100);
      digitalWrite(2, LOW);                   //Stop built-in LED blinking
      break;
    }
    else{
      WiFi.disconnect();
      Serial.println("Disconnect block");
    }
  }
}

void handle_metrics_Json(const JsonDocument& doc) {
    // Access the JSON fields directly
    tank_height = doc["h"];
    upper_limit = doc["ul"];
    lower_threshold = doc["lt"];

    // Print values for testing
    Serial.print("Tank Height: ");
    Serial.println(tank_height);
    Serial.print("Upper Limit: ");
    Serial.println(upper_limit);
    Serial.print("Lower Threshold: ");
    Serial.println(lower_threshold);
}

void handle_time_Json(const JsonDocument& doc) {
    // Access the JSON fields directly
    timed=doc["en"];
    start_time_h = doc["sth"];
    start_time_m = doc["stm"];
    end_time_h = doc["eth"];
    end_time_m = doc["etm"];

    // Print values for testing
    Serial.print("timed: ");
    Serial.println(timed);
    Serial.print("start_time_h: ");
    Serial.println(start_time_h);
    Serial.print("start_time_m: ");
    Serial.println(start_time_m);
    Serial.print("end_time_h: ");
    Serial.println(end_time_h);
    Serial.print("end_time_m: ");
    Serial.println(end_time_m);
}

void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

  if(strcmp(topic, "rpi/broadcast/metrics") == 0) {
    DeserializationError error = deserializeJson(metrics_jsonDoc, message, length);
    // Serial.println("inside /metrics topic");
    if (error) {
      Serial.print("Failed to parse JSON: ");
      Serial.println(error.c_str());
      return;
    }

    // Handle the received JSON object
    handle_metrics_Json(metrics_jsonDoc);
  }

  if(strcmp(topic, "rpi/broadcast/time") == 0) {
    DeserializationError error = deserializeJson(time_jsonDoc, message, length);
    // Serial.println("inside /time topic");
    if (error) {
      Serial.print("Failed to parse JSON: ");
      Serial.println(error.c_str());
      return;
    }

    // Handle the received JSON object
    handle_time_Json(time_jsonDoc);
  }
}

void reconnect() {
  // Loop until we're reconnected
  if(!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect(device_name)) {
      Serial.println("connected");
      // Subscribe
      client.subscribe("rpi/broadcast/#");
    } else {
      Serial.print("failed, rc=");
      Serial.println(client.state());
      // Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}
//----------------------------------------------------//


void main_program() {
  char dht_string[15];
  float temp=dht.readTemperature();
  float humidity=dht.readHumidity();

  // Serial.print("Temp: ");
  // Serial.print(temp);
  // Serial.print(" C ");
  // Serial.print("Humidity: ");
  // Serial.print(humidity);
  // Serial.println(" % ");
  sprintf(dht_string, "%.2f %.2f", temp, humidity);  // Format with 2 decimal places
  Serial.println(dht_string);
  delay(2000);

  client.publish("esp32/Temperature_and_Humidity", dht_string);


  char send[10];                // Array to hold the converted string
  
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  duration = pulseIn(echoPin, HIGH);
  distance = duration / 58.2;
  String disp = String(distance);     

  Serial.print("Distance: ");
  Serial.print(disp);
  Serial.print(" cm ");
  water_level=(tank_height-distance);

  if(distance<=empty) {
    tank_status=2;
    if(filling) {
      digitalWrite(valve, LOW);
      filling=false;
      Serial.println("Tank Full, Valve Closed");
    }  
  }
                        
  else if(distance>=to_fill) {
    if(!filling) {
      digitalWrite(valve, HIGH);
      tank_status=1;
      filling=true;
      Serial.println("Filling Water, Valve Opened");
    }
  }
            
  else{
    if(!filling) {
      tank_status=0;
      Serial.println("Neutral");
      digitalWrite(12, LOW);
    }
  }

  JsonDocument tank;
  tank["wl"] = water_level;
  tank["ts"] = tank_status;
  
  char jsonBuffer[512];
  serializeJson(tank, jsonBuffer);

  // Publish JSON message
  client.publish("esp32/tank", jsonBuffer);

  Serial.print("Published: ");
  Serial.println(jsonBuffer);

  delay(1000);
}

void get_time() {
  time_t now = time(nullptr);
  struct tm *timeinfo = localtime(&now);

  // Get current hour and minute
  currentHour = timeinfo->tm_hour;
  currentMinute = timeinfo->tm_min;

  // Print the current time for debugging
  Serial.print("Current time (IST): ");
  Serial.print(currentHour);
  Serial.print(":");
  Serial.println(currentMinute);
  // Serial.print(" ");
  // delay(3000);                   // this will block the main_program
}

unsigned long previousMillis = 0;   // Stores the last time the action was performed
const long interval = 30000;        // Interval for the delay (in milliseconds)

void loop(){
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  // Serial.println("after client.loop");
  unsigned long currentMillis = millis(); // Get the current time

  

  if(timed) {
    // Check if it's time to perform the action
    if (currentMillis - previousMillis >= interval) {
      previousMillis = currentMillis; // Save the last time the action was performed
      get_time();
    }
    if((start_time_h <= currentHour) && (currentHour <= end_time_h) && (start_time_m <= currentMinute) && (currentMinute <=end_time_m)) {
      digitalWrite(Vcc, HIGH);
      main_program();
    }
    else {
      digitalWrite(valve, LOW);
      filling=false;
      delay(2000);
      digitalWrite(Vcc, LOW);
    }
  }
  else {
    digitalWrite(Vcc, HIGH);
    main_program();
  }
  // Serial.print("tank_height: ");
  // Serial.println(tank_height);
  // Serial.print("lower_threshold: ");
  // Serial.println(lower_threshold);
  // Serial.print("upper_limit: ");
  // Serial.println(upper_limit);
  // Serial.print("empty: ");
  // Serial.println(empty);
  // Serial.print("to_fill: ");
  // Serial.println(to_fill);
  // Serial.print("Distance");
  // Serial.println(distance);

  // Serial.println("Hello World");
}
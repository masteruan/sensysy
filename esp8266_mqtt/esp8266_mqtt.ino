/*
* satellite
* 16 Maggio 2017
*
* DHT11
* Photoresistor
* Neopixel
*
* */

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Adafruit_NeoPixel.h>
#include "DHT.h"

#define DHTPIN 5
#define DHTTYPE DHT11
#define adafruitPIN 6
#define adafruitNUM 12

Adafruit_NeoPixel strip = Adafruit_NeoPixel(adafruitNUM, adafruitPIN, NEO_GRB + NEO_KHZ800);

// Update these with values suitable for your network.
const char* ssid = "#########";
const char* password = "#################";
const char* mqtt_server = "192.168.1.79"; // Raspberry IP

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;


DHT dht(DHTPIN, DHTTYPE);

int photo = A0;

void setup() {
  pinMode(2, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  dht.begin();
  float t = dht.readTemperature();
  Serial.println(t);
  strip.begin();
  strip.show(); // initialize strip off
  for (int i = 0; i < adafruitNUM + 1; i++){
    strip.setPixelColor(i,255, 0, 0);
    strip.show();
    delay(100);
  }
  for (int i = 0; i < adafruitNUM + 1; i++){
    strip.setPixelColor(i,0, 0, 0);
    strip.show();
  }
}

void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  // Switch on the LED if an 1 was received as first character
  if ((char)payload[0] == '1') {
    digitalWrite(2, LOW);   // Turn the LED on (Note that LOW is the voltage level
    // but actually the LED is on; this is because
    // it is acive low on the ESP-01)
  } else {
    digitalWrite(2, HIGH);  // Turn the LED off by making the voltage HIGH
  }

}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish("outTopic", "hello world");
      // ... and resubscribe
      client.subscribe("inTopic");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}
void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  long now = millis();
  if (now - lastMsg > 10000) {
    lastMsg = now;
    ++value;
    float h = dht.readHumidity();
    float t = dht.readTemperature();
    int lux = analogRead(photo);
    snprintf (msg, 75, "hello world #%ld", value);
    Serial.print("Publish message: ");
    Serial.println(msg);
    Serial.print(lux);

    //client.publish("outTopic", msg);
    client.publish("time",String(value).c_str(), true);
    client.publish("temp",String(t).c_str(), true);
    client.publish("lux",String(lux).c_str(), true);
    client.publish("humi",String(h).c_str(), true);
  }
}

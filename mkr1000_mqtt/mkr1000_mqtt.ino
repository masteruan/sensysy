/*
* Satellite
* 30 Maggio 2017
* TFL
* Arduino MKR 1000
*
* DHT-11 pin 5
* NO Photoresistor pin A0
* Gas pin A1
* Amps pin A2
* 
* Neopixel pin 3
* Relay pin 6
*
* */
#include "FastLED.h"
#include <PubSubClient.h>
#include "DHT.h"
#include <SPI.h>
#include <WiFi101.h>

// led
#define NUM_LEDS 1
#define DATA_PIN 3
CRGB leds[NUM_LEDS];

// dht
#define DHTPIN 5
#define DHTTYPE DHT11

// Update these with values suitable for your network.
const char* ssid = "TalentGarden";
const char* password = "Calabiana2017";
const char* mqtt_server = "10.13.2.45"; // Raspberry IP 192.168.0.102

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;
int builtinLed = 6;
int relay = 7;

DHT dht(DHTPIN, DHTTYPE);

// Photoresistor
const int photo = A0;
// Gas sensor
const int sensorGas = A1;
// Amp
const int sensorIn = A2;
int mVperAmp = 100; // use 100 for 20A Module and 66 for 30A Module
double Voltage = 0;
double VRMS = 0;
double AmpsRMS = 0;
int Watt = 0;

void setup() {
  pinMode(builtinLed, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  Serial.begin(9600);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  dht.begin();
  float t = dht.readTemperature();
  Serial.println(t);
  FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
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
  IPAddress ip = WiFi.localIP();
  Serial.println(ip);
  Serial.print("signal strength (RSSI):");
  Serial.print(WiFi.RSSI());
  Serial.println(" dBm");
  /*
  leds[0] = CRGB::Purple;
  FastLED.show();
  delay(500);
  // Now turn the LED off, then pause
  leds[0] = CRGB::Black;
  FastLED.show();
  delay(500);
  */
}
// if plus topic
// void callback(Sting topic, byte* payload, unsigned int length) {
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
    digitalWrite(builtinLed, HIGH);
    leds[0] = CRGB::Green;
    FastLED.show();
  }
  else if ((char)payload[0] == '2') {
    digitalWrite(relay, HIGH);
  }
  else if ((char )payload[0] == '3') {
    digitalWrite(relay, LOW);
  }
  else {
    digitalWrite(builtinLed, LOW);
    digitalWrite(relay, LOW);
    leds[0] = CRGB::Red;
    FastLED.show();
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

    // Amperometer
    Voltage = getVPP();
    VRMS = (Voltage/2.0) *0.707;
    AmpsRMS = ((VRMS * 1000)/mVperAmp) - 0.86; // Amp 0 - 20
    
    // Gas
    int aria = analogRead(sensorGas);
    aria = map(aria, 0, 1023, 10, 10000); // particolato g/1000000

    // Temperature
    float h = dht.readHumidity() - (h*0.15);
    float t = dht.readTemperature() - 5;
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
    client.publish("gas",String(aria).c_str(), true);
    client.publish("amp",String(AmpsRMS).c_str(), true);
    /*
    leds[0] = CRGB::Red;
    FastLED.show();
    delay(500);
    leds[0] = CRGB::Black;
    FastLED.show();
    */
  }
}
float getVPP()
{
  float result;

  int readValue;             //value read from the sensor
  int maxValue = 0;          // store max value here
  int minValue = 1024;          // store min value here

   uint32_t start_time = millis();
   while((millis()-start_time) < 1000) //sample for 1 Sec
   {
       readValue = analogRead(sensorIn);
       // see if you have a new maxValue
       if (readValue > maxValue)
       {
           /*record the maximum sensor value*/
           maxValue = readValue;
       }
       if (readValue < minValue)
       {
           /*record the maximum sensor value*/
           minValue = readValue;
       }
   }

   // Subtract min from max
   result = ((maxValue - minValue) * 5.0)/1024.0;

   return result;
 }

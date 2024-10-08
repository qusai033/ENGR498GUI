#include <WiFiNINA.h>
#include <RTCZero.h>
#include <SPI.h>
#include <SD.h> // Add the SD card library

#include <Arduino.h>
#include <PubSubClient.h>

#include "config.h"

// Function prototypes
void sampleData();
void printToSerial();
void dataToString();
void saveToSDCard(); // Function to save data to SD card

String dataString = "";
int readResolution = 12;
int analogPin = A1; // Use A1 for analog pin
int OutputPin = A5; // Use A5 for digital output pin
unsigned int sampleAmt = 499;
unsigned int sampleArray[499];
const int chipSelect = 4; // SD card chip select pin (adjust depending on your board)
int fileCounter = 0; // Counter to create unique filenames

void connectWiFi()
{
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.println("Connecting to WiFi..");
    WiFi.begin(SSID, PASSWORD);
    delay(500);
  }

  Serial.println("Connected!");
}

WiFiClient wifiClient;
PubSubClient client(wifiClient);

void reconnectMQTTClient()
{
  while (!client.connected())
  {
    Serial.print("Attempting MQTT connection...");

    if (client.connect(CLIENT_NAME.c_str()))
    {
      Serial.println("connected");
      client.subscribe(CLIENT_TELEMETRY_TOPIC.c_str());
    }
    else
    {
      Serial.print("Retrying in 5 seconds - failed, rc=");
      Serial.println(client.state());
      delay(5000);
    }
  }
}

void createMQTTClient()
{
  client.setServer(BROKER.c_str(), TCP_PORT);
  reconnectMQTTClient();
}

void setup()
{
  Serial.begin(9600);
  while (!Serial)
  {
    ;
  }

  connectWiFi();
  createMQTTClient();

  // Initialize the SD card
  if (!SD.begin(chipSelect))
  {
    Serial.println("SD card initialization failed!");
    return;
  }
  Serial.println("SD card initialized.");

  analogReference(AR_INTERNAL);
  analogReadResolution(readResolution);
  pinMode(OutputPin, OUTPUT);
}

void loop()
{
  reconnectMQTTClient();
  client.loop();

  sampleData();
  dataToString();
  printToSerial();
  saveToSDCard(); // Save the data to the SD card

  for (int j = 0; j < sampleAmt; j++)
  {
    float voltage = sampleArray[j] * (3.3 / 4096);
    String voltageStr = String(voltage);
    client.publish(CLIENT_TELEMETRY_TOPIC.c_str(), voltageStr.c_str());
  }

  exit(0); // Exiting loop, assuming you want to do this for testing purposes
}

void sampleData()
{
  digitalWrite(OutputPin, HIGH);
  delay(1000);
  digitalWrite(OutputPin, LOW);
  for (int i = 0; i < sampleAmt; i++)
  {
    sampleArray[i] = analogRead(analogPin);
  }
}

void printToSerial()
{
  for (int j = 0; j < sampleAmt; j++)
  {
    float voltage = sampleArray[j] * (3.3 / 4096);
    Serial.println(voltage);
  }
}

void dataToString()
{
  dataString = ""; // Clear the previous data
  for (int j = 0; j < sampleAmt; j++)
  {
    float voltage = sampleArray[j] * (3.3 / 4096);
    // Add unique identifier (e.g., timestamp or counter) to each entry
    dataString += String(j) + ";" + String(voltage) + ";" + millis() + "\n"; 
  }
}

// Function to save the sampled data to the SD card with a unique filename
void saveToSDCard(){
  // Generate a unique filename using a counter
  String filename = "data_" + String(fileCounter) + ".txt";
  fileCounter++; // Increment the counter for the next file

  // Open the file on the SD card
  File dataFile = SD.open(filename.c_str(), FILE_WRITE);

  if (dataFile) //if it open
  {
    dataFile.println(dataString); // Write the dataString to the file
    dataFile.close(); // Close the file
    Serial.println("Data saved to SD card: " + filename);
  }
  else
  {
    Serial.println("Error opening " + filename);
  }
}

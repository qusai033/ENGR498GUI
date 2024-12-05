
#include <WiFiNINA.h>
#include <RTCZero.h>
#include <SPI.h>
#include <SD.h>         // Add the SD card library
#include <WiFiClient.h> // WiFiClient for HTTP POST requests

#include <string.h>
#include <TimeLib.h>
#include <Wire.h>

// WiFi credentials
const char *SSID = "TP-Link_BE10";      // Your Wi-Fi SSID
const char *PASSWORD = "SensorLab123$"; // Your Wi-Fi password

// Server details
const char *SERVER_IP = "192.168.0.69";  // IP address of your Raspberry Pi
const int SERVER_PORT = 5000;            // Port of your Flask server
const char *UPLOAD_ENDPOINT = "/upload"; // Flask upload endpoint

const long bleedInterval = 20000;
unsigned long previousMillis = 0;
unsigned long currentMillis = 0;

uint8_t i = 0;
uint8_t sampleVal = 0;
uint8_t samplePeriod = 1; // microseconds (1us)
uint16_t sampleAmt = 499;
uint16_t sampleArray[499]; // Array that will contain sample data
// uint16_t sampleArrayInverse[500]; // Array that contains the inverse of the sampla data
uint32_t timeArray[499]; // Array that will contain the time of the sample data
uint32_t timeStart, timeFinish, timeTotal, dataTime, epochTime;
uint8_t sampleMinutes = 1;

// String for data
String dataString = "";

// Date and Time values
uint32_t epoch;

// ts_ stands for time stamp. These are
uint16_t ts_year;
uint16_t ts_month;
uint16_t ts_day;
uint16_t ts_hour;
uint16_t ts_minute;
uint16_t ts_second;

// Data File component to save to SD
File dataFile;
char fileName[13];

// Function prototypes
void sampleData();
void sampleDataToString();
void printDataString();
void getTime();
void DateTimeSD(uint16_t *date, uint16_t *time);
void saveDataSD();       // Function to save data to SD card
void sendFileToServer(); // Function to send data file to the server

// String dataString = "";
int readResolution = 12;
int analogPin = A1;       // Use A1 for analog pin
int OutputPin = A5;       // Use A5 for digital output pin
const int chipSelect = 4; // SD card chip select pin (adjust depending on your board)
int fileCounter = 0;      // Counter to create unique filenames

WiFiServer server(80); // Initialize WiFi server on port 80

void connectWiFi()
{
    while (WiFi.status() != WL_CONNECTED)
    {
        Serial.println("Connecting to WiFi...");
        WiFi.begin(SSID, PASSWORD);
        delay(500);
    }
    Serial.println("Connected to WiFi!");
}

WiFiClient client;

void setup()
{
    Serial.begin(9600);
    while (!Serial)
    {
        ; // Wait for serial port to connect
    }

    connectWiFi();

    // Start the WiFi server
    server.begin();

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
    // Check for incoming client connection
    WiFiClient client = server.available();
    if (client)
    {
        Serial.println("Client connected");

        // Read the HTTP request
        String request = client.readStringUntil('\r');
        client.flush();

        // Check for the "GET_DATA" command in the request
        if (request.indexOf("GET_DATA") != -1)
        {
            Serial.println("GET_DATA command received");

            // Execute data sampling, saving, and sending logic

            sampleData();
            sampleDataToString();
            printDataString();
            saveDataSD();

            sendFileToServer();

            // Respond to the client
            client.println("HTTP/1.1 200 OK");
            client.println("Content-Type: csv/plain");
            client.println();
            client.println("Data sampling and upload complete!");
        }
        else
        {
            // Respond with a default message for other requests
            client.println("HTTP/1.1 400 Bad Request");
            client.println("Content-Type: csv/plain");
            client.println();
            client.println("Invalid command");
        }

        client.stop(); // Close the connection
        Serial.println("Client disconnected");
    }
}

// Function to sample data
void sampleData()
{ // This function pulses in 3.3 volts into the capactitor then samples the decaying voltage into an array, takes readings from the analog pin, and saves that data into an array

    digitalWrite(OutputPin, HIGH);
    delay(1000);
    digitalWrite(OutputPin, LOW);

    timeStart = micros();
    for (int i = 0; i < sampleAmt; i++)
    { // This takes the readings from the analog pin and puts it in an array

        timeFinish = micros();
        timeTotal = timeFinish - timeStart;
        timeArray[i] = timeTotal;
        sampleArray[i] = analogRead(analogPin);
    }

    Serial.println("data sampled.");
}

// Function to convert data to a CSV string
void sampleDataToString()
{ // This function parses the sample and time arrays and formats them into a string.

    dataString = "";

    dataString += "Voltage,Time\n"; // Add header (Time in seconds)

    for (int i = 0; i < sampleAmt; i++)
    {
        float voltage = sampleArray[i] * (3.3 / 1023.0);
        // float voltageInverse = 1 / voltage;
        dataTime = timeArray[i];

        dataString += voltage;
        dataString += ",";
        dataString += dataTime;
        dataString += "\n";
    }

    Serial.println("data to string");
}

void printDataString()
{
    // Ensure dataString has content before trying to print
    if (dataString.length() == 0)
    {
        Serial.println("No data to print. Please generate dataString first.");
        return;
    }

    String line = ""; // Temporary variable to store each line

    // Loop through dataString and parse it line by line
    for (int i = 0; i < dataString.length(); i++)
    {
        char c = dataString[i]; // Get each character

        if (c == '\n') // Newline detected, print the line
        {
            Serial.println(line); // Print the current line
            line = "";            // Reset for the next line
        }
        else
        {
            line += c; // Append character to the current line
        }
    }

    // Print any remaining line if it doesn't end with a newline
    if (line.length() > 0)
    {
        Serial.println(line);
    }
}

void getTime()
{ // This function takes the epoch time from WiFi and then grabs the date and time from that

    epochTime = WiFi.getTime();

    // Adjust time to your local timezone (7 hours before GMT)
    epochTime = epochTime - (7 * 60 * 60); // Subtract 7 hours in seconds

    ts_year = year(epochTime);
    ts_month = month(epochTime);
    ts_day = day(epochTime);
    ts_hour = hour(epochTime);
    ts_minute = minute(epochTime);
    ts_second = second(epochTime);

    sprintf(fileName, "%02d%02d%02d%02d.csv", ts_month, ts_day, ts_hour, ts_minute);

    Serial.println(fileName);
}

// Function to save the sampled data to the SD card as a .csv file
void saveDataSD()
{
    Serial.println("Entering saveDataSD...");

    getTime(); // Ensure timestamp variables are set correctly
    SdFile::dateTimeCallback(DateTimeSD);

    // sprintf(fileName, "LOG%02d%02d.csv", ts_hour, ts_minute); // Use a simple filename
    Serial.println("Generated filename: " + String(fileName));

    if (dataString.length() == 0)
    {
        Serial.println("dataString is empty. No data to save.");
        return;
    }

    File dataFile = SD.open(fileName, FILE_WRITE);
    if (dataFile)
    {
        Serial.println("File opened successfully for writing.");
        dataFile.println(dataString); // Write data to the file
        dataFile.close();             // Close the file
        Serial.println("Data saved to SD card as: " + String(fileName));
    }
    else
    {
        Serial.println("Failed to open file for writing.");
    }

    Serial.println("Exiting saveDataSD...");
}

void DateTimeSD(uint16_t *date, uint16_t *time)
{ // This function adds a timestamp to the file that Windows will display in the file information

    *date = FAT_DATE(ts_year, ts_month, ts_day);
    *time = FAT_TIME(ts_hour, ts_minute, ts_second);
}

// Function to send the .csv file to the server
void sendFileToServer()
{

    File dataFile = SD.open(fileName); // Use the filename generated during saveDataSD

    if (!dataFile)
    {
        Serial.println("Failed to open file for sending: " + String(fileName));
        return;
    }

    unsigned long contentLength = dataFile.size(); // Get file size
    Serial.print("File size (Content-Length): ");
    Serial.println(contentLength);

    if (client.connect(SERVER_IP, SERVER_PORT))
    {
        Serial.println("Connected to server, sending file...");

        // HTTP POST request
        client.println("POST " + String(UPLOAD_ENDPOINT) + " HTTP/1.1");
        client.println("Host: " + String(SERVER_IP));
        client.println("Content-Type: csv");
        client.print("Content-Length: ");
        client.println(contentLength);
        client.println("Connection: close");
        client.println();

        // Send the file content in chunks
        const int bufferSize = 64; // Adjust buffer size based on memory constraints
        char buffer[bufferSize];
        while (dataFile.available())
        {
            int bytesRead = dataFile.read(buffer, bufferSize);
            client.write(buffer, bytesRead);
            delay(10);
        }

        dataFile.close(); // Close the file after sending
        Serial.println("File content sent");

        // Read and print server response
        while (client.connected())
        {
            if (client.available())
            {
                String response = client.readStringUntil('\n');
                Serial.println("Server response: " + response);
            }
        }

        client.stop(); // Close the connection
        delay(1000);
    }
    else
    {
        Serial.println("Connection to server failed");
    }
}

// 192.168.0.158 (Arduino)
// 192.168.0.69  (Odyssey)

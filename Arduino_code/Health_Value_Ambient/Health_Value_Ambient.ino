#include <FastLED.h>
#include <ESP8266WiFi.h>
#include <espnow.h>

// How many leds in your strip?
#define NUM_LEDS 13

#define DATA_PIN 4
#define CLOCK_PIN 13

// Define the array of leds
CRGB leds[NUM_LEDS];

boolean trigger = false;

int red = 0;
int green = 255;
int blue = 0;

int currentHealth = 0;
// Structure example to receive data
// Must match the sender structure
typedef struct healthStruct {
    int health;
} hs;

// Create a struct_message
hs health_S;

// Callback function that will be executed when data is received
void OnDataRecv(uint8_t * mac, uint8_t *incomingData, uint8_t len) {
  memcpy(&health_S, incomingData, sizeof(health_S));
  currentHealth  = health_S.health;
  Serial.println("REC data");
  Serial.println(health_S.health);
  trigger = true; 
}
 

void setup() { 
     Serial.begin(115200);
     FastLED.addLeds<UCS1903, DATA_PIN, BRG>(leds, NUM_LEDS);
       // Turn the LED on, then pause
     GreenToRedGradient(100);
     FastLED.show();
     WiFi.mode(WIFI_STA);
     WiFi.disconnect();        // we do not want to connect to a WiFi network

  if(esp_now_init() != 0) {
    Serial.println("ESP-NOW initialization failed");
    return;
  }

  esp_now_register_recv_cb(OnDataRecv);   // this function will get called once all data is sent

  Serial.println("Initialized.");
}

void loop() { 

  if(trigger)
  {
     GreenToRedGradient(currentHealth);
     FastLED.show();
     delay(10);
     trigger = false;
  }
}

void GreenToRedGradient(double percentage)
{
    red = 255*(100-percentage)/100;
    green = 255*(percentage/100);
    blue = 0;
    for(int i = 0; i < 13; i++)
    {
      leds[i].red   = red;
      leds[i].green = green;
      leds[i].blue  = blue;
    }
}

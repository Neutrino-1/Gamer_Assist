#include <ESP8266WiFi.h>
#include <espnow.h>
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define RING_DI_PIN 5
#define HAPTIC_MOTOR_1 2
#define HAPTIC_MOTOR_2 4

Adafruit_NeoPixel ring = Adafruit_NeoPixel(16, RING_DI_PIN, NEO_GRB + NEO_KHZ800);

boolean triggerRing = false;
int previousHealth = 0;
int currentHealth = 0;
int damage = 0;

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
  triggerRing = true; 
}
 

void setup() {

  pinMode(HAPTIC_MOTOR_1,OUTPUT);
  pinMode(HAPTIC_MOTOR_2,OUTPUT);
  digitalWrite(HAPTIC_MOTOR_1,HIGH);

  Serial.begin(115200);
  ring.begin();
  ring.setBrightness(25);
  ring.show(); // Initialize all pixels to 'off'
  
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
  
  colorWipe(ring.Color(0, 0, 255), 20); // Red 
  if(triggerRing)
  {
    damage = abs(previousHealth - currentHealth);
    
    //HealthRegenration
    if(previousHealth < currentHealth && previousHealth != 0)
    {
      analogWrite(HAPTIC_MOTOR_1,220);
      analogWrite(HAPTIC_MOTOR_2,220);
      colorWipe(ring.Color(0, 255, 0), damage); // Green
      digitalWrite(HAPTIC_MOTOR_1,HIGH);
      digitalWrite(HAPTIC_MOTOR_2,LOW);
    }
    else if(currentHealth < previousHealth)
    {
      analogWrite(HAPTIC_MOTOR_1,150);
      analogWrite(HAPTIC_MOTOR_2,150);
      colorWipe(ring.Color(255, 0, 0), damage); // Red 
      digitalWrite(HAPTIC_MOTOR_2,LOW);
      digitalWrite(HAPTIC_MOTOR_1,HIGH);
    }
    previousHealth = currentHealth;
    triggerRing = false;
  }
  
}

// Fill the dots one after the other with a color
void colorWipe(uint32_t c, uint8_t wait) {
  for(uint16_t i=0; i<ring.numPixels(); i++) {
    ring.setPixelColor(i, c);
    ring.show();
    delay(wait);
  }
}

void rainbow(uint8_t wait) {
  uint16_t i, j;

  for(j=0; j<256; j++) {
    for(i=0; i<ring.numPixels(); i++) {
      ring.setPixelColor(i, Wheel((i+j) & 255));
    }
    ring.show();
    delay(wait);
  }
}

uint32_t Wheel(byte WheelPos) {
  WheelPos = 255 - WheelPos;
  if(WheelPos < 85) {
    return ring.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  }
  if(WheelPos < 170) {
    WheelPos -= 85;
    return ring.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
  WheelPos -= 170;
  return ring.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
}

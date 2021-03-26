#include <ESP8266WiFi.h>
#include <espnow.h>

// REPLACE WITH RECEIVER MAC Address
uint8_t ringAddress[] = {0xBC, 0xDD, 0xC2, 0x5C, 0x68, 0xC2}; //  BC:DD:C2:5C:68:C2
uint8_t stripAddress[] = {0x48, 0x3F, 0xDa, 0x05, 0xC8, 0xFB}; //48:3F:DA:05:C8:FB

// Structure example to send data
// Must match the receiver structure
typedef struct healthStruct {
    int health;
} hs;

// Create a struct_message
hs health_s;

// Callback when data is sent
void OnDataSent(uint8_t *mac_addr, uint8_t sendStatus) {
  Serial.print("Last Packet Send Status: ");
  if (sendStatus == 0){
    Serial.println("Delivery success");
    digitalWrite(2,LOW);
    delay(1000);
    digitalWrite(2,HIGH);
  }
  else{
    Serial.println("Delivery fail");
  }
}
 
void setup() {
  // Init Serial Monitor
  Serial.begin(115200);
  // Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  // Init ESP-NOW
  if (esp_now_init() != 0) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  esp_now_set_self_role(ESP_NOW_ROLE_CONTROLLER);   
  esp_now_register_send_cb(OnDataSent);   // this function will get called once all data is sent
  esp_now_add_peer(ringAddress, ESP_NOW_ROLE_SLAVE, 1, NULL, 0);
  esp_now_add_peer(stripAddress, ESP_NOW_ROLE_SLAVE, 1, NULL, 0);

  Serial.println("Initialized.");
}
 
void loop() {
  if (Serial.available()) {
    digitalWrite(2,LOW);
    String data = Serial.readString();
    int healthValue = data.toInt();
    health_s.health = healthValue; 
    delay(1000);
    // Send message via ESP-NOW
    esp_now_send(ringAddress, (uint8_t *) &health_s, sizeof(health_s));
    esp_now_send(stripAddress, (uint8_t *) &health_s, sizeof(health_s));
    digitalWrite(2,HIGH);
  }
}

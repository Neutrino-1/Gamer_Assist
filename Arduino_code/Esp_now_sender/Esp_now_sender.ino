#include <ESP8266WiFi.h>
#include <espnow.h>

// REPLACE WITH RECEIVER MAC Address
uint8_t receiverAddress[] = {0x84, 0xCC, 0xA8, 0x83, 0x76, 0xBE}; // 84:CC:A8:83:76:BE

// Structure example to send data
// Must match the receiver structure
typedef struct struct_message {
    uint8_t healthValue;
} message;

// Create a struct_message called myData
message msg;


// Callback when data is sent
void OnDataSent(uint8_t *mac_addr, uint8_t sendStatus) {
  Serial.print("Last Packet Send Status: ");
  if (sendStatus == 0){
    Serial.println("Delivery success");
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
  esp_now_add_peer(receiverAddress, ESP_NOW_ROLE_SLAVE, 1, NULL, 0);

  Serial.println("Initialized.");
}
 
void loop() {
  if(Serial.available())
  {
     String data = Serial.readString();
     uint8_t healthValue = data.toInt();
     msg.healthValue = healthValue;
     // Send message via ESP-NOW 
     esp_now_send(receiverAddress, (uint8_t *) &msg, sizeof(msg));
     delay(10);
  }  
}

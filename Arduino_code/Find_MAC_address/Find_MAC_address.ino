#include <ESP8266WiFi.h>

void setup(){
  pinMode(2,OUTPUT);
  digitalWrite(2,HIGH);
  Serial.begin(115200);
  Serial.println();
  Serial.print("ESP8266 Board MAC Address:  ");
}
 
void loop(){
    Serial.println(WiFi.macAddress());
    delay(3000);
}

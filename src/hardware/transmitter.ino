#include <SPI.h>
#include <LoRa.h>


#define SS_PIN     10
#define RST_PIN     9
#define DIO0_PIN    2    


#define MAX_PACKET_SIZE 200   
#define PACKET_DELAY    300   

String inputMessage = "";
bool newData = false;

void setup() {
  Serial.begin(9600);
  while (!Serial);

  Serial.println("LoRa TX - type and hit Enter.");

  pinMode(RST_PIN, OUTPUT);
  pinMode(DIO0_PIN, INPUT);   

  
  while (!initLoRa()) {
    Serial.println("Init failed - retry in 2s");
    delay(2000);
  }
  Serial.println("LoRa OK!");
}

bool initLoRa() {
  digitalWrite(RST_PIN, LOW);  delay(10);
  digitalWrite(RST_PIN, HIGH); delay(10);
  LoRa.setPins(SS_PIN, RST_PIN, DIO0_PIN);
  if (!LoRa.begin(433E6)) return false;
  LoRa.setTxPower(17);
  LoRa.setSpreadingFactor(7);
  LoRa.setSyncWord(0x34);
  return true;
}

void loop() {
 
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') newData = true;
    else          inputMessage += c;
  }

  if (newData) {
    int len = inputMessage.length();
    int pktCount = (len + MAX_PACKET_SIZE - 1) / MAX_PACKET_SIZE;

    Serial.print("Msg ");
    Serial.print(len);
    Serial.print(" B → ");
    Serial.print(pktCount);
    Serial.println(" packets.");

 
    LoRa.beginPacket();
      LoRa.write('H');
      LoRa.write(pktCount);
    LoRa.endPacket();               
    waitForTxDone();
    delay(PACKET_DELAY);

 
    for (int i = 0; i < pktCount; i++) {
      int start = i * MAX_PACKET_SIZE;
      int end   = min((i+1)*MAX_PACKET_SIZE, len);
      String chunk = inputMessage.substring(start, end);
      Serial.print("Pkt ");
      Serial.print(i+1);
      Serial.print("/");
      Serial.print(pktCount);
      Serial.print(" (");
      Serial.print(end - start);
      Serial.println(" B)");

      LoRa.beginPacket();
        LoRa.write('D');
        LoRa.write(i);
        LoRa.print(chunk);
      LoRa.endPacket();             
      waitForTxDone();
      delay(PACKET_DELAY);
    }

    Serial.println("Done.");
    inputMessage = "";
    newData = false;
  }
}


void waitForTxDone() {
  unsigned long start = millis();
  while (digitalRead(DIO0_PIN) == LOW) {
    // timeout fallback
    if (millis() - start > 2000) break;
  }
}

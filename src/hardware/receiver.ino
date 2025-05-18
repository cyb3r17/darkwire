#include <SPI.h>
#include <LoRa.h>


#define SS_PIN 10
#define RST_PIN 9
#define DIO0_PIN 2


#define MAX_PACKETS 8    
#define BUFFER_SIZE 256  

uint8_t packetReceived = 0;  
uint8_t expectedPacketCount = 0;
uint8_t receivedPacketCount = 0;
bool messageInProgress = false;
char buffer[BUFFER_SIZE];    

void resetMessageAssembly() {
  packetReceived = 0;
  expectedPacketCount = 0;
  receivedPacketCount = 0;
  messageInProgress = false;
}

void setup() {
  Serial.begin(9600);
  Serial.println(F("LoRa Receiver"));
  
  
  while (true) {
    pinMode(RST_PIN, OUTPUT);
    digitalWrite(RST_PIN, LOW); delay(10);
    digitalWrite(RST_PIN, HIGH); delay(10);
    
    LoRa.setPins(SS_PIN, RST_PIN, DIO0_PIN);
    if (LoRa.begin(433E6)) break;
    
    Serial.println(F("Init failed. Retry..."));
    delay(2000);
  }
  
  LoRa.setSpreadingFactor(7);
  LoRa.setSyncWord(0x34);
  resetMessageAssembly();
}

void loop() {
  int packetSize = LoRa.parsePacket();
  if (!packetSize) return;
  
  char packetType = LoRa.read();
  
  if (packetType == 'H') {
 
    uint8_t count = LoRa.read();
    if (count > MAX_PACKETS) {
      Serial.println(F("Error: Too many packets"));
      return;
    }
    
    resetMessageAssembly();
    expectedPacketCount = count;
    messageInProgress = true;
    
    Serial.print(F("New msg: "));
    Serial.print(count);
    Serial.println(F(" packets"));
  } 
  else if (packetType == 'D' && messageInProgress) {
 
    uint8_t packetIndex = LoRa.read();
    
    if (packetIndex >= expectedPacketCount) {
      Serial.println(F("Invalid packet index"));
      return;
    }
    
   
    if (packetReceived & (1 << packetIndex)) {
      Serial.println(F("Duplicate packet"));
      return;
    }
    
   
    int bytesRead = 0;
    memset(buffer, 0, BUFFER_SIZE);
    
    while (LoRa.available() && bytesRead < BUFFER_SIZE-1) {
      buffer[bytesRead++] = LoRa.read();
    }
    buffer[bytesRead] = '\0';
    
   
    packetReceived |= (1 << packetIndex);
    receivedPacketCount++;
    
 
    Serial.print(F("P"));
    Serial.print(packetIndex + 1);
    Serial.print(F("/"));
    Serial.print(expectedPacketCount);
    Serial.print(F(": "));
    Serial.println(buffer);
    
   
    if (receivedPacketCount >= expectedPacketCount) {
      Serial.println(F("\n--- MESSAGE COMPLETE ---"));
      resetMessageAssembly();
    }
  }
}
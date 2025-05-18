#include <SPI.h>
#include <LoRa.h>


// beta testing???


#define SS_PIN     10
#define RST_PIN     9
#define DIO0_PIN    2


#define MAX_PACKET_SIZE 200
#define PACKET_DELAY    300
#define MAX_PACKETS     8
#define BUFFER_SIZE     256


#define RELAY_DELAY     500 
#define NODE_ID         1   


uint8_t packetReceived = 0;  
uint8_t expectedPacketCount = 0;
uint8_t receivedPacketCount = 0;
bool messageInProgress = false;
char messageBuffer[MAX_PACKETS][BUFFER_SIZE];  
uint8_t chunkSizes[MAX_PACKETS];               


String inputMessage = "";
bool newData = false;


#define DEBUG true

void setup() {
  Serial.begin(9600);
  while (!Serial && millis() < 5000);  

  if (DEBUG) Serial.println("LoRa Transceiver - Relay Node");

  pinMode(RST_PIN, OUTPUT);
  pinMode(DIO0_PIN, INPUT);

// lora init
  while (!initLoRa()) {
    if (DEBUG) Serial.println("Init failed - retry in 2s");
    delay(2000);
  }
  
  if (DEBUG) Serial.println("LoRa initialization OK!");
  resetMessageAssembly();
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

  receiveMessage();
  
 
  readSerialInput();
  
  
  if (receivedPacketCount >= expectedPacketCount && messageInProgress) {
    if (DEBUG) Serial.println("Message complete - forwarding...");
    forwardReceivedMessage();
    resetMessageAssembly();
  }
  
  
  if (newData) {
    transmitMessage(inputMessage);
    inputMessage = "";
    newData = false;
  }
}

void receiveMessage() {
  int packetSize = LoRa.parsePacket();
  if (!packetSize) return;
  
  char packetType = LoRa.read();
  
  if (packetType == 'H') {
    
    uint8_t count = LoRa.read();
    uint8_t sourceID = LoRa.read(); 
    
    
    if (sourceID == NODE_ID) {
      return;
    }
    
    if (count > MAX_PACKETS) {
      if (DEBUG) Serial.println("Error: Too many packets");
      return;
    }
    
    resetMessageAssembly();
    expectedPacketCount = count;
    messageInProgress = true;
    
    if (DEBUG) {
      Serial.print("New message: ");
      Serial.print(count);
      Serial.println(" packets");
    }
  } 
  else if (packetType == 'D' && messageInProgress) {
    
    uint8_t packetIndex = LoRa.read();
    
    if (packetIndex >= expectedPacketCount) {
      if (DEBUG) Serial.println("Invalid packet index");
      return;
    }
    
   
    if (packetReceived & (1 << packetIndex)) {
      if (DEBUG) Serial.println("Duplicate packet");
      return;
    }
    
   
    int bytesRead = 0;
    memset(messageBuffer[packetIndex], 0, BUFFER_SIZE);
    
    while (LoRa.available() && bytesRead < BUFFER_SIZE-1) {
      messageBuffer[packetIndex][bytesRead++] = LoRa.read();
    }
    messageBuffer[packetIndex][bytesRead] = '\0';
    chunkSizes[packetIndex] = bytesRead;
    
    
    packetReceived |= (1 << packetIndex);
    receivedPacketCount++;
    
    if (DEBUG) {
      Serial.print("Received P");
      Serial.print(packetIndex + 1);
      Serial.print("/");
      Serial.print(expectedPacketCount);
      Serial.print(" (");
      Serial.print(bytesRead);
      Serial.println(" bytes)");
    }
  }
}

void forwardReceivedMessage() {
  if (DEBUG) Serial.println("Forwarding message...");
  

  LoRa.beginPacket();
    LoRa.write('H');
    LoRa.write(expectedPacketCount);
    LoRa.write(NODE_ID);  
  LoRa.endPacket();
  waitForTxDone();
  delay(PACKET_DELAY);
  

  for (int i = 0; i < expectedPacketCount; i++) {
  
    if (packetReceived & (1 << i)) {
      if (DEBUG) {
        Serial.print("Forwarding P");
        Serial.print(i + 1);
        Serial.print("/");
        Serial.println(expectedPacketCount);
      }
      
      LoRa.beginPacket();
        LoRa.write('D');
        LoRa.write(i);
        for (int j = 0; j < chunkSizes[i]; j++) {
          LoRa.write(messageBuffer[i][j]);
        }
      LoRa.endPacket();
      waitForTxDone();
      delay(PACKET_DELAY);
    }
  }
  
 
  Serial.println("\n--- RELAYED MESSAGE ---");
  for (int i = 0; i < expectedPacketCount; i++) {
    if (packetReceived & (1 << i)) {
      Serial.print(messageBuffer[i]);
    }
  }
  Serial.println("\n---------------------");
}

void readSerialInput() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      newData = true;
    } else {
      inputMessage += c;
    }
  }
}

void transmitMessage(String message) {
  int len = message.length();
  int pktCount = (len + MAX_PACKET_SIZE - 1) / MAX_PACKET_SIZE;
  
  if (DEBUG) {
    Serial.print("Transmitting message: ");
    Serial.print(len);
    Serial.print(" bytes → ");
    Serial.print(pktCount);
    Serial.println(" packets.");
  }
  
  
  LoRa.beginPacket();
    LoRa.write('H');
    LoRa.write(pktCount);
    LoRa.write(NODE_ID);  
  LoRa.endPacket();
  waitForTxDone();
  delay(PACKET_DELAY);
  

  for (int i = 0; i < pktCount; i++) {
    int start = i * MAX_PACKET_SIZE;
    int end = min((i+1) * MAX_PACKET_SIZE, len);
    String chunk = message.substring(start, end);
    
    if (DEBUG) {
      Serial.print("Sending P");
      Serial.print(i+1);
      Serial.print("/");
      Serial.print(pktCount);
      Serial.print(" (");
      Serial.print(end - start);
      Serial.println(" bytes)");
    }
    
    LoRa.beginPacket();
      LoRa.write('D');
      LoRa.write(i);
      LoRa.print(chunk);
    LoRa.endPacket();
    waitForTxDone();
    delay(PACKET_DELAY);
  }
  
  if (DEBUG) Serial.println("Transmission complete.");
}

void resetMessageAssembly() {
  packetReceived = 0;
  expectedPacketCount = 0;
  receivedPacketCount = 0;
  messageInProgress = false;
}

void waitForTxDone() {
  unsigned long start = millis();
  while (digitalRead(DIO0_PIN) == LOW) {
    // timeout fallback after 2 seconds
    if (millis() - start > 2000) break;
  }
}
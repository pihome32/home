// Feather9x_RX
// -*- mode: C++ -*-
// Example sketch showing how to create a simple messaging client (receiver)
// with the RH_RF95 class. RH_RF95 class does not provide for addressing or
// reliability, so you should only use RH_RF95 if you do not need the higher
// level messaging abilities.
// It is designed to work with the other example Feather9x_TX

#include <SPI.h>
#include <RH_RF95.h>

/* for Feather32u4 RFM9x*/
#define RFM95_CS 8
#define RFM95_RST 4
#define RFM95_INT 7


#define RF95_FREQ 868.0

// Singleton instance of the radio driver
RH_RF95 rf95(RFM95_CS, RFM95_INT);

#define LED 13

int buzPin = 12;
bool buzzerState = 0;
long buzzerMillis = 0;
long buzzerIntON = 10; 
long buzzerIntOFF = 100; 
bool buzzerON = 0;


void setup()
{
  pinMode(LED, OUTPUT);
<<<<<<< HEAD
  pinMode(buzPin, OUTPUT);
  digitalWrite(buzPin, HIGH);
=======

>>>>>>> 2bde3c6ec60451449ffb7233b7066616aabd910e
  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);

  Serial.begin(115200);
  while (!Serial) {
    delay(1);
  }
  delay(100);


  // manual reset
  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);

  while (!rf95.init()) {
    //Serial.println("LoRa radio init failed");
    while (1);
  }
  if (!rf95.setFrequency(RF95_FREQ)) {
    Serial.println("setFrequency failed");
    while (1);
  }
  rf95.setTxPower(23, false);
}

int counter = 0;

void loop()
{

<<<<<<< HEAD
  checkMessage();
  buzzer();
  checkLoraMessage();

}

void buzzer(){
  if (buzzerState== 1) {
    unsigned long currentMillis = millis();
    if (buzzerON==0) {
      if(currentMillis - buzzerMillis > buzzerIntOFF) {
        buzzerMillis=currentMillis;
        digitalWrite(buzPin,LOW);
        buzzerON=1;        } 
        } 
    else {
        if(currentMillis - buzzerMillis > buzzerIntON) {
          digitalWrite(buzPin,HIGH);
          buzzerMillis=currentMillis;
          buzzerON=0; }
        } }
  else {
    digitalWrite(buzPin,HIGH);  }
}

void checkMessage() {
  String command;
  if (Serial.available() > 0) {
      // read the incoming byte:
      command = Serial.readStringUntil("/n");
      if (command=="buzzerON"){
        buzzerState=1;
        buzzerMillis=millis();
        
      } 
      if (command=="buzzerOFF"){
        buzzerState=0;        
      }
    }
  
}

void checkLoraMessage() {
    if (rf95.available())
=======
  if (rf95.available())
>>>>>>> 2bde3c6ec60451449ffb7233b7066616aabd910e
  {
    // Should be a message for us now
    uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
    uint8_t len = sizeof(buf);

    if (rf95.recv(buf, &len))
    {
      digitalWrite(LED, HIGH);
      /*RH_RF95::printBuffer("Received: ", buf, len);*/
       String recieveData;
       String rssi;
       rssi=(rf95.lastRssi());
      recieveData = rssi + ",";
      recieveData = recieveData + (char*)buf;
      recieveData = recieveData ;
      sendBack((char*)buf);
      //Serial.println((char*)buf );
      Serial.println(recieveData);
      digitalWrite(LED, LOW);
    }
    else
    {
      Serial.println("Receive failed");
    }
  }
<<<<<<< HEAD
}

void sendBack(String data) {
  char radiopacket[1024];
  strcpy(radiopacket, data.c_str());
  delay(10);
  rf95.send((uint8_t *)radiopacket, 100);
  rf95.waitPacketSent();
  rf95.sleep();
=======
>>>>>>> 2bde3c6ec60451449ffb7233b7066616aabd910e
}
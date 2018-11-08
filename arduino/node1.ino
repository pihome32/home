// Feather9x_TX
// -*- mode: C++ -*-
// Example sketch showing how to create a simple messaging client (transmitter)
// with the RH_RF95 class. RH_RF95 class does not provide for addressing or
// reliability, so you should only use RH_RF95 if you do not need the higher
// level messaging abilities.
// It is designed to work with the other example Feather9x_RX
#include <OneWire.h>
#include <SPI.h>
#include "RH_RF95.h"
#include "Adafruit_SleepyDog.h"
/* for feather32u4 7*/

#define RFM95_CS 8
#define RFM95_RST 4
#define RFM95_INT 7
#define VBATPIN A9
OneWire  ds(10);  // on pin 10 (a 4.7K resistor is necessary)
#if defined(ESP8266)
  /* for ESP w/featherwing */ 
  #define RFM95_CS  2    // "E"
  #define RFM95_RST 16   // "D"
  #define RFM95_INT 15   // "B"

#elif defined(ESP32)  
  /* ESP32 feather w/wing */
  #define RFM95_RST     27   // "A"
  #define RFM95_CS      33   // "B"
  #define RFM95_INT     12   //  next to A

#elif defined(NRF52)  
  /* nRF52832 feather w/wing */
  #define RFM95_RST     7   // "A"
  #define RFM95_CS      11   // "B"
  #define RFM95_INT     31   // "C"
  
#elif defined(TEENSYDUINO)
  /* Teensy 3.x w/wing */
  #define RFM95_RST     9   // "A"
  #define RFM95_CS      10   // "B"
  #define RFM95_INT     4    // "C"
#endif


// Change to 434.0 or other frequency, must match RX's freq!
#define RF95_FREQ 868.0

// Singleton instance of the radio driver
RH_RF95 rf95(RFM95_CS, RFM95_INT);

void setup() 
{
  pinMode(13, OUTPUT);
  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);

 /* Serial.begin(115200);
  while (!Serial) {
    delay(1);
  }*/

  delay(5000);

  /*Serial.println("Feather LoRa TX Test!");*/

  // manual reset
  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);

  while (!rf95.init()) {
   /* Serial.println("LoRa radio init failed");*/
    while (1);
  }
  /*Serial.println("LoRa radio init OK!");*/

  // Defaults after init are 434.0MHz, modulation GFSK_Rb250Fd250, +13dbM
  if (!rf95.setFrequency(RF95_FREQ)) {
    /*Serial.println("setFrequency failed");*/
    while (1);
  }
  /*Serial.print("Set Freq to: "); Serial.println(RF95_FREQ);*/
  
  // Defaults after init are 434.0MHz, 13dBm, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on

  // The default transmitter power is 13dBm, using PA_BOOST.
  // If you are using RFM95/96/97/98 modules which uses the PA_BOOST transmitter pin, then 
  // you can set transmitter powers from 5 to 23 dBm:
  rf95.setTxPower(5, false);
}

int16_t packetnum = 0;  // packet counter, we increment per xmission

void loop()
{
  
  digitalWrite(13, HIGH); 

  float measuredvbat = analogRead(VBATPIN);
  measuredvbat *= 2;    // we divided by 2, so multiply back
  measuredvbat *= 3.3;  // Multiply by 3.3V, our reference voltage
  measuredvbat /= 1024; // convert to voltage
  
  /*Serial.println("Transmitting..."); // Send a message to rf95_server*/
  String sendpacket;
 sendpacket="1,0," + String(measuredvbat);

 char radiopacket[1024];
 strcpy(radiopacket, sendpacket.c_str());
 /*char radiopacket[20] = sendpacket;*/
  /*itoa(packetnum++, radiopacket+13, 10);*/
 
  //radiopacket[19] = 0;
  
  //Serial.print(sizeof(radiopacket));
  delay(10);
  rf95.send((uint8_t *)radiopacket, 100);


  rf95.waitPacketSent();
  digitalWrite(13, LOW);
  //delay(3000);
  rf95.sleep();
  Watchdog.sleep(10000);
}

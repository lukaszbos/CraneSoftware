#include <Arduino.h>
#include "test.h"


int sensorValue = 0;
int sensorValue2 = 0;
void setup() {
 Serial.begin(115200);
 //test();
 //klasowyTekst();
}
void loop() {
  
 sensorValue = analogRead(A0);
 //Serial.print("First value: ");
 Serial.println(sensorValue);
 //sensorValue2 = analogRead(A1);
// Serial.print("Second value: ");
 //Serial.println(sensorValue2);
 delay(100);
 
}

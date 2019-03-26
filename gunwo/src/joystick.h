/*
 * This file contains joystick controller methods
 *
 */
 ////JOYSTICK CANT SEE  3
#include <Arduino.h>

int sensorValue;
int outputValue;

//returns value read from analog pin
int getGear(const int analogPin){
  sensorValue = analogRead(analogPin); // read the input on analog pin A0
  outputValue = map(sensorValue,  0, 1000, -3, 3); // mapping sensor value to scale from -3 to 3
  return outputValue;

  // print out the value you read:
  //Serial.println(sensorValue);
  //sensorValue2 = analogRead(A1);
  // Serial.print("Second value: ");
  //Serial.println(sensorValue2);
  //delay(100);
}

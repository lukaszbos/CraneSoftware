#include "Joystick.h"


//returns value read from analog pin
  int Joystick::getGear(const int analogPin){
  int sensorValue;
  int outputValue;

  sensorValue = analogRead(analogPin); // read the input on analog pin A0
  outputValue = map(sensorValue,  0, 900, MIN_GEAR, MAX_GEAR); // mapping sensor value to scale from -3 to 3
                                                              // skalling from 0 to 900 not 1023 becouse of the problems with 0 Gear
  return outputValue;

  // print out the value you read:
  //Serial.println(sensorValue);
  //sensorValue2 = analogRead(A1);
  // Serial.print("Second value: ");
  //Serial.println(sensorValue2);
  //delay(100);
}

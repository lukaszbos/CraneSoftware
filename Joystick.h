/*
 * This file contains joystick controller methods
 * 
 */

//returns value read from analog pin
int getVoltage(int analogPin){
  // read the input on analog pin 0:
  int sensorValue = analogRead(analogPin); // read the input pin
  return sensorValue; 
  
  // print out the value you read:
  //Serial.println(sensorValue);
  //sensorValue2 = analogRead(A1);
  // Serial.print("Second value: ");
  //Serial.println(sensorValue2);
  //delay(100);
}

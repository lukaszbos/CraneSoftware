/*
 * The less code in this file, the better 
 * Try to create methods in .h files and only call them here
 * One sensor = one .h file ? 
 * You should also comment your code so others can easily understand it
 * 
 */

 

#include <Arduino.h>
#include "StepperMotor28BYJ48.h"
#include "Joystick.h"

const byte analogPin = A0;     // potentiometer wiper (middle terminal) connected to analog pin A0
                       // outside leads to ground and +5V

void setup() {
	Serial.begin(9600);
	setupStepper28BYJ48(); 
}

void loop() {
	Serial.println(getVoltage(analogPin)); //  testing if joystick's potentiometer works  
  changeDirectionOfStepper28BYJ48(getVoltage(analogPin));
  delay(2);
 
}

#include <Arduino.h>
#include <stdlib.h>
#include "jibStepperMotor.h"
#include <AccelStepper.h>
#include "joystick.h"

const int PIN_ODCZYT = A0;

AccelStepper stepper_jib(AccelStepper::DRIVER, STEP, DIRECTION); // Setting jib stepper motor. The motor is controlled by Big Easy driver. pin 25 = step control, pin 23 = direction control
void setup() {
  setupJibStepperMotor(stepper_jib);
  Serial.begin(9600); // Serial communication is begun.
  Serial.setTimeout(10); // Some time is given for the serial communication to establish.
}


void loop() {
  //runJibMotor(stepper_jib);
  int jibGear = getGear(PIN_ODCZYT);
  Serial.println(jibGear);
  changeDirectionOfStepper(jibGear,stepper_jib);
  //tone(STEP, voltageValue);


}

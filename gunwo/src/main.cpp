#include <Arduino.h>
#include <stdlib.h>
#include <AccelStepper.h>

#include "Atributtes.h"
#include "Joystick.h"
#include "JibStepperMotor.h"


AccelStepper stepper_jib(AccelStepper::DRIVER, STEP_J, DIRECTION_J); // Setting jib stepper motor. The motor is controlled
                                                                    //by Big Easy driver. pin 25 = step control, pin 23 = direction control
void setup() {
  stepper_jib = setupJibStepperMotor(stepper_jib);
  Serial.begin(9600); // Serial communication is begun.
  Serial.setTimeout(10); // Some time is given for the serial communication to establish.
}

void loop() {
  int jibGear = getGear(ANALOG_READ_JIB);
  Serial.println(jibGear);

  stepper_jib = changeDirectionOfStepper(jibGear,stepper_jib);
  stepper_jib.run();

  //runJibMotor(stepper_jib);
}

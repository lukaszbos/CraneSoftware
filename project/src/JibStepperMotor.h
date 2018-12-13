#ifndef JIB_STEPPER_MOTOR_H
#define JIB_STEPPER_MOTOR_H

#include <Arduino.h>
#include <AccelStepper.h>
#include <stdlib.h>

#include "Atributtes.h"

// Define some steppers and the pins the steppers will use
void runJibMotor(AccelStepper stepper_jib); // Function which runs all motors according to control values set for them.
                                            //This function has to be called "frequent enough" in order to keep the motors operational
                                            //throughout executing code (for example it is recommended to call this function before and
                                            //after any serial communication related activity)
AccelStepper setupJibStepperMotor(AccelStepper stepper_j);
void setJibMotorSpeedCase(int gear, AccelStepper stepper_jib);
AccelStepper changeDirectionOfStepper(int gear_, AccelStepper stepper_j);


/*
#include <AccelStepper.h>

AccelStepper Xaxis(AccelStepper::DRIVER, 11, 12); // pin 3 = step, pin 6 = direction


void setup() {
  Xaxis.setMaxSpeed(400);  //  4 step per sec
  Xaxis.setAcceleration(2);  // 2 step per sec^2
  Xaxis.move(2000);  // move of 200 step

}

void loop() {

  Xaxis.run();

}
*/

#endif /* end of include guard: JIB_STEPPER_MOTOR_H */

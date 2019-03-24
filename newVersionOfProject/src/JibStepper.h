#ifndef JIB_STEPPER_H
#define JIB_STEPPER_H

#include <Arduino.h>
#include <AccelStepper.h>
#include <stdlib.h>

#include "Atributtes.h"

// Define some steppers and the pins the steppers will use
void runJibMotor(AccelStepper stepper_jib); // Function which runs all motors according to control values set for them.
                                            //This function has to be called "frequent enough" in order to keep the motors operational
                                            //throughout executing code (for example it is recommended to call this function before and
                                            //after any serial communication related activity)

AccelStepper setupJibStepper(AccelStepper stepper_jib, float speed);
AccelStepper setJibMotorSpeedCase(int gear, AccelStepper stepper_jib);
AccelStepper changeDirectionOfStepper(int gear, AccelStepper stepper_jib);



#endif /* end of include guard: JIB_STEPPER_H */

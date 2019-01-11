#include <Arduino.h>
#include <stdlib.h>
#include <AccelStepper.h>

#include "Atributtes.h"
#include "Joystick.h"
#include "JibStepper.h"


AccelStepper stepper_jib(AccelStepper::DRIVER, STEP_J, DIRECTION_J); // Setting jib stepper motor. The motor is controlled
                                                                     //by Big Easy driver. pin 25 = step control, pin 23 = direction control


void setup() {
  //stepper_jib = setupJibStepper(stepper_jib, START_SPEED);
  stepper_jib.setMaxSpeed(2000);
  setupJibStepper(stepper_jib, 1000);
  Serial.begin(9600); // Serial communication is begun.
  Serial.setTimeout(10); // Some time is given for the serial communication to establish.
  //stepper_jib.setMaxSpeed(400);  //  4 step per sec
  //stepper_jib.setAcceleration(400);  // 2 step per sec^2
  //stepper_jib.move(2000);  // move of 200 step
  pinMode(ENJ_J, OUTPUT); // Enable pin for the jib motor is defined as output pin i.e. it will output a signal
  pinMode(STEP_J, OUTPUT);
  pinMode(DIRECTION_J, OUTPUT);
  digitalWrite(ENJ_J, LOW); // Enable pin for the jib motor is set to HIGH (5V), meaning that the motor is off

}

Joystick jibJoystick = Joystick();
void loop() {
  int jibGear = jibJoystick.getGear(ANALOG_READ_JIB);
  Serial.println(jibGear);

   stepper_jib = changeDirectionOfStepper(jibGear,stepper_jib);



  // stepper_jib.run();
  // delay(5);


  // int gear = jibGear;
  // if (gear>0) {
  //   digitalWrite(ENJ_J, LOW);
  //
  //   stepper_jib.move(5);  // move of 10 steps
  //   stepper_jib.setSpeed(100); // Maximum speed [steps/s] of the jib motor is set. This is the speed that the motor tries to achieve. This value is altered for the motor control.
  //   stepper_jib.setAcceleration(100); // Acceleration [steps/s^2] of the jib motor is set.
  //   //stepper_jib.runSpeed();
  //
  // }
  // if (gear<0) {
  //   digitalWrite(ENJ_J, LOW);
  //
  //   stepper_jib.move(5);  // move of 10 steps
  //   stepper_jib.setSpeed(-400); // Maximum speed [steps/s] of the jib motor is set. This is the speed that the motor tries to achieve. This value is altered for the motor control.
  //   stepper_jib.setAcceleration(100); // Acceleration [steps/s^2] of the jib motor is set.
  //   //stepper_jib.runSpeed();
  //
  // }
  // if (gear==0){
  //   digitalWrite(ENJ_J, HIGH);
  //   //Serial.println("Gear=0");
  // }
  // //stepper_jib.run();
  // stepper_jib.runSpeed();


}

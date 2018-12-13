#include "JibStepperMotor.h"

int spd_j = 0; // Initial speed of the jib is set to zero
int dir_j = 0; // Initial direction of the jib is set to zero
const float max_step_spd_jib = 3; // [step/s]

// Define some steppers and the pins the steppers will use
void runJibMotor(AccelStepper stepper_jib) // Function which runs all motors according to control values set for them. This function has to be called "frequent enough" in order to keep the motors operational throughout executing code (for example it is recommended to call this function before and after any serial communication related activity)
{
  stepper_jib.run();
}

AccelStepper setupJibStepperMotor(AccelStepper stepper_j){
  stepper_j.setMaxSpeed(250); // Maximum speed [steps/s] of the jib motor is set. This is the speed that the motor tries to achieve. This value is altered for the motor control.
  stepper_j.setAcceleration(5); // Acceleration [steps/s^2] of the jib motor is set.
  //stepper_j.moveTo(20000);  // move of 10 steps

  pinMode(ENJ_J, OUTPUT); // Enable pin for the jib motor is defined as output pin i.e. it will output a signal
  pinMode(STEP_J, OUTPUT);
  digitalWrite(ENJ_J, LOW); // Enable pin for the jib motor is set to HIGH (5V), meaning that the motor is off

  return stepper_j;
}

void setJibMotorSpeedCase(int gear, AccelStepper stepper_jib){
  switch (gear) {
     case 1:
      //stepper_jib.setMaxSpeed(5);
  //     stepper_jib.setAcceleration(max_step_spd_jib/3);
      //stepper_jib.setSpeed(0.2);
      //stepper_jib.runSpeed();
      //stepper_jib.moveTo(-10);
      //stepper_jib.run();

      stepper_jib.moveTo(500);  // move of 10 steps

      //tone(STEP, max_step_spd_jib/3);
      break;
     case 2:
    //  stepper_jib.setMaxSpeed(max_step_spd_jib/2);
    //  stepper_jib.setAcceleration(max_step_spd_jib/3);
    //stepper_jib.setSpeed(100);
    //stepper_jib.runSpeed();
      //stepper_jib.moveTo(-10);
      //stepper_jib.run();
      tone(STEP_J, max_step_spd_jib/2);
      break;
     case 3:
      /*stepper_jib.setMaxSpeed(max_step_spd_jib);
      stepper_jib.setAcceleration(max_step_spd_jib/3);
      stepper_jib.moveTo(-10);
      stepper_jib.run(); */
      tone(STEP_J, max_step_spd_jib);
      break;
     case -1:
    //  stepper_jib.setSpeed(max_step_spd_jib/3);
      tone(STEP_J, max_step_spd_jib/3);
      break;
     case -2:
    //  stepper_jib.setSpeed(max_step_spd_jib/2);
      tone(STEP_J, max_step_spd_jib/2);
      break;
     case -3:
    //  stepper_jib.setSpeed(max_step_spd_jib);
      tone(STEP_J, max_step_spd_jib);
      break;
    case 0:
      digitalWrite(ENJ_J, HIGH);
      break;
    }

}

AccelStepper changeDirectionOfStepper(int gear_, AccelStepper stepper_j){
  if (gear_>0) {
    dir_j = 0;
    digitalWrite(ENJ_J, LOW);
    digitalWrite(DIRECTION_J, LOW);
    setJibMotorSpeedCase(gear_,stepper_j);
    //spd_j = left_hor_mid - 81 - left_hor;
    //spd_j = map(spd_j, 0, 252, 0, max_step_spd_jib-10); // Analog value of the joystick is converted to the stepping speed of the motor
    //spd_j = (jibVoltageValue/MAX) * max_step_spd_jib;
  }
  if (gear_<0) {
    dir_j = 1;
    digitalWrite(ENJ_J, LOW);
    digitalWrite(DIRECTION_J, HIGH);
    setJibMotorSpeedCase(gear_,stepper_j);
    //spd_j = left_hor_mid - 81 - left_hor;
    //spd_j = map(spd_j, 0, 252, 0, max_step_spd_jib-10); // Analog value of the joystick is converted to the stepping speed of the motor
    //spd_j = (jibVoltageValue/MAX) * max_step_spd_jib;
  }
  if (gear_==0){
    digitalWrite(ENJ_J, HIGH);
  }
return stepper_j;
}


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

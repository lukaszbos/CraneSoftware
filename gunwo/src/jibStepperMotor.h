#include <Arduino.h>
#include <AccelStepper.h>
#include <stdlib.h>

#define STEP 11 // USTAW TO
#define DIRECTION 12 // USTAW TO
#define ENJ 6 // giving high to EN shuts down the driver
// SLP - hight sleeps the driver, RST - state HIGH resets driver
//MS1, MS2 ,MS3 configouring resolution of driver
//#define ENK1 2
//#define ENK2 3
#define MAX 800

int spd_j = 0; // Initial speed of the jib is set to zero
int dir_j = 0; // Initial direction of the jib is set to zero
const float max_step_spd_jib = 500; // [step/s]

// Define some steppers and the pins the steppers will use
void runJibMotor(AccelStepper stepper_jib) // Function which runs all motors according to control values set for them. This function has to be called "frequent enough" in order to keep the motors operational throughout executing code (for example it is recommended to call this function before and after any serial communication related activity)
{
  stepper_jib.run();
}

void setupJibStepperMotor(AccelStepper stepper_jib){
  pinMode(ENJ, OUTPUT); // Enable pin for the jib motor is defined as output pin i.e. it will output a signal
  digitalWrite(ENJ, HIGH); // Enable pin for the jib motor is set to HIGH (5V), meaning that the motor is off

  //stepper_jib.setMaxSpeed(250.0); // Maximum speed [steps/s] of the jib motor is set. This is the speed that the motor tries to achieve. This value is altered for the motor control.
  //stepper_jib.setAcceleration(60.0); // Acceleration [steps/s^2] of the jib motor is set.
  stepper_jib.setSpeed(60);
  pinMode(STEP, OUTPUT);
}

void setJibMotorSpeedCase(int gear, AccelStepper stepper_jib){
  switch (gear) {
     case 1:
      stepper_jib.setSpeed(max_step_spd_jib/3);
      tone(STEP, max_step_spd_jib/3);
      break;
     case 2:
      stepper_jib.setSpeed(max_step_spd_jib/2);
      tone(STEP, max_step_spd_jib/2);
      //tone(STEP, 50);
      break;
     case 3:
      stepper_jib.setSpeed(max_step_spd_jib);
      tone(STEP, max_step_spd_jib);
      break;
     case -1:
      stepper_jib.setSpeed(max_step_spd_jib/3);
      tone(STEP, max_step_spd_jib/3);
      break;
     case -2:
      stepper_jib.setSpeed(max_step_spd_jib/2);
      tone(STEP, max_step_spd_jib/2);
      break;
     case -3:
      stepper_jib.setSpeed(max_step_spd_jib);
      tone(STEP, max_step_spd_jib);
      break;
     case 0:
      tone(STEP, 0);
      break;
    }

}

void changeDirectionOfStepper(int gear, AccelStepper stepper_jib){
  if (gear>=0) {
    dir_j = 0;
    digitalWrite(DIRECTION, LOW);
    setJibMotorSpeedCase(gear,stepper_jib);
    //spd_j = left_hor_mid - 81 - left_hor;
    //spd_j = map(spd_j, 0, 252, 0, max_step_spd_jib-10); // Analog value of the joystick is converted to the stepping speed of the motor
    //spd_j = (jibVoltageValue/MAX) * max_step_spd_jib;
  }

  if (gear<0) {
    dir_j = 1;
    digitalWrite(DIRECTION, HIGH);
    setJibMotorSpeedCase(gear,stepper_jib);
    //spd_j = left_hor_mid - 81 - left_hor;
    //spd_j = map(spd_j, 0, 252, 0, max_step_spd_jib-10); // Analog value of the joystick is converted to the stepping speed of the motor
    //spd_j = (jibVoltageValue/MAX) * max_step_spd_jib;
  }

}

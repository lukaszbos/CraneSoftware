#include "JibStepper.h"

int spd_j = 0; // Initial speed of the jib is set to zero
int dir_j = 0; // Initial direction of the jib is set to zero
const float max_step_spd_jib = 2000; // [step/s]

// Define some steppers and the pins the steppers will use
void runJibMotor(AccelStepper stepper_jib) // Function which runs all motors according to control values set for them. This function has to be called "frequent enough" in order to keep the motors operational throughout executing code (for example it is recommended to call this function before and after any serial communication related activity)
{
  stepper_jib.run();
}

AccelStepper setupJibStepper(AccelStepper stepper_jib, float speed){
  //digitalWrite(ENJ_J, LOW);
  stepper_jib.move(10);  // move of 10 steps
  stepper_jib.setSpeed(speed); // Maximum speed [steps/s] of the jib motor is set. This is the speed that the motor tries to achieve. This value is altered for the motor control.
  stepper_jib.setAcceleration(speed); // Acceleration [steps/s^2] of the jib motor is set.
  stepper_jib.runSpeed();
  Serial.println("ustawiam speed");
  Serial.println(speed);
  return stepper_jib;

}
/*

AccelStepper setJibMotorSpeedCase(int gear, AccelStepper stepper_jib){
  switch (gear) {
     case 1:
      //setupJibStepper(stepper_jib, max_step_spd_jib/3);
      // stepper_jib.move(5);  // move of 10 steps
      // stepper_jib.setSpeed(200); // Maximum speed [steps/s] of the jib motor is set. This is the speed that the motor tries to achieve. This value is altered for the motor control.
      // stepper_jib.setAcceleration(200); // Acceleration [steps/s^2] of the jib motor is set.
      //
      // Serial.println("ustawiam speed");
    //  Serial.println(speed);
      break;
     case 2:
      stepper_jib=setupJibStepper(stepper_jib, max_step_spd_jib/2);
      stepper_jib.runSpeed();
      //tone(STEP_J, max_step_spd_jib/2);
      break;
     case 3:
      //Serial.println("wchodze do kejsa z wart 3");
      /*stepper_jib.setMaxSpeed(max_step_spd_jib);
      stepper_jib.setAcceleration(max_step_spd_jib/3);
      stepper_jib.moveTo(-10);
      stepper_jib.run();
      stepper_jib=setupJibStepper(stepper_jib, max_step_spd_jib);
      //tone(STEP_J, max_step_spd_jib);
      break;
     case -1:
    //  stepper_jib.setSpeed(max_step_spd_jib/3);
      //Serial.println("wchodze do kejsa z wart -1");
      stepper_jib=setupJibStepper(stepper_jib, -max_step_spd_jib/3);
      //tone(STEP_J, max_step_spd_jib/3);
      break;
     case -2:
    //  stepper_jib.setSpeed(max_step_spd_jib/2);
      stepper_jib=setupJibStepper(stepper_jib, -max_step_spd_jib/2);
      stepper_jib.runSpeed();
    //  tone(STEP_J, max_step_spd_jib/2);
      break;
     case -3:
    //  stepper_jib.setSpeed(max_step_spd_jib);
      stepper_jib=setupJibStepper(stepper_jib, -max_step_spd_jib);
    //  tone(STEP_J, max_step_spd_jib);
      break;
    case 0:
      digitalWrite(ENJ_J, HIGH);
      break;
    }
    return stepper_jib;
}

*/
AccelStepper changeDirectionOfStepper(int gear, AccelStepper stepper_jib){
    if(gear==1){
        digitalWrite(ENJ_J, LOW);
        stepper_jib=setupJibStepper(stepper_jib, max_step_spd_jib/4);
        stepper_jib.runSpeed();
    }
    if(gear==2){
        digitalWrite(ENJ_J, LOW);
        stepper_jib=setupJibStepper(stepper_jib, max_step_spd_jib/2);
        stepper_jib.runSpeed();
    }
    if(gear==3){
        digitalWrite(ENJ_J, LOW);
        stepper_jib=setupJibStepper(stepper_jib, max_step_spd_jib);
        stepper_jib.runSpeed();
     }
    if(gear==-1){
      digitalWrite(ENJ_J, LOW);
      stepper_jib=setupJibStepper(stepper_jib, -max_step_spd_jib/4);
      stepper_jib.runSpeed();
     }
    if(gear==-2){
        digitalWrite(ENJ_J, LOW);
        stepper_jib=setupJibStepper(stepper_jib, -max_step_spd_jib/2);
        stepper_jib.runSpeed();
     }
    if(gear==-3){
        digitalWrite(ENJ_J, LOW);
        stepper_jib=setupJibStepper(stepper_jib, -max_step_spd_jib);
        stepper_jib.runSpeed();
     }
    if(gear==0){
     digitalWrite(ENJ_J, HIGH);
    }
    return stepper_jib;
  }


/*
AccelStepper changeDirectionOfStepper(int gear, AccelStepper stepper_jib){

  if (gear>0) {
    digitalWrite(ENJ_J, LOW);
  //  digitalWrite(DIRECTION_J, LOW);
  // stepper_jib.move(5);  // move of 10 steps
  // stepper_jib.setSpeed(200); // Maximum speed [steps/s] of the jib motor is set. This is the speed that the motor tries to achieve. This value is altered for the motor control.
  // stepper_jib.setAcceleration(200); // Acceleration [steps/s^2] of the jib motor is set.
  //
  // Serial.println("ustawiam speed");
  stepper_jib = setupJibStepper(stepper_jib, 200);
    //setJibMotorSpeedCase(gear,stepper_jib);
    //Serial.println("Gear>0");
  }
  if (gear<0) {
    digitalWrite(ENJ_J, LOW);
    //digitalWrite(DIRECTION_J, HIGH);
    stepper_jib = setupJibStepper(stepper_jib, -200);
    //stepper_jib = setJibMotorSpeedCase(gear,stepper_jib);
    //Serial.println("Gear<0");
  }
  if (gear==0){
    digitalWrite(ENJ_J, HIGH);
    //Serial.println("Gear=0");
  }
return stepper_jib;
}
*/

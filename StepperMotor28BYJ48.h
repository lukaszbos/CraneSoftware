/*
Stepper Motor with 28BYJ-48 Gear 5V/ 0.1A/ 0,03Nm with ULN2003 driver

Very first tests..
 */
 
#include <Stepper.h>
#include <AccelStepper.h>

const int stepsPerRevolution = 512;  // change this to fit the number of steps per revolution
                                     // for your motor
const int maxSpeed28BYJ = 60;

// initialize the stepper library on pins 8 through 11:
Stepper myStepper(stepsPerRevolution, 8, 10, 9, 11); // 1 becouse we want to make one step at one looping... specification says  1-3-2-4 is correct order

void setupStepper28BYJ48() {
  // set the speed at 60 rpm:
 myStepper.setSpeed(60);
  
}

void setSpeedCase(int gear){
    switch (gear) {
       case 1:
        myStepper.setSpeed(maxSpeed28BYJ/3);
        break;
       case 2:
        myStepper.setSpeed(maxSpeed28BYJ/2);
        break;
       case 3:
        myStepper.setSpeed(maxSpeed28BYJ);
        break;
       case -1:
        myStepper.setSpeed(maxSpeed28BYJ/3);
        break;
       case -2:
        myStepper.setSpeed(maxSpeed28BYJ/2);
        break;
       case -3:
        myStepper.setSpeed(maxSpeed28BYJ);
        break;
  }
  }

void changeDirectionOfStepper28BYJ48(int gear){
  // step one revolution  in one direction:
  if(gear>0){
  Serial.println("clockwise");
  setSpeedCase(gear);
  myStepper.step(10);
      
  }
  // step one revolution in the other direction:
  if(gear<0){
  Serial.println("counterclockwise");
  setSpeedCase(gear);
  myStepper.step(-10);
   
  }
}


  

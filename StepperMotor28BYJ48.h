/*
Stepper Motor with 28BYJ-48 Gear 5V/ 0.1A/ 0,03Nm with ULN2003 driver

Very first tests..
 */
 
#include <Stepper.h>

const int stepsPerRevolution = 512;  // change this to fit the number of steps per revolution
// for your motor

// initialize the stepper library on pins 8 through 11:
Stepper myStepper(stepsPerRevolution, 8, 10, 9, 11); // specification says  1-3-2-4 is correct order

void setupStepper28BYJ48() {
  // set the speed at 60 rpm:
  myStepper.setSpeed(60);
  // initialize the serial port:
  Serial.begin(9600);
}

void changeDirectionOfStepper28BYJ48(){
  // step one revolution  in one direction:
  Serial.println("clockwise");
  myStepper.step(stepsPerRevolution);
  delay(500);

  // step one revolution in the other direction:
  Serial.println("counterclockwise");
  myStepper.step(-stepsPerRevolution);
  delay(500);

}

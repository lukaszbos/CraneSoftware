#include <Arduino.h>
#include "attributes.h"

// This code uses two libraries. These both can be easily installed through Arduino IDE library manager by pressing CTRL + SHIFT + I
#include <TMC2130Stepper.h> // https://github.com/teemuatlut/TMC2130Stepper
TMC2130Stepper driver = TMC2130Stepper(EN_PIN, DIR_PIN, STEP_PIN, CS_PIN);

#include <AccelStepper.h> // https://www.airspayce.com/mikem/arduino/AccelStepper/
AccelStepper stepper = AccelStepper(stepper.DRIVER, STEP_PIN, DIR_PIN);

int realSpeed;
int maxSpd = 1000;

int changeVelocity(int gear) {
 if(gear==1){
   driver.shaft_dir(0);
   realSpeed=maxSpd/3;
   stepper.setSpeed(realSpeed);
  }
   if(gear==2){
   driver.shaft_dir(0);
   realSpeed=maxSpd/2;
   stepper.setSpeed(realSpeed);
   }
   if(gear==3){
   driver.shaft_dir(0);
   realSpeed=maxSpd;
   stepper.setSpeed(realSpeed);
    }
   if(gear==-1){
     driver.shaft_dir(1);
     realSpeed=maxSpd/3;
     stepper.setSpeed(realSpeed);
    }
   if(gear==-2){
      driver.shaft_dir(1);
      realSpeed=maxSpd/2;
      stepper.setSpeed(realSpeed);
    }
   if(gear==-3){
      driver.shaft_dir(1);
      realSpeed=maxSpd;
      stepper.setSpeed(realSpeed);
    }
   if(gear==0){
     driver.shaft_dir(1);
     realSpeed=0;
     stepper.setSpeed(realSpeed);
   }
   return realSpeed;;
}

int getJibGear(int gear, int pot){
  //stepper.setSpeed(map(analogRead(JOYSTICK_PIN),0,1023,-800,800));
   pot = analogRead(JIB_JOYSTICK_PIN);
  //changes the output of the joystick (voltages from 0 to 1023) to gears from -3 (counter clockwise) to 3 (clockwise)
   gear = map(pot,0,1023,-3,4);
  return gear;

}

void settings(){ // this function changes some settings of TMC2130
 driver.begin(); // Initiate pins and registeries
 driver.setCurrent(400, 0.11, 0.2);    // Set stepper current to 600mA. The command is the same as command TMC2130.setCurrent(600, 0.11, 0.5);
 driver.hold_delay(15);
 driver.power_down_delay(64);
 driver.stealthChop(1);      // Enable extremely quiet stepping
 driver.stealth_autoscale(1);
 driver.microsteps(0);
 driver.interpolate(1);
}

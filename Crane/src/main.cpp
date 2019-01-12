#include <Arduino.h>
#include "motor_movements.h"
#include "attributes.h"

/* You also need to connect the SPI pins as follows for programming the TMC2130. If you have several TMC2130, they all must use these same pins.
SDI --> D11
SDO --> D12
SCK --> D13
So our crane needs 9 pins in total to control three TMC2130.
And on top of that you need to also connect motor coils
M1A and M1B to one coil and
M2A and M2B to another coil
Finally connect the power wires
GND --> GND
VIO --> 5V
VM --> motor power supply (5 - 45 V) and > 100 µF capacitor */

void setup() {
 SPI.begin();
 Serial.begin(250000); // Set baud rate in serial monitor
 //while(!Serial); //only needed for ATmega32U4
 Serial.println("Start...");
 pinMode(CS_PIN, OUTPUT);
 digitalWrite(CS_PIN, HIGH);
 settings();

 stepper.setAcceleration(500);
 stepper.setMaxSpeed(2000);
 stepper.setSpeed(500);
}




void loop() {
 stepper.runSpeed();
 //control something by typing into serial monitor. Just for testing.
 if(Serial.available()){
   char a = Serial.read();
   static word spd=stepper.speed(); // save the last speed of the motor
   if(a=='0') stepper.setSpeed(0); // stop motor
   else{
     if(a=='1') driver.shaft_dir(0);
     else if(a=='2') driver.shaft_dir(1); // reverses motor direction
     else if(a=='+' && spd<0x800) spd<<=2; // double the speed
     else if(a=='-' && spd>4) spd>>=2; // half speed
     stepper.setSpeed(spd); // run motor at that speed
   }
   Serial.println(spd);
 }
 stepper.runSpeed();
 // read joystick to control speed
int gear;
int pot;

  gear = getJibGear(gear, pot);
 changeVelocity(gear);

 stepper.runSpeed();
 // print Hall sensor readings to serial
 static unsigned long banana=0;
 if(millis()-banana>500){ // some library affects millis(), so its clock runs at wrong rate
   banana=millis();
   Serial.print(analogRead(HALL_PIN)); // print hall sensor readings
   if(driver.GSTAT()==1){ // if driver has detected error, it has automatically stopped
     settings(); // reset the driver settings, so it can start spinning again
     driver.shaft_dir(!driver.shaft_dir()); // and change motor direction
   }
   Serial.print(" ");
   Serial.print(pot);
   Serial.print(" ");
   Serial.print(realSpeed);
   Serial.print(" ");
   Serial.println(gear);
 }
}

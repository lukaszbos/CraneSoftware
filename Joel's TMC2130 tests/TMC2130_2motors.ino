// Arduino Nano pin connections 
#define HALL_PIN  A7 // Hall-effect sensor pin
#define slewJoyPin A0
#define trolleyJoyPin A1

// TMC2130 pin connections
/* You need to connect the SPI pins as follows for programming the TMC2130. If you have several TMC2130, they all must use these same pins.
SDI --> D11
SDO --> D12
SCK --> D13

En --> GND // enable (CFG6). I want driver always enabled, so connect EN --> GND
Dir --> GND // direction can also be controlled through SPI, so to save pins, connect DIR --> GND

And on top of that you need to also connect motor coils
M1A and M1B to one coil and
M2A and M2B to another coil

Finally connect the power wires
GND --> GND
VIO --> 5V
VM --> motor power supply (5 - 45 V) and > 100 µF capacitor */

// This code uses two libraries. These both can be easily installed through Arduino IDE library manager by pressing CTRL + SHIFT + I
#include <TMC2130Stepper.h> // https://github.com/teemuatlut/TMC2130Stepper
// choose chip select pins for each stepper driver
TMC2130Stepper slewer = TMC2130Stepper(7);
TMC2130Stepper troller = TMC2130Stepper(5);

#include <AccelStepper.h> // https://www.airspayce.com/mikem/arduino/AccelStepper/
// choose step pins for each
AccelStepper slew = AccelStepper(slew.DRIVER, 6);
AccelStepper trolley = AccelStepper(trolley.DRIVER, 4);

void settings(){ // this function changes some settings of TMC2130
	// slewing driver settings
	slewer.begin(); // Initiate pins and registeries
	slewer.setCurrent(400, 0.11, 0.2); // coil current (mA), current sense resistor (0.11 ohm on silentStepSticks), hold current relative to run current (0.0-1.0)
	slewer.power_down_delay(64); // how long to wait after movement stops before reducing to hold current 0-255 = 0-4 seconds
	slewer.hold_delay(15); // 0-15 how gradually it reduces to hold current. 0=fast change. 15=slow change.
	slewer.stealthChop(1);      // Enable extremely quiet stepping
	slewer.stealth_autoscale(1);
	//slewer.stealth_max_speed(10); // switch stealthChop off if motor spins fast enough (meaning if time between two steps is less than this)
	slewer.microsteps(0); // we dont want any
	slewer.interpolate(1); // automatic 256 x microstepping
	slewer.chopper_mode(0); // 0=spreadCycle 1=constant off time

	// trolleying driver settings
	troller.begin();
	troller.setCurrent(400, 0.11, 0.2);
	troller.power_down_delay(64);
	troller.hold_delay(15);
	troller.stealthChop(1);
	troller.stealth_autoscale(1);
	//troller.stealth_max_speed(10);
	troller.microsteps(0);
	troller.interpolate(1);
	troller.chopper_mode(0);
}

void setup() {
	//SPI.begin();
	Serial.begin(250000); // Set baud rate in serial monitor
	//while(!Serial); //only needed for ATmega32U4
	Serial.println("Start...");
	/*pinMode(CS_PIN, OUTPUT);
	digitalWrite(CS_PIN, HIGH);*/
	settings();

	slew.setAcceleration(500);
	slew.setMaxSpeed(1500);
	trolley.setAcceleration(500);
	trolley.setMaxSpeed(1500);
	//slew.setSpeed(600);
}

void loop() {
	if(Serial.available()){ //control something by typing into serial monitor. Just for testing.
		char a=Serial.read();
		static word spd=slew.speed(); // save the last speed of the motor
		if(a=='0') slew.setSpeed(0); // stop motor
		else{
			if(a=='1') slewer.shaft_dir(0);
			else if(a=='2') slewer.shaft_dir(1); // reverses motor direction
			else if(a=='+' && spd<0x800) spd<<=2; // double the speed
			else if(a=='-' && spd>4) spd>>=2; // half speed
			slew.setSpeed(spd); // run motor at that speed
		}
		Serial.println(spd);
	}
	// read joystick to control slewing speed
	int slewPot = analogRead(slewJoyPin);
	int slewSpd;
	if (slewPot<412){
		slewer.shaft_dir(0);
		slewSpd=map(slewPot,412,0,3,2000);
		slew.setSpeed(slewSpd);
	}
	else if (slewPot>612){
		slewer.shaft_dir(1);
		slewSpd=map(slewPot,612,1023,3,2000);
		slew.setSpeed(slewSpd);
	}
	else{
		slewSpd=0;
		slew.setSpeed(slewSpd);
	}
	slew.run();
	
	// read joystick to control trolleying speed
	int trolleyPot = analogRead(trolleyJoyPin);
	int trolleySpd;
	if (trolleyPot<412){
		troller.shaft_dir(0);
		trolleySpd=map(trolleyPot,412,0,3,2000);
		trolley.setSpeed(trolleySpd);
	}
	else if (trolleyPot>612){
		troller.shaft_dir(1);
		trolleySpd=map(trolleyPot,612,1023,3,2000);
		trolley.setSpeed(trolleySpd);
	}
	else{
		trolleySpd=0;
		trolley.setSpeed(trolleySpd);
	}
	trolley.run();
	/*delay(2000);
	slewer.shaft_dir(0);
	slew.runToNewPosition(800);
	delay(2000);
	slewer.shaft_dir(1);
	slew.runToNewPosition(0);*/
	// print Hall sensor readings to serial
	static unsigned long banana=0;
	if(millis()-banana>50){ // some library affects millis(), so its clock runs at wrong rate
		banana=millis();
		Serial.print(analogRead(HALL_PIN)); // print hall sensor readings
		/*Serial.print(" ");
		Serial.print(slewPot);
		Serial.print(" ");
		Serial.println(slewSpd);*/
		if(slewer.GSTAT()==1){ // if driver has detected error, it has automatically stopped
			settings(); // reset the driver settings, so it can start spinning again
			//slewer.shaft_dir(!slewer.shaft_dir()); // and change motor direction
		}
	}
}

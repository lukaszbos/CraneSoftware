// Arduino Nano pin connections. These you can rewire freely. Each TMC2130 needs its own pins.
// To reduce the number of pins needed, i have wired EN and DIR to GND.
#define EN_PIN    0xFFFF  //enable (CFG6). I want driver always enabled, so connect EN --> GND 
#define DIR_PIN   0xFFFF //direction can also be controlled through SPI, so connect DIR --> GND
#define STEP_PIN  3 	//step
#define CS_PIN    2 	//chip select

#define HALL_PIN  A7 //Hall-effect sensor pin
#define JOYSTICK_PIN A0

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

// This code uses two libraries. These both can be easily installed through Arduino IDE library manager by pressing CTRL + SHIFT + I
#include <TMC2130Stepper.h> // https://github.com/teemuatlut/TMC2130Stepper
TMC2130Stepper driver = TMC2130Stepper(EN_PIN, DIR_PIN, STEP_PIN, CS_PIN);

#include <AccelStepper.h> // https://www.airspayce.com/mikem/arduino/AccelStepper/
AccelStepper stepper = AccelStepper(stepper.DRIVER, STEP_PIN, DIR_PIN);

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
	if(Serial.available()){ //control something by typing into serial monitor. Just for testing.
		char a=Serial.read();
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
	//stepper.setSpeed(map(analogRead(JOYSTICK_PIN),0,1023,-800,800));
	int pot = analogRead(JOYSTICK_PIN);
	int realSpeed;
	if (pot<400){
		driver.shaft_dir(0);
		realSpeed=map(pot,400,0,3,1500);
		stepper.setSpeed(realSpeed);
	}
	else if (pot>600){
		driver.shaft_dir(1);
		realSpeed=map(pot,600,1023,3,1500);
		stepper.setSpeed(realSpeed);
	}
	else{
		realSpeed=0;
		stepper.setSpeed(realSpeed);
	}
	stepper.runSpeed();
	// print Hall sensor readings to serial
	static unsigned long banana=0;
	if(millis()-banana>50){ // some library affects millis(), so its clock runs at wrong rate
		banana=millis();
		Serial.print(analogRead(HALL_PIN)); // print hall sensor readings
		if(driver.GSTAT()==1){ // if driver has detected error, it has automatically stopped
			settings(); // reset the driver settings, so it can start spinning again
			driver.shaft_dir(!driver.shaft_dir()); // and change motor direction
		}
		Serial.print(" ");
		Serial.print(pot);
		Serial.print(" ");
		Serial.println(realSpeed);
	}
}

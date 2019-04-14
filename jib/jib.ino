// This code is supposed to read commands from serial and control 3 steppers.
// This works at least with atmega 328p microcontroller (Arduino Uno or Nano)
/* todo:
 * change acceleration limit to constant acceleration?
 * slow speed precise mode that uses stealthChop only
 * high speed mode that uses spreadCycle
 * adjust also setCurrent, power_down_delay, microsteps etc.
 * add step counting
 * make stallGuard work as a limit switch
 * use stallGuard value to limit speed to prevent motors stalling
 * slew homing with hall sensor
 * slack detector to stop hook motor before rope gets loose
 * combine with ethernet code
 * make trolley slow down before edges
 * add neoPixel leds for cool light effects
 * enable coolStep for power savings and less heating
 * overflow alarm for timer1 to test if code works
*/

// a motor can never spin too fast, right?
#pragma GCC optimize ("-O2") // https://www.instructables.com/id/Arduino-IDE-16x-compiler-optimisations-faster-code/

// Arduino Nano pin connections 
//#define HALL_PIN  A7 // Hall-effect sensor pin

// TMC2130 pin connections
	/* You need to connect the SPI pins as follows for programming the TMC2130. If you have several TMC2130, they all must use these same pins.
		SDI --> D11
		SDO --> D12
		SCK --> D13
	En --> GND // enable (CFG6). I want driver always enabled, so connect EN --> GND
	Dir --> GND // direction can also be controlled through SPI, so to save pins, connect DIR --> GND
	Step (slew) --> D4 
	Step (trolley) --> D5
	Step (hook) --> D6
	And on top of that you need to also connect motor coils
		M1A and M1B to one coil and
		M2A and M2B to another coil
	Finally connect the power wires
		GND --> GND
		VIO --> 5V
		VM --> motor power supply (5 - 45 V) and > 100 µF capacitor */

// This code uses libraries. These can be easily installed through Arduino IDE library manager by pressing CTRL + SHIFT + I
#include <TMC2130Stepper.h> // https://github.com/teemuatlut/TMC2130Stepper
// choose chip select pins for each stepper driver
TMC2130Stepper slew = TMC2130Stepper(A0);
TMC2130Stepper trolley = TMC2130Stepper(A1);
TMC2130Stepper hook = TMC2130Stepper(A2);

void settings(){ // this function changes some settings of TMC2130
	// slewing driver settings
	slew.begin(); // Initiate pins and registeries
	slew.setCurrent(400, 0.11, 0.2); // coil current (mA), current sense resistor (0.11 ohm on silentStepSticks), hold current relative to run current (0.0-1.0)
	slew.power_down_delay(64); // how long to wait after movement stops before reducing to hold current 0-255 = 0-4 seconds
	slew.hold_delay(15); // 0-15 how gradually it reduces to hold current. 0=fast change. 15=slow change.
	slew.stealthChop(1);      // Enable extremely quiet stepping
	slew.stealth_autoscale(1);
	slew.stealth_max_speed(10000); // switch stealthChop off if motor spins fast enough (meaning if time between two steps is less than this)
	slew.microsteps(0); // we dont want any
	slew.interpolate(1); // automatic 256 x microstepping
	slew.double_edge_step(1); // step on both rising and falling edges
	slew.chopper_mode(0); // 0=spreadCycle 1=constant off time

	// trolleying driver settings
	trolley.begin();
	trolley.setCurrent(400, 0.11, 0.2);
	trolley.power_down_delay(64);
	trolley.hold_delay(15);
	trolley.stealthChop(1);
	trolley.stealth_autoscale(1);
	trolley.stealth_max_speed(10000);
	trolley.microsteps(0);
	trolley.interpolate(1);
	trolley.double_edge_step(1);
	trolley.chopper_mode(0);

	// hoisting driver settings
	hook.begin();
	hook.setCurrent(700, 0.11, 0.2);
	hook.power_down_delay(64);
	hook.hold_delay(15);
	hook.stealthChop(1);
	hook.stealth_autoscale(1);
	hook.stealth_max_speed(10000); // big motor isn't as quick
	hook.microsteps(0);
	hook.interpolate(1);
	hook.double_edge_step(1);
	hook.chopper_mode(0);
}

volatile unsigned long
	kid[3]={0xFFFF00,0xFFFF00,0xFFFF00}, // CPU cycles to wait between steps for each motor
	boy[3]={0xFFFF00,0xFFFF00,0xFFFF00}; // CPU cycles left until the motor needs to be stepped again
volatile bool motOn[3]={0,0,0}; // which motors are spinning
volatile long pos[3]={0,0,0}; // motor step positions
volatile bool dir[3]={0,0,0}; // slew, trolley, hook direction

// Interrupt Service Routine that automatically keeps stepping motors
ISR(TIMER1_CAPT_vect){ // http://www.gammon.com.au/interrupts
	static bool man[3]={0}; // which motors to step next
	
	// toggles step pin(s)
	if(motOn[0] && man[0]){ //slew
		if(dir[0]) ++pos[0];
		else --pos[0];
		PORTD ^= 1<<4; // https://www.arduino.cc/en/Reference/PortManipulation
	}
	if(motOn[1] && man[1]){ //trolley
		if(dir[1]) ++pos[1];
		else --pos[1];
		PORTD ^= 1<<5;
	}
	if(motOn[2] && man[2]){ //hook
		if(dir[2]) ++pos[2];
		else --pos[2];
		PORTD ^= 1<<6;
	}

	// if new speed is higher than before
 	if(kid[0]<boy[0]) boy[0]=kid[0];
 	if(kid[1]<boy[1]) boy[1]=kid[1];
 	if(kid[2]<boy[2]) boy[2]=kid[2];

	// find who is the smallest boy
	unsigned long small=160000; // set maximum ISR refresh period
	if(boy[0]<=boy[1] && boy[0]<=boy[2] && boy[0]<=small){
		man[0]=1;
		small=boy[0];
	}else man[0]=0;
	if(boy[1]<=boy[0] && boy[1]<=boy[2] && boy[1]<=small){
		man[1]=1;
		small=boy[1];
	}else man[1]=0;
	if(boy[2]<=boy[0] && boy[2]<=boy[1] && boy[2]<=small){
		man[2]=1;
		small=boy[2];
	}else man[2]=0;

	// update boys
	boy[0]-=small;
	boy[1]-=small;
	boy[2]-=small;
	if(boy[0]==0) boy[0]=kid[0];
	if(boy[1]==0) boy[1]=kid[1];
	if(boy[2]==0) boy[2]=kid[2];
	
	fox(small); // set timer to wait for next motor step
}

// changes motor speed
// parameters: motor (0 or 1 or 2), cpu cycles between 2 steps (less is faster, but 0 stops motor)
void setSpeed(byte motor, unsigned long newKid){
	if (newKid==0){
		cli();
		motOn[motor]=0; // dont step the motor
		kid[motor]=0xFFFF00; // longest possible step period
		sei();
	}
	else{
		if(newKid>0xFFFF00) newKid=0xFFFF00; // why would we even try to step slower than this
		cli();
		motOn[motor]=1;
		kid[motor]=newKid;
		sei();
	}
}

// function to set timer1 period. Stolen from https://www.pjrc.com/teensy/td_libs_TimerOne.html
inline void fox(unsigned long cycles){
	if(cycles<500) cycles=500; // minimum cycles, cuz ISR takes some time too
	byte clockSelectBits;
	word period;
	if (cycles < 0x10000UL) {
		clockSelectBits = _BV(CS10);
		period = cycles;
	} else
	if (cycles < 0x10000UL * 8) {
		clockSelectBits = _BV(CS11);
		period = cycles / 8;
	} else
	if (cycles < 0x10000UL * 64) {
		clockSelectBits = _BV(CS11) | _BV(CS10);
		period = cycles / 64;
	} else
	if (cycles < 0x10000UL * 256) {
		clockSelectBits = _BV(CS12);
		period = cycles / 256;
	} else {
		clockSelectBits = _BV(CS12);
		period = 0xFFFFUL;
	}
	ICR1 = period;
	TCCR1B = _BV(WGM13) | _BV(WGM12) | clockSelectBits; // mode 12. p136
	//TCNT1 = 0; // reset counter. p115
}

void setup() {
	DDRD |= 0b01110000; // step pins outputs
	Serial.begin(250000); // Set baud rate in serial monitor
	settings();
	// let's enable timer1 to time the step pulses. See p113 here https://www.sparkfun.com/datasheets/Components/SMD/ATMega328.pdf
	TCCR1A=B00000000; //p134
	TIMSK1=B00100000; //p139
	fox(1000);
	//Serial.println();
	pinMode(A3,INPUT_PULLUP); // slack detector
}

void loop() {
	static char s0=0, s1=0, s2=0, goal0=0, goal1=0, goal2=0;
	static unsigned long fast[3]={400000,2000000,2000000}; // motor max speeds
	static unsigned long acl=10; // acceleration setting
	static unsigned long then=0;
	const unsigned long now=millis();
	
	if(now-then>acl){ //accelerate slowly
		then=now;
		
		if(s0<goal0) s0++; // slew
		else if(s0>goal0) s0--;
		bool newDir=s0>0?0:1;
		if (newDir!=dir[0]){
			slew.shaft_dir(newDir);
			dir[0]=newDir;
		}
		setSpeed(0,s0==0?0:fast[0]/abs(s0));

		if(s1<goal1) s1++; // trolley
		else if(s1>goal1) s1--;
		newDir=s1<0?0:1;
		if (newDir!=dir[1]){
			trolley.shaft_dir(newDir);
			dir[1]=newDir;
		}
		setSpeed(1,s1==0?0:fast[1]/abs(s1));

		if(s2<goal2) s2++; // hook
		else if(s2>goal2) s2--;
		newDir=s2>0?0:1;
		if (newDir!=dir[2]){
			hook.shaft_dir(newDir);
			dir[2]=newDir;
		}
		if(newDir==0 && digitalRead(A3)==1){ // slack detection
			s2=0;
			goal2=0;
			setSpeed(2,0);
		}
		else setSpeed(2,s2==0?0:fast[2]/abs(s2));
	}
	
	if(Serial.available()){ // receive speed commands from Python code
		static byte job=255;
		char wax=Serial.read();
		if(wax==127) job=0; // speed packet start character is 127
		else if(wax==-127) job=4; // -127 indicates that next byte will be settings
		else if(job<3){ // or else it must be a speed command -126 to 126
			if(job==0){
				goal0=wax;
			}
			if(job==1){
				goal1=wax;
			}
			if(job==2){
				goal2=wax;
			}
			++job;
		}
		else if(job==4){ // translate settings byte
			if(wax & 1){ // silent mode
				slew.stealth_max_speed(10);
				trolley.stealth_max_speed(10);
				hook.stealth_max_speed(10);
				fast[0]=2000000;
				fast[1]=8000000;
				fast[2]=15000000;
				acl=2;
			}else{ // high speed mode
				slew.stealth_max_speed(10000);
				trolley.stealth_max_speed(10000);
				hook.stealth_max_speed(10000);
				fast[0]=400000;
				fast[1]=2000000;
				fast[2]=2000000;
				acl=10;
			}
			++job;
		}
	}
	
	// prints various numbers to serial
	static unsigned long owl=0;
	if(now-owl>200){
		owl=now;
		//Serial.print(analogRead(HALL_PIN)); // print hall sensor readings
		long positron[3];
		for(byte i=0; i<3; i++){ // copy motor positions to buffer
			cli();
			positron[i]=pos[i];
			sei();
		}
		for(byte i=0; i<3; i++){ // print motor positions
			Serial.print(positron[i]);
			Serial.print(", ");
		}
		Serial.println((slew.DRV_STATUS() & 0x3FFUL) , DEC); // stallGuard reading
	}
}

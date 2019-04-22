// This code is supposed to read commands from serial and control 3 steppers.
// This works at least with atmega 328p microcontroller (Arduino Uno or Nano)
/* todo:
 * slew homing with hall sensor (can be simultaneous with trolley homing)
 * smooth transition from slow mode to fast mode
 * user shouldnt be able to switch to silent mode during homing
 * combine with ethernet code
 * real acceleration setting instead of acl
 * joystick smoothing? jerk limit? increase acceleration resolution?
 * make hook stop before it hits trolley to keep string loose for better trolley homing
 * make trolley slow down before edges to limit sway
 * adjust sg_stall_value based on input voltage
 * POWER & TORQUE:
	 * adjust setCurrent, power_down_delay, microsteps etc.
	 * enable coolStep for power savings and less heating
	 * high torque mode for heavy lifting (and homing?), low torque for power savings
	 * use stallGuard value to limit speed to prevent motors stalling
 * add neoPixel leds for cool light effects
 * isr is not sending step pulses perfectly evenly when spinning many motors at same time
*/

// a motor can never spin too fast, right?
#pragma GCC optimize ("-O2") // https://www.instructables.com/id/Arduino-IDE-16x-compiler-optimisations-faster-code/

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

// global variables
volatile unsigned long
	kid[3]={0xFFFF00,0xFFFF00,0xFFFF00}, // CPU cycles to wait between steps for each motor
	boy[3]={0xFFFF00,0xFFFF00,0xFFFF00}; // CPU cycles left until the motor needs to be stepped again
volatile bool motOn[3]={0,0,0}; // which motors are spinning
volatile bool dir[3]={0,0,0}; // slew, trolley, hook direction
volatile long
	pos[3]={0,0,0}, // motor step positions
	posMax=2E9, posMin=-2E9,
	posTop=2E9;
volatile byte homing=0;
unsigned long fast[3]; // motor max speeds
unsigned long acl=10; // acceleration setting
char goal0=0, goal1=0, goal2=0;
char spd[3]={0,0,0};

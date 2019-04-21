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
	trolley.coolstep_min_speed(200);
	trolley.diag1_stall(1);
	trolley.sg_stall_value(15);

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

void silentMode(){
	slew.stealth_max_speed(10);
	trolley.stealth_max_speed(10);
	hook.stealth_max_speed(10);
	fast[0]=2000000;
	fast[1]=8000000;
	fast[2]=15000000;
	acl=2; // todo switch from this hack to a true acceleration setting
}

void fastMode(){
	slew.stealth_max_speed(10000);
	trolley.stealth_max_speed(10000);
	hook.stealth_max_speed(10000);
	fast[0]=400000;
	fast[1]=2000000;
	fast[2]=2000000;
	acl=10;
}

void setup() {
	DDRD |= 0b01110000; // step pins outputs
	Serial.begin(250000); // Set baud rate in serial monitor
	// let's enable timer1 to time the step pulses. See p113 here https://www.sparkfun.com/datasheets/Components/SMD/ATMega328.pdf
	TCCR1A=B00000000; //p134
	TIMSK1=B00100000; //p139
	fox(1000);
	pinMode(A3,INPUT_PULLUP); // slack detector
	pinMode(8,INPUT_PULLUP); // diag1 trolley
	//pinMode(A7,INPUT); // some random line here or i get compiler error
}

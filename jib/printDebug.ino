void printDebug()
{
	bool say=0;
	//Serial.print(analogRead(A7)); // print hall sensor readings
	
	long positron[3];
	static long positronOld[3]={0,0,0};
	for(byte i=0; i<3; i++){ // copy motor positions to buffer
		cli();
		positron[i]=pos[i];
		sei();
		if (positron[i] != positronOld[i]){
			say=1;
			positronOld[i]=positron[i];
		}
	}
	
	const int
		stallGuardSlew = slew.DRV_STATUS() & 0x3FFUL, // todo remove UL?
		stallGuardTrolley = trolley.DRV_STATUS() & 0x3FFUL,
		stallGuardHook = hook.DRV_STATUS() & 0x3FFUL;
		
	const float Vin=analogRead(A7)*0.03812; // input voltage
	static float VinOld=0;
	if(Vin < VinOld-2|| Vin > VinOld+2){ // hysteresis to not print voltage ripple
		say=1;
		VinOld=Vin;
	}

	static char speed1Old=0;
	if(speed1 != speed1Old){
		say=1;
		speed1Old=speed1;
	}

	static byte homingOld=0;
	if(homing != homingOld){
		say=1;
		homingOld=homing;
	}
	
	if(say){
		for(byte i=0; i<3; i++){ // print motor positions
			Serial.print(positron[i]);
			Serial.print(", ");
		}
		Serial.print("  ");
		Serial.print(stallGuardSlew, DEC);
		Serial.print(", ");
		Serial.print(stallGuardTrolley, DEC);
		Serial.print(", ");
		Serial.print(stallGuardHook, DEC);
		if(PINB & 1==0) Serial.print(", trolley stalled");
		Serial.print(",   ");
		Serial.print(Vin,1);
		Serial.print(", ");
		Serial.print(speed1,DEC);
		Serial.print(", ");
		Serial.print(homingOld,DEC);
		Serial.println();
	}

	static bool enabled=0;
	if(enabled){
		if(Vin<5){
			Serial.println("Drivers off");
			enabled=0;
		}
	}
	else if(Vin>6){ // auto re-enable drivers after power off
		Serial.println("Drivers on");
		settings(); // this function blocks for half a second
		enabled=1;
	}
}

void printDebug()
{
	//Serial.print(analogRead(A7)); // print hall sensor readings
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
	Serial.print("  ");
	Serial.print((slew.DRV_STATUS() & 0x3FFUL) , DEC); // stallGuard reading
	Serial.print(", ");
	Serial.print((trolley.DRV_STATUS() & 0x3FFUL) , DEC);
	Serial.print(", ");
	Serial.print((hook.DRV_STATUS() & 0x3FFUL) , DEC);
	if(PINB & 1==0){
		Serial.print(", trolley stalled");
	}
	Serial.print(",   ");
	const float Vin=analogRead(A7)*0.03812; // input voltage
	Serial.print(Vin,1);
	static bool enabled=0;
	if(enabled){
		if(Vin<5){
			Serial.print(", Off");
			enabled=0;
		}
	}
	else if(Vin>6){ // auto re-enable drivers after power off
		Serial.print(", On");
		settings(); // this function blocks for half a second
		enabled=1;
	}
	Serial.print(", ");
	Serial.print(speed1,DEC);
	Serial.print(", ");
	Serial.print(homing,DEC);
	Serial.println();
}

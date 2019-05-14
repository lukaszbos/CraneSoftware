// homing function
void home(){
	if(homing==1){ // start homing
		Serial.println("Lowering hook");
		posTop=2E9;
		fastMode();
		goal0=0;
		goal1=0;
		goal2=-20;
		homing=2;
	}
	else if(homing==2){
		if(spd[2]<=-20){
			Serial.println("Raising hook");
			goal2=50;
			homing=3;
		}
	}
	else if(homing==4){
		Serial.println("Hook stalled. Lowering hook a bit");
		delay(50);
		hook.shaft_dir(!dir[2]);
		for(byte i=0; i<9; i++){
			delay(10);
			PORTD ^= 1<<6;
		}
		hook.shaft_dir(dir[2]);
		cli();
		pos[2]=0;
		posTop=0;
		sei();
		Serial.println("Homing trolley and slew");
		posMin=-2E9;
		homing=5;
		homeSlew=1;
		goal0=126;
		homeTrolley=1;
		goal1=-126;
	}
	else if(homing==5){
		if(homeTrolley==2){
			Serial.println("Edge detected");
			cli();
			posMin=0;
			pos[1]=-20; // stop before edge
			sei();
			posMax=2E9;
			delay(50);
			goal1=126; // change direction
			homeTrolley=3;
		}
		else if(homeTrolley==4){
			Serial.println("Trolley homed");
			goal1=0;
			cli();
			posMax=pos[1]-20;
			sei();
			homeTrolley=0;
		}
		if(homeSlew==3){
			goal0=0;
			Serial.println("Slew homed");
			homeSlew=0;
		}
		if(homeSlew==0 && homeTrolley==0){
			Serial.println("Homing finished");
			homing=0;
		}
	}
}

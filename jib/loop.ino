void loop() {
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

		cli(); // trolley
		const long pos_=pos[1];
		sei();
		if(speed1<goal1) speed1++;
		else if(speed1>goal1) speed1--;
		if(pos_>=posMax && speed1>0 || pos_<=posMin && speed1<0) speed1=0;
		newDir=speed1<0?0:1;
		if (newDir!=dir[1]){
			trolley.shaft_dir(newDir);
			dir[1]=newDir;
		}
		setSpeed(1,speed1==0?0:fast[1]/abs(speed1));

		if(s2<goal2) s2++; // hook
		else if(s2>goal2) s2--;
		newDir=s2>0?0:1;
		if (newDir!=dir[2]){
			hook.shaft_dir(newDir);
			dir[2]=newDir;
		}
		if(newDir==0 && digitalRead(A3)==0){ // slack detection
			s2=0;
			goal2=0;
			setSpeed(2,0);
		}
		else setSpeed(2,s2==0?0:fast[2]/abs(s2));
	}
	
	if(Serial.available()){ // receive commands from Python code
		static byte job=255;
		char wax=Serial.read();
		if(wax==127 && homing==0) job=0; // speed packet start character is 127
		else if(wax==-127) job=4; // -127 indicates that next byte will be settings
		else if(job<3){ // or else it must be a speed command -126 to 126
			if(job==0) goal0=wax;
			if(job==1) goal1=wax;
			if(job==2) goal2=wax;
			++job;
		}
		else if(job==4){ // decode settings byte
			if(wax & 2) homing=1;
			else{
				if(wax & 1){
					Serial.println("Silent mode");
					silentMode();
				}else{
					Serial.println("Fast mode");
					fastMode();
				}
			}
			++job;
		}
	}

	if(homing>0){ // homing function
		if(homing==1){ // start homing
			Serial.println("Homing");
			fastMode();
			posMin=-2E9;
			goal1=-50;
			homing=2;
		}
		else if(homing==3){ // change direction
			Serial.println("Edge detected");
			cli();
			posMin=0;
			pos[1]=-20; // stop before edge
			sei();
			posMax=2E9;
			goal1=50;
			homing=4;
		}
		else if(homing==5){
			cli();
			posMax=pos[1]-20;
			sei();
			Serial.println("Homing finished");
			homing=0;
		}
	}
	
	static unsigned long owl=0;
	if(now-owl>200){ // prints various numbers to serial
		owl=now;
		printDebug();
	}
}

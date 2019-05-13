void loop() {
	const unsigned long now=millis();
	static unsigned long timeReceived = 0;

	// send some random data to PC
	Udp.beginPacket(ip_server, localPort);
	Udp.write(ReplyBuffer);
	if(Udp.endPacket()) Serial.println("Send OK");
	else Serial.println("Send failed");
	
	// receive commands from PC through Ethernet
	const byte packetSize = Udp.parsePacket();
	if (packetSize) {
		timeReceived=now;
		Serial.print(packetSize);
		Serial.print(" bytes from ");
		IPAddress remote = Udp.remoteIP();
		for (int i=0; i < 4; i++) {
		Serial.print(remote[i], DEC);
			if (i < 3) {
				Serial.print(".");
			}
		}
		Serial.print(", port ");
		Serial.print(Udp.remotePort());
		
		// read the packet into packetBufffer
		Udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE);
		goal0=packetBuffer[0];
		goal1=packetBuffer[1];
		goal2=packetBuffer[2];
		Serial.print(", contents ");
		Serial.print(packetBuffer[0],DEC);
		Serial.print(" ");
		Serial.print(packetBuffer[1],DEC);
		Serial.print(" ");
		Serial.print(packetBuffer[2],DEC);
		Serial.print(" ");
		Serial.print(packetBuffer[3],DEC);
		Serial.println();
	}
	delay(10);

	static unsigned long then=0;
	
	if(now-then>acl){ //accelerate slowly
		then=now;

		// slew
		if(spd[0]<goal0) spd[0]++; else
		if(spd[0]>goal0) spd[0]--;
		static bool newDir0=0;
		if(spd[0]>0) newDir0=1; else
		if(spd[0]<0) newDir0=0;
		if (newDir0!=dir[0]){
			slew.shaft_dir(newDir0);
			dir[0]=newDir0;
		}
		setSpeed(0,spd[0]==0?0:fast[0]/abs(spd[0]));

		// trolley
		if(spd[1]<goal1) spd[1]++; else
		if(spd[1]>goal1) spd[1]--;
		cli();
		const long pos_=pos[1];
		sei();
		if(pos_>=posMax && spd[1]>0 || pos_<=posMin && spd[1]<0) spd[1]=0;
		static bool newDir1=0;
		if(spd[1]>0) newDir1=1; else
		if(spd[1]<0) newDir1=0;
		if (newDir1!=dir[1]){
			trolley.shaft_dir(newDir1);
			dir[1]=newDir1;
		}
		setSpeed(1,spd[1]==0?0:fast[1]/abs(spd[1]));

		// hook
		if(spd[2]<goal2) spd[2]++; else
		if(spd[2]>goal2) spd[2]--;
		cli();
		const long posHook=pos[2];
		sei();
		if(posHook>=posTop && spd[2]>0) spd[2]=0;
		static bool newDir2=0;
		if(spd[2]>0) newDir2=1; else
		if(spd[2]<0) newDir2=0;
		if (newDir2!=dir[2]){
			hook.shaft_dir(newDir2);
			dir[2]=newDir2;
		}
		if(newDir2==0 && (PINC&8)==0){ // slack detection
			spd[2]=0;
			goal2=0;
			setSpeed(2,0);
		}
		else setSpeed(2,spd[2]==0?0:fast[2]/abs(spd[2]));
	}

	// receive commands from PC through USB
	if(Serial.available()){
		timeReceived = now;
		static byte job=255;
		char wax=Serial.read();
		if(wax==127 && homing==0) job=0; // speed packet start character is 127
		else if(wax==-127) job=4; // -127 indicates that next byte will be settings
		else if(job<3){ // or else it must be a speed command -126 to 126
			if(job==0) goal0=wax; else
			if(job==1) goal1=wax; else
			if(job==2) goal2=wax;
			++job;
		}
		else if(job==4){ // decode settings byte
			if(wax & 4){ // stop motors now
				goal0=0; goal1=0; goal2=0;
				spd[0]=0; spd[1]=0; spd[2]=0;
				setSpeed(0,0); setSpeed(1,0); setSpeed(2,0);
				homing=0; homeTrolley=0; homeSlew=0;
				posMax=2E9; posMin=-2E9; posTop=2E9;
			}else{
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
			}
			++job;
		}
	}

	if(now - timeReceived > 1000){
		goal0=0; goal1=0; goal2=0;
	}
	
	if(homing>0) home();
	
	static unsigned long owl=0;
	if(now-owl>1000){ // prints various numbers to serial
		owl=now;
		printDebug();
	}

	static unsigned long rat=0;
	if(spd[0]==0 && spd[1]==0 && spd[2]==0 && now-rat>40){
		rat=now;
		larsonScanner();
	}
	
}

void loop() {
	const unsigned long now=millis();
	static unsigned long timeReceived=0, timeSerial=0;
	
	// receive commands from PC through Ethernet
	if(ethernetConnected){
		const bool debugger=0;
		const byte packetSize = Udp.parsePacket();
		if (packetSize) {
			timeReceived=now;
			if(debugger){
				Serial.print(packetSize);
				Serial.print(" bytes from ");
				IPAddress remote = Udp.remoteIP();
				for (int i=0; i < 4; i++) {
					Serial.print(remote[i], DEC);
					if (i < 3) Serial.print(".");
				}
				Serial.print(", port ");
				Serial.println(Udp.remotePort());
			}
			
			// read the packet into packetBuffer
			Udp.read(packetBuffer, packetSize);
			if(packetSize<5){
				/*goal0=packetBuffer[0];
				goal1=packetBuffer[1];
				goal2=packetBuffer[2];*/
				if(debugger){
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
			}else{
				if(debugger){
					Serial.println(packetBuffer);
				}
				char* token;
				char* rest = packetBuffer;
				int iterator;
				int valuesFromController[6];
				int xMapped;

				while (token = strtok_r(rest, " ", &rest)) {
					/*if(debugger){
						Serial.print(F("Token "));
						Serial.print(token);
					}*/
					double x;

					if (String(token) == "s"){
						iterator = 0;
					}
					else{
						if (String(token) == "e"){
							if(homing==0){
								goal0=valuesFromController[0];
								goal1=valuesFromController[1];
								goal2=valuesFromController[2];
								static byte oldMode=2; // 1=fast, 0=slow
								if(valuesFromController[4] != oldMode){
									oldMode=valuesFromController[4];
									if(oldMode) fastMode();
									else silentMode();
								}
							}
							if(valuesFromController[5]){
								slew.hold_current(0);
								trolley.hold_current(0);
								hook.hold_current(0);
								stopMotors();
								while(1){
									led.fill(0xFF0000);
									led.show();
									delay(300);
									led.clear();
									led.show();
									delay(300);
								}
							}
							else if(valuesFromController[3]) homing=1;
							/*if(debugger){
								Serial.print(" ");
								Serial.print(valuesFromController[0]);
								Serial.print(" ");
								Serial.print(valuesFromController[1]);
								Serial.print(" ");
								Serial.print(valuesFromController[2]);
								Serial.print(" ");
								Serial.println(valuesFromController[3]);
							}*/
						}
						
						x = atof(token); 
						
						if(iterator < 3){
							x = x * 100;
							xMapped = map(x, 0.00, 200.00, -126, 126);
							valuesFromController[iterator] = xMapped; 
						}else{
							valuesFromController[iterator] = x; 
						}
						iterator++;
					}
				}
			}
		}
	}

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
		timeSerial = now;
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
			if(wax & 4){
				stopMotors();
			}else{
				if(wax & 2) homing=1;
				else{
					if(wax & 1) silentMode();
					else fastMode();
				}
			}
			++job;
		}
	}

	static bool serialOld=serialActive;
	serialActive = now-timeSerial<1000?1:0;
	static unsigned long rat=0;
	if((serialActive>serialOld) || (spd[0]==0 && spd[1]==0 && spd[2]==0 && now-rat>40)){
		rat=now;
		larsonScanner();
		serialOld=serialActive;
	}

	if(now - timeReceived > 1000){
		goal0=0; goal1=0; goal2=0;
	}
	
	if(homing>0) home();
	
	static unsigned long owl=0;
	if(now-owl>200){
		owl=now;
		//Serial.println(goal2,DEC);
		printDebug();
	}

	if(ethernetConnected){
		static unsigned long dad=0;
		if(now-dad>50){
			dad=now;
			// send some data to PC
			Udp.beginPacket(ip_server, localPort);
			Udp.write(ReplyBuffer);
			if(Udp.endPacket()==0){
				Serial.println(F("UDP send failed. :("));
				Udp.stop();
				ethernetConnected=0;
			}
		}
		if(serialActive){
			Udp.stop();
			ethernetConnected=0;
			Serial.println(F("Serial active --> UDP closed. :)"));
		}
		if(Ethernet.linkStatus()==LinkOFF){
			Serial.println(F("Ethernet cable unplugged. :("));
			Udp.stop();
			ethernetConnected=0;
		}
	}else{
		if(!serialActive && Ethernet.linkStatus()==LinkON && Udp.begin(localPort)){
			Serial.println(F("UDP socket opened. :)"));
			ethernetConnected=1;
		}
	}
}

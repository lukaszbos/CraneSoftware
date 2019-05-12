// Interrupt Service Routine that automatically keeps stepping motors
ISR(TIMER1_CAPT_vect) // http://www.gammon.com.au/interrupts
{
	static bool man[3]={0}; // which motors to step next
	
	// slew
	if(motOn[0] && man[0])
	{
		if(homeSlew>0) // homing mode
		{
			const int box = analogRead(A6);
			if(homeSlew==1 && box>923)
			{
				homeSlew=2;
			}
			else if(homeSlew==2 && box<512)
			{
				homeSlew=3;
				pos[0]=0;
			}
		}
		if(dir[0]) ++pos[0];
		else --pos[0];
		PORTD ^= 1<<4; // https://www.arduino.cc/en/Reference/PortManipulation
	}
	
	// trolley
	if(motOn[1] && man[1])
	{
		if(homeTrolley>0) // homing mode
		{
			if(PINB & 1) // trolley stallGuard diag1 high
			{
				if(dir[1]) ++pos[1];
				else --pos[1];
				PORTD ^= 1<<5;
			}
			else // diag1 low, stall detected during homing
			{
				motOn[1]=0;
				kid[1]=0xFFFF00;
				spd[1]=0;
				goal1=0;
				++homeTrolley;
			}
		}
		else // normal mode
		{
			if(dir[1])
			{
				if(pos[1]<posMax)
				{
					++pos[1];
					PORTD ^= 1<<5;
				}
			}
			else if(pos[1]>posMin)
			{
				--pos[1];
				PORTD ^= 1<<5;
			}
		}
	}

	// hook
	if(motOn[2] && man[2])
	{
		if(homing>0) // homing mode
		{
			if(PINB & 2)
			{
				++pos[2];
				PORTD ^= 1<<6;
			}
			else // stall detected
			{
				motOn[2]=0;
				kid[2]=0xFFFF00;
				spd[2]=0;
				goal2=0;
				homing++;
			}
		}
		else // normal mode
		{
			if(dir[2])
			{
				if(pos[2]<posTop)
				{
					++pos[2];
					PORTD ^= 1<<6;
				}
			}
			else
			{
				--pos[2];
				PORTD ^= 1<<6;
			}
		}
	}

	// if new speed is higher than before
 	if(kid[0]<boy[0]) boy[0]=kid[0];
 	if(kid[1]<boy[1]) boy[1]=kid[1];
 	if(kid[2]<boy[2]) boy[2]=kid[2];

	// find who is the smallest boy
	unsigned long small=160000; // set maximum ISR refresh period
	if(boy[0]<=boy[1] && boy[0]<=boy[2] && boy[0]<=small)
	{
		man[0]=1;
		small=boy[0];
	}
	else man[0]=0;
	if(boy[1]<=boy[0] && boy[1]<=boy[2] && boy[1]<=small)
	{
		man[1]=1;
		small=boy[1];
	}
	else man[1]=0;
	if(boy[2]<=boy[0] && boy[2]<=boy[1] && boy[2]<=small)
	{
		man[2]=1;
		small=boy[2];
	}
	else man[2]=0;

	// update boys
	boy[0]-=small;
	boy[1]-=small;
	boy[2]-=small;
	if(boy[0]==0) boy[0]=kid[0];
	if(boy[1]==0) boy[1]=kid[1];
	if(boy[2]==0) boy[2]=kid[2];
	
	fox(small); // set timer to wait for next motor step
}

volatile byte rat=0;
ISR(TIMER1_OVF_vect)
{
	++rat;
}

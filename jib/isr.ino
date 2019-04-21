// Interrupt Service Routine that automatically keeps stepping motors
ISR(TIMER1_CAPT_vect) // http://www.gammon.com.au/interrupts
{
	static bool man[3]={0}; // which motors to step next
	
	// toggles step pin(s)
	if(motOn[0] && man[0]) //slew
	{
		if(dir[0]) ++pos[0];
		else --pos[0];
		PORTD ^= 1<<4; // https://www.arduino.cc/en/Reference/PortManipulation
	}
	if(motOn[1] && man[1]) //trolley
	{
		if(homing>0) // homing mode
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
				homing++;
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
	if(motOn[2] && man[2]) //hook
	{
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

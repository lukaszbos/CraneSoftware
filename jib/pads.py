# Hello, Joel here. Before running this code, connect one or more gamepads and arduinos to the computer. This code sends commands from the pads to several arduinos through serial (USB wire). This code is not yet finished.

# libraries you may need to install with pip
import pygame # https://www.pygame.org/docs/ref/joystick.html I took this code from here.
import serial # https://playground.arduino.cc/interfacing/python
import serial.tools.list_ports

# comes with Python 3.7.2
import struct # https://docs.python.org/2/library/struct.html
import threading
import time

def monitor(fan): # prints whatever arduino sends us
	while True:
		try:
			print(fan.readline().rstrip().decode())
		except:
			break

# Define some colors
BLACK=(0,0,0)
WHITE=(255,255,255)

# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint:
	def __init__(self):
		self.reset()
		self.font = pygame.font.SysFont('Calibri', 17, bold=False, italic=False)
	def print(self, screen, textString):
		textBitmap = self.font.render(textString, True, WHITE)
		screen.blit(textBitmap, [self.x, self.y])
		self.y += self.line_height
	def reset(self):
		self.x = 10
		self.y = 10
		self.line_height = 15
	def indent(self):
		self.x += 10
	def unindent(self):
		self.x -= 10

pygame.init()
screen = pygame.display.set_mode([300, 700]) # screen size [width,height]
pygame.display.set_caption("pads PdP MiCrane")
done = False #Loop until the user clicks the close button.
clock = pygame.time.Clock() # Used to manage how fast the screen updates
pygame.joystick.init() # Initialize the joysticks
textPrint = TextPrint() # Get ready to print

def deadzone(wolf): # calculates deadzones for DualShock4
	zone=0.1
	if wolf>=zone:
		return int((wolf-zone)/(1-zone)*125.01+1) # 1 to 126
	elif wolf<=-zone:
		return int((wolf+zone)/(1-zone)*125-1) # -1 to -126
	else: # we are in deadzone
		return int(0) # means don't move

ser=[None,None,None,None,None,None]
wax=0
oldSilent=[0,0,0,0,0,0,0,0]
newSilent=[0,0,0,0,0,0,0,0]
oldFast=[0,0,0,0,0,0,0,0]
newFast=[0,0,0,0,0,0,0,0]
oldHome=[0,0,0,0,0,0,0,0]
newHome=[0,0,0,0,0,0,0,0]
slewOld=0
trolleyOld=0
hookOld=0
mode=False
armed=[False,False,False,False,False,False,False,False]

# opens COM ports
comCount=0
for dog in serial.tools.list_ports.comports():
	try:
		ser[comCount] = serial.Serial(dog.device,250000) # port, baud rate
	except:
		print('Problem with ',dog)
	else:
		threading.Thread(target=monitor, args=(ser[comCount],)).start()
		comCount+=1
		print('Connected ',dog)
if comCount is 0:
	print('Plug Arduino USB cable and relaunch me.')

# -------- Main Program Loop -----------
while done==False:
	for event in pygame.event.get(): # User did something
		if event.type == pygame.QUIT: # If user clicked close
			done=True # Flag that we are done so we exit this loop					
	screen.fill(BLACK)
	textPrint.reset()
	joystick_count = pygame.joystick.get_count()
	textPrint.print(screen, "Number of joysticks: {}".format(joystick_count) )
	textPrint.indent()
	
	slew=0
	trolley=0
	hook=0
	send=0
	stopping=False
	homing=False
	
	# For each pad:
	for i in range(joystick_count):
		pad = pygame.joystick.Joystick(i)
		pad.init()
		textPrint.print(screen, "Joystick {} : {}".format(i,pad.get_name()) )
		textPrint.indent()
		
		# Usually axis run in pairs, up/down for one, and left/right for
		# the other.
		axes = pad.get_numaxes()
		textPrint.print(screen, "Number of axes: {}".format(axes) )
		textPrint.indent()
		
		show=False
		for j in range( axes ):
			if pad.get_axis(j) != 0:
				show=True
		if show:
			for j in range( axes ):
				textPrint.print(screen, "Axis {} : {:>6.3f}".format(j, pad.get_axis(j)) )
		textPrint.unindent()
				
		buttons = pad.get_numbuttons()
		textPrint.print(screen, "Number of buttons: {}".format(buttons) )
		textPrint.indent()

		for j in range( buttons ):
			button = pad.get_button( j )
			if button is 1:
				textPrint.print(screen, "Button {:>2}".format(j) )
		textPrint.unindent()
		textPrint.unindent()
		
		newSilent[i]=pad.get_button(1) # silent mode
		if newSilent[i]>oldSilent[i]:
			wax |= 1
			send=1
		oldSilent[i]=newSilent[i]
		newFast[i]=pad.get_button(2) # fast mode
		if newFast[i]>oldFast[i]:
			wax &= ~1
			send=1
		oldFast[i]=newFast[i]
		newHome[i]=pad.get_button(8) # home
		if newHome[i]>oldHome[i]:
			wax |= 2
			send=1
			homing=True
		else: # don't home again
			wax &= ~2
		oldHome[i]=newHome[i]
		if pad.get_button(9): # switch joystick modes
			if armed[i]:
				mode = not mode
				armed[i]=False
		else:
			armed[i]=True
		if pad.get_button(13): # stop motors button
			wax |= 4
			send=1
			slew0=0
			trolley0=0
			hook0=0
			stopping=True
		else:
			if stopping == False:
				wax &= ~4
				trolley0=deadzone(pad.get_axis(1)) # DualShock4 doesn't have built in deadzones, so we do that here in software.
			if mode:
				slew0=-deadzone(pad.get_axis(0))
				hook0=deadzone(pad.get_axis(3))
			else:
				slew0=int((pad.get_axis(5)-pad.get_axis(4))*63.01)
				hook0=-deadzone(pad.get_axis(3))
		if slew0!=0:
			slew=slew0
		if trolley0!=0:
			trolley=trolley0
		if hook0!=0:
			hook=hook0
	
	#For each arduino
	for i in range(comCount):
		if ser[i] is not None:
			if slew!=slewOld or trolley!=trolleyOld or hook!=hookOld or slew!=0 or trolley!=0 or hook!=0:
				msg=struct.pack('>bbbb',127,slew,trolley,hook)
				try:
					ser[i].write(bytes(msg))
				except:
					ser[i]=None
				else:
					slewOld=slew
					trolleyOld=trolley
					hookOld=hook
					textPrint.print(screen,"Sent: {}".format(msg))
	if send:
		msg=struct.pack('>bb',-127,wax)
		for i in range(comCount):
			if ser[i] is not None:
				try:
					ser[i].write(bytes(msg)) # sometimes send also settings
				except:
					ser[i]=None
				else:
					textPrint.print(screen,"Sent: {}".format(msg))
		send=0
		wax &= ~2 # stop homing
	# ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
	pygame.display.flip()
	clock.tick(20)
ser.close()
pygame.quit ()
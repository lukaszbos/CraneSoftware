# Hello, Joel here. Before running this code, connect one or more gamepads to the computer. This code detects which of the pads are Spartan Gear Oplon and which are Sony DualShock4 and reads 3 joysticks from each pad. The code then notices if a joystick on any of the connected pads is being turned by someone and sends that joystick position to arduino through serial (USB wire). This keeps repeating forever.

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
pygame.display.set_caption("PdP MiCrane gamepad")
done = False #Loop until the user clicks the close button.
clock = pygame.time.Clock() # Used to manage how fast the screen updates
pygame.joystick.init() # Initialize the joysticks
textPrint = TextPrint() # Get ready to print

def deadzone(wolf): # calculates deadzones for DualShock4
	if wolf>=0.1:
		return int((wolf-0.1)/0.9*125+1) # 1 to 126
	elif wolf<=-0.1:
		return int((wolf+0.1)/0.9*125-1) # -1 to -126
	else: # we are in deadzone
		return int(0) # means don't move

ser=None
cat=None
say=False
old=0
# -------- Main Program Loop -----------
while done==False:
	if ser is None: # auto select arduino COM port
		if cat is None:
			now=time.time()
			if now-old > 1 : # reduces CPU usage
				old=now
				for dog in serial.tools.list_ports.comports():
					print(dog)
					cat=dog.device
				if say is False:
					say=True
					if cat is None:
						print('Plug Arduino USB cable.')
		else:
			try:
				ser = serial.Serial(cat,250000) # port, baud rate
			except:
				pass
			else:
				threading.Thread(target=monitor, args=(ser,)).start()

	# EVENT PROCESSING STEP
	for event in pygame.event.get(): # User did something
		if event.type == pygame.QUIT: # If user clicked close
			done=True # Flag that we are done so we exit this loop					

	# DRAWING STEP
	# First, clear the screen to white. Don't put other drawing commands
	# above this, or they will be erased with this command.
	screen.fill(BLACK)
	textPrint.reset()

	# Get count of joysticks
	joystick_count = pygame.joystick.get_count()

	textPrint.print(screen, "Number of joysticks: {}".format(joystick_count) )
	textPrint.indent()
	
	slew=0
	trolley=0
	hook=0
	wax=0
	flag=0
	
	# For each joystick:
	for i in range(joystick_count):
		pad = pygame.joystick.Joystick(i)
		pad.init()

		textPrint.print(screen, "Joystick {}".format(i) )
		textPrint.indent()

		# Get the name from the OS for the controller/joystick
		name = pad.get_name()
		textPrint.print(screen, "Joystick name: {}".format(name) )
		
		# Usually axis run in pairs, up/down for one, and left/right for
		# the other.
		axes = pad.get_numaxes()
		textPrint.print(screen, "Number of axes: {}".format(axes) )
		textPrint.indent()
		
		for i in range( axes ):
			axis = pad.get_axis( i )
			textPrint.print(screen, "Axis {} value: {:>6.3f}".format(i, axis) )
		textPrint.unindent()
		textPrint.unindent()
		
		if pad.get_name() == 'Wireless Controller': # bluetooth DualShock4
			if pad.get_button(1): # button pressed, we are sending settings flag later
				wax=1
				flag=1
			if pad.get_button(2):
				wax=0
				flag=1
			slew0=int((pad.get_axis(4)-pad.get_axis(5))*63) # DualShock4 doesn't have built in deadzones, so we do that here in software.
			trolley0=deadzone(pad.get_axis(1))
			hook0=deadzone(pad.get_axis(3))
		else: # USB wired Spartan has built in deadzones. A bit easier to code here, but not as precise control as DualShock4.
			slew0=int(pad.get_axis(0)*126)
			trolley0=int(pad.get_axis(1)*126)
			hook0=int(pad.get_axis(3)*126)
		if slew0!=0:
			slew=slew0
		if trolley0!=0:
			trolley=trolley0
		if hook0!=0:
			hook=hook0
		
	if ser != None:
		try:
			ser.write(bytes(struct.pack('>bbbb',127,slew,trolley,hook))) # send 4 bytes to Arduino. The first one, 127, is packet start byte. After that comes three joystick positions as a number between -126 to 126.
		except:
			ser=None
			cat=None
			say=False
		else:
			if flag:
				try:
					ser.write(bytes(struct.pack('>bb',-127,wax))) # maybe send also settings
				except:
					pass
				else:
					flag=0
	
	# ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
	
	# Go ahead and update the screen with what we've drawn.
	pygame.display.flip()
	
	# Limit to 20 frames per second
	clock.tick(60)
		
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
ser.close()
pygame.quit ()
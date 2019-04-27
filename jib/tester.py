# libraries you may need to install with pip
import pygame # https://www.pygame.org/docs/ref/joystick.html I took this code from here.

# Define some colors
BLACK		= (	 0,	 0,	 0)
WHITE		= ( 255, 255, 255)

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
 
size = [300, 700] # screen size [width,height]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("PdP MiCrane gamepad")
done = False #Loop until the user clicks the close button.
clock = pygame.time.Clock() # Used to manage how fast the screen updates
pygame.joystick.init() # Initialize the joysticks
textPrint = TextPrint() # Get ready to print

# -------- Main Program Loop -----------
while done==False:
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
					
			buttons = pad.get_numbuttons()
			textPrint.print(screen, "Number of buttons: {}".format(buttons) )
			textPrint.indent()

			for i in range( buttons ):
					button = pad.get_button( i )
					textPrint.print(screen, "Button {:>2} value: {}".format(i,button) )
			textPrint.unindent()
					
			# Hat switch. All or nothing for direction, not like joysticks.
			# Value comes back in an array.
			hats = pad.get_numhats()
			textPrint.print(screen, "Number of hats: {}".format(hats) )
			textPrint.indent()

			for i in range( hats ):
					hat = pad.get_hat( i )
					textPrint.print(screen, "Hat {} value: {}".format(i, str(hat)) )
			textPrint.unindent()
			textPrint.unindent()
		
		# ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
		
		# Go ahead and update the screen with what we've drawn.
		pygame.display.flip()
		
		# Limit to 20 frames per second
		clock.tick(20)
		
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit ()
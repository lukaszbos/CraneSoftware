import logging
import pygame
import Controller
import textprint

from threading import *
from typing import List

'''
    PadClient.py: it contains definition of PadClient() class. It is responsible for handling getting information from 
    game-pads, and adding commands from each pad to pad command queue

    Authors: Lukasz Michowski, Mateusz Jaszek
'''
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(asctime)s %(threadName)-10s %(message)s',
                    datefmt='%m/%d/%Y  %I:%M:%S %p')


class PadClient(Thread):
    def __init__(self, name, index, lock, queue):
        Thread.__init__(self, name=name)

        self.lock = lock
        self.queue = queue
        self.name = name
        self.index = index
        # self.pad = controller.Controller()
        self.myControllers = []

    _running = False

    def run(self):
        logging.info('Starting')
        numberOfPads = 4
        self.fillListOfControllers(numberOfPads)
        '''
        Value Matrix scheme - data from each pad is passed to DataExchangeThread in this form:
             | var0 | var1 | var2 | var3
        pad0 | int  | int  | int  | int
        pad1 | int  | int  | int  | int
        pad2 | int  | int  | int  | int
        pad3 | int  | int  | int  | int
        '''

        pygame.init()
        self.threadLoop()
        pygame.quit()

    #   threadLoop() checks for changes in any of connected gamepads and later it sets newest data into the queue
    def threadLoop(self):
        controllerValueMatrix = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
        while True:
            try:
                self.padHandler()
            except Exception as e:
                logging.info(f'-> Exception has happened. Exception: {e} \n '
                             f'GamePads might not be connected properly')
            controllerValueMatrix: List[List[int]]
            for pad in self.myControllers:
                controllerValueMatrix[pad.index] = pad.getValueList()
            self.queue.put(controllerValueMatrix)

    def fillListOfControllers(self, numberOfPads):
        for i in range(numberOfPads):
            self.myControllers.append(Controller.Controller(i))

    # Method responsible for handling Pads connected to computer
    # to fully understand padHandler method check: https://www.pygame.org/docs/ref/joystick.html and Controller class
    # what it simply do is it loops by every button of every connected to computer controller, displays the data
    # to the screen and also updates myControllers List
    def padHandler(self):

        # Set the width and height of the screen [width,height]
        size = [500, 700]
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Mi Crane")
        # Loop until the user clicks the close button.
        done = False
        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()
        # Initialize the joysticks
        pygame.joystick.init()
        # Get ready to print
        textPrint = textprint.TextPrint()
        # while done == False:
        # EVENT PROCESSING STEP
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
            #   These are not necessary
            # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
            # if event.type == pygame.JOYBUTTONDOWN:
            #     print("Joystick button pressed.")
            # if event.type == pygame.JOYBUTTONUP:
            #     print("Joystick button released.")
        # DRAWING STEP
        # First, clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
        screen.fill(textprint.WHITE)
        textPrint.reset()

        # Get count of joysticks
        joystick_count = pygame.joystick.get_count()

        textPrint.print(screen, "Number of joysticks: {}".format(joystick_count))
        textPrint.indent()

        # For each joystick:
        for i in range(joystick_count):
            joystickInUse = i
            # print("joystickInUse")
            # print(joystickInUse)
            joystick = pygame.joystick.Joystick(i)
            joystick.init()

            textPrint.print(screen, "Joystick {}".format(i))
            textPrint.indent()

            # Get the name from the OS for the controller/joystick
            name = joystick.get_name()
            textPrint.print(screen, "Joystick name: {}".format(name))

            # Usually axis run in pairs, up/down for one, and left/right for
            # the other.
            axes = joystick.get_numaxes()
            textPrint.print(screen, "Number of axes: {}".format(axes))
            textPrint.indent()

            for i in range(axes):
                axis = joystick.get_axis(i)
                textPrint.print(screen, "Axis {} value: {:>6.3f}".format(i, axis))
                try:
                    self.myControllers[joystickInUse].update(i, axis)
                    # self.myControllers[joystickInUse].printValues()
                except Exception as e:
                    print("error when updating controller")
                    print(e)
            # if self.myControllers[joystickInUse] is not None
            self.myControllers[joystickInUse].updateHorizontals(joystick.get_axis(5), joystick.get_axis(2))

            textPrint.unindent()

            buttons = joystick.get_numbuttons()
            textPrint.print(screen, "Number of buttons: {}".format(buttons))
            textPrint.indent()

            for i in range(buttons):
                button = joystick.get_button(i)
                textPrint.print(screen, "Button {:>2} value: {}".format(i, button))
                self.myControllers[joystickInUse].updateButtons(i, button)
                self.myControllers[joystickInUse].updatePreciseFastButtons(joystick.get_button(1),
                                                                           joystick.get_button(0))
                self.myControllers[joystickInUse].printValues()
            textPrint.unindent()

            # Hat switch. All or nothing for direction, not like joysticks.
            # Value comes back in an array.
            hats = joystick.get_numhats()
            textPrint.print(screen, "Number of hats: {}".format(hats))
            textPrint.indent()

            for i in range(hats):
                hat = joystick.get_hat(i)
                self.myControllers[joystickInUse].stopEngines(hat)
                textPrint.print(screen, "Hat {} value: {}".format(i, str(hat)))
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
    pygame.quit()

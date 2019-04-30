from typing import List, Any

from GpsObjects import *
from threading import *
import time
import logging
import queue
import pygame
import sender
import textprint
import controller

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
        print('Pad Thread has started')

    _running = False

    def run(self):

        logging.info('Starting')
        self._running = True
        for i in range(2):
            self.myControllers.append(controller.Controller(i))

        '''
        Value Matrix scheme:
             | var0 | var1 | var2 | var3
        pad0 | int  | int  | int  | int
        pad1 | int  | int  | int  | int
        pad2 | int  | int  | int  | int
        pad3 | int  | int  | int  | int
        '''

        tempCounter = 0
        pygame.init()
        while self._running:
            messageList = []
            self.padHandler()

            valueMatrix: List[List[int]] = [[], []]

            p: controller.Controller
            # tmpInfo = ''
            for pad in self.myControllers:
                # try:
                # with self.lock:
                valueMatrix[pad.index] = pad.getValueList()
                # tempCounter += self._inc
                # messageList.append(pad.printValues())
                # tmpInfo += pad.printValues()

            self.queue.put(valueMatrix)
            # self.queue.put(messageList)
            # finally:
            #     print(f'Data not forwarded')
        pygame.quit()

    # print('running')

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

            # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
            if event.type == pygame.JOYBUTTONDOWN:
                print("Joystick button pressed.")
            if event.type == pygame.JOYBUTTONUP:
                print("Joystick button released.")

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

                self.myControllers[joystickInUse].update(i, axis)
                # self.myControllers[joystickInUse].printValues()

            textPrint.unindent()

            buttons = joystick.get_numbuttons()
            textPrint.print(screen, "Number of buttons: {}".format(buttons))
            textPrint.indent()

            for i in range(buttons):
                button = joystick.get_button(i)
                textPrint.print(screen, "Button {:>2} value: {}".format(i, button))
                self.myControllers[joystickInUse].updateButton(i, button)
            textPrint.unindent()

            # Hat switch. All or nothing for direction, not like joysticks.
            # Value comes back in an array.
            hats = joystick.get_numhats()
            textPrint.print(screen, "Number of hats: {}".format(hats))
            textPrint.indent()

            for i in range(hats):
                hat = joystick.get_hat(i)
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
    # pygame.quit()

# def PadWorker(index):
#     index = index
#     logging.info('Starting')
#     running = True
#     controller = Controller()
#     myControllers = []
#     for i in range(3):
#         myControllers.append(controller)
#
#     pygame.init()
#     while running:
#         print('working')
#         for i in range(len(myControllers)):
#             print(f'Pad_{i + 1} values: '
#                   f'{myControllers[i].printAxis()}')
#         time.sleep(1)

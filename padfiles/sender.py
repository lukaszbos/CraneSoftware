# Class used to send data from pad.py to AC software
import sys
import pygame


class Sender:

    def __init__(self, joystickNumber, voltage):
        self.joystickNumber = joystickNumber
        self.voltage = voltage

    def setVoltage(self, joystickNumber, voltage):
        self.joystickNumber = joystickNumber
        self.voltage = voltage

    def getVoltage(self, voltage):
        return voltage

    def printCurrentVoltage(self):
       # print("Current voltage is: ")
        #print(self.joystickNumber)
        print(self.voltage)

    def getButtonName(self):
        self.get_name


# sender = Sender(voltage=0)
# pad.sender.printCurrentVoltage()
# pad.sender.setVoltage(0.4)
# pad.sender.printCurrentVoltage()

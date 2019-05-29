"""
I tried to name classes & variable so code would be understandable without comments

*****************************************************************

Class Controller simulates every PS4 pad button used to control a crane.
Make sure that you know pygame library before reading this class: https://www.pygame.org/docs/ref/joystick.html

"""


class Controller:
    # if no button pressed variables are initialized with undermentioned values
    def __init__(self, index):
        self.axisHorizontal = 1.00
        self.axisVertical = 1.00
        self.axisHook = 1.00
        self.homingButton = 0
        self.fastOrPrecise = 0
        self.emergencyStopButton = 0
        self.index = index
        # this list contains actual values of every button
        self.valueList = [self.axisHorizontal, self.axisVertical, self.axisHook, self.homingButton, self.fastOrPrecise,
                          self.emergencyStopButton]

    # updates value of both joysticks (vertical plane only)
    def updateVerticalJoysticks(self, numberOfAxe, voltage):
        if numberOfAxe == 1:
            voltage = self.formatValue(voltage)
            self.axisVertical = voltage
            self.valueList[1] = voltage
        if numberOfAxe == 4:
            voltage = self.formatValue(voltage)
            self.axisHook = voltage
            self.valueList[2] = voltage

    # maps input from pad so it has static length
    @staticmethod
    def formatValue(voltage):
        voltage = voltage + 1
        voltage = "{:.2f}".format(voltage)
        return voltage

    # updates buttons responsible for movement in horizontal plane
    def updateHorizontals(self, valueHorizontalRight, valueHorizontalLeft):
        valueHorizontal = -(valueHorizontalRight - valueHorizontalLeft) / 2
        valueHorizontal = self.formatValue(valueHorizontal)
        self.axisHorizontal = valueHorizontal
        self.valueList[0] = valueHorizontal

    @staticmethod
    def deadzone(voltage):  # calculates deadzones for DualShock4
        zone = 0.1
        if voltage >= zone:
            return int((voltage - zone) / (1 - zone) * 125.01 + 1)  # 1 to 126
        elif voltage <= -zone:
            return int((voltage + zone) / (1 - zone) * 125 - 1)  # -1 to -126
        else:  # we are in deadzone
            return int(0)  # means don't move

    def getValueList(self):  # lock should be added here
        return self.valueList

    def printValues(self):
        return f'Horizontal {self.axisVertical} \nVertical {self.axisHorizontal} \nHook {self.axisHook} \nSprint Button {self.homingButton}'

    def updateButtons(self, buttonNumber, buttonValue):
        homingButtonNumber = 8
        if buttonNumber == homingButtonNumber:
            self.homingButton = buttonValue
            self.valueList[3] = buttonValue

    def updatePreciseFastButtons(self, fastButtonValue, preciseButtonValue):
        # 1 means that button was clicked
        if fastButtonValue == 1:
            self.fastOrPrecise = 1
            self.valueList[4] = 1
        if preciseButtonValue == 1:
            self.fastOrPrecise = 0
            self.valueList[4] = 0

    def stopEngines(self, hat):
        if hat[0] != 0:
            self.emergencyStopButton = hat[0] % 2
            self.valueList[5] = hat[0] % 2
        if hat[1] != 0:
            self.emergencyStopButton = hat[1] % 2
            self.valueList[5] = hat[1] % 2
        else:
            self.emergencyStopButton = hat[0] % 2
            self.valueList[5] = hat[0] % 2

    def getIndex(self):
        return self.index

import struct


class Controller:

    def __init__(self, index):
        self.axisVertical = 0
        self.axisHorizontal = 0
        self.axisHook = 0
        self.button = 0
        #       self.fastSpeedButton = 1.00
        #       self.slowSpeedButton = 1.00
        self.index = index
        self.valueList = [self.axisHorizontal, self.axisVertical, self.axisHook, self.button]

    def update(self, numberOfAxes, voltage):
        voltage = self.deadzone(voltage)
        #voltage = chr(voltage)
        if numberOfAxes == 1:
            self.axisHorizontal = bytes(voltage)
            self.valueList[0] = bytes(voltage)
        if numberOfAxes == 0:
            self.axisVertical = bytes(voltage)
            self.valueList[1] = bytes(voltage)
        if numberOfAxes == 4:
            self.axisHook = bytes(voltage)
            self.valueList[2] = bytes(voltage)

    @staticmethod
    def formatVoltage(voltage):
        voltage = voltage + 1
        voltage = "{:.2f}".format(voltage)
        return voltage

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
        return f'Horizontal {self.axisVertical} \nVertical {self.axisHorizontal} \nHook {self.axisHook} \nSprint Button {self.button}'

    def updateButton(self, buttonClicked, buttonValue):
        sprintButton = 5
        if buttonClicked == sprintButton:
            self.button = bytes(buttonValue)
            self.valueList[3] = bytes(buttonValue)

    def getIndex(self):
        return self.index

class Controller:

    def __init__(self, index):
        self.axisHorizontal = 1.00
        self.axisVertical = 1.00
        self.axisHook = 1.00
        self.button = 1.00
        self.index = index
        self.valueList = [self.axisHorizontal, self.axisVertical, self.axisHook, self.button]

    def update(self, numberOfAxes, voltage):
        if numberOfAxes == 0:
            voltage = voltage * (-1)  # couse direction was wrong
            voltage = self.formatVoltage(voltage)
            self.axisHorizontal = voltage
            self.valueList[0] = voltage
        if numberOfAxes == 1:
            voltage = self.formatVoltage(voltage)
            self.axisVertical = voltage
            self.valueList[1] = voltage
        if numberOfAxes == 4:
            voltage = self.formatVoltage(voltage)
            self.axisHook = voltage
            self.valueList[2] = voltage
    #     if numberOfAxes == 5 or numberOfAxes == 2:
    #         voltageTwo =
    #         voltage = self.formatVoltage(voltage/2)
    #         self.axisHorizontal = voltage
    #         self.valueList[0] = voltage
    #     if numberOfAxes == 2:
    #         voltage = self.formatVoltage(voltage/2)
    #         self.axisHorizontal = voltage
    #         self.valueList[0] = voltage

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
        sprintButton = 8
        if buttonClicked == sprintButton:
            self.button = buttonValue
            self.valueList[3] = buttonValue

    def getIndex(self):
        return self.index

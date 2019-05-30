class Controller:

    def __init__(self, index):
        self.axisVertical = 1.00
        self.axisHorizontal = 1.00
        self.axisHook = 1.00
        self.button = 1.00
        self.index = index
        self.valueList = [self.axisHorizontal, self.axisVertical, self.axisHook, self.button]

    def update(self, numberOfAxes, voltage):
        voltage = self.formatVoltage(voltage)
        if numberOfAxes == 1:
            self.axisHorizontal = voltage
            self.valueList[0] = voltage
        if numberOfAxes == 0:
            self.axisVertical = voltage
            self.valueList[1] = voltage
        if numberOfAxes == 4:
            self.axisHook = voltage
            self.valueList[2] = voltage

    @staticmethod
    def formatVoltage(voltage):
        voltage = voltage + 1
        voltage = "{:.2f}".format(voltage)
        return voltage

    def getValueList(self):  # lock should be added here
        return self.valueList

    def printValues(self):
        return f'Horizontal {self.axisVertical} \nVertical {self.axisHorizontal} \nHook {self.axisHook} \nSprint Button {self.button}'

    def updateButton(self, buttonClicked, buttonValue):
        sprintButton = 5
        if buttonClicked == sprintButton:
            self.button = buttonValue
            self.valueList[3] = buttonValue

    def getIndex(self):
        return self.index

class Controller:

    def __init__(self, index):
        self.axisVertical = 0
        self.axisHorizontal = 0
        self.axisHook = 0
        self.button = 0
        self.index = index
        self.valueList = [self.axisHorizontal, self.axisVertical, self.axisHook, self.button]

    def update(self, numberOfAxes, voltage):
        if numberOfAxes == 1:
            self.axisHorizontal = voltage
            self.valueList[0] = voltage
        if numberOfAxes == 0:
            self.axisVertical = voltage
            self.valueList[1] = voltage
        if numberOfAxes == 4:
            self.axisHook = voltage
            self.valueList[2] = voltage

    def getValueList(self):     #lock should be added here
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

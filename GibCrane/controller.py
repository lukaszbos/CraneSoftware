class Controller:

    def __init__(self, index):
        self.axisVertical = 0
        self.axisHorizontal = 0
        self.axisHook = 0
        self.button = 0
        self.index = index

    def update(self, numberOfAxe, voltage):
        if numberOfAxe == 1:
            self.axisHorizontal = voltage
        if numberOfAxe == 0:
            self.axisVertical = voltage
        if numberOfAxe == 4:
            self.axisHook = voltage

    def printValues(self):
        # print("Horizontal ", self.axisVertical)
        # print("Vertical ", self.axisHorizontal)
        # print("Hook ", self.axisHook)
        # print("Sprint Button ", self.button)
        # print("")
        return f'Horizontal {self.axisVertical} \nVertical {self.axisHorizontal} \nHook {self.axisHook} \nSprint Button {self.button}'

    def updateButton(self, buttonClicked, buttonValue):
        sprintButton = 5
        if buttonClicked == sprintButton:
            self.button = buttonValue

    def getIndex(self):
        return self.index

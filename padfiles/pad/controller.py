class Controller:

    def __init__(self):
        self.axisVertical = 0
        self.axisHorizontal = 0
        self.axisHook = 0
        self.button = 0

    def update(self, numberOfAxe, voltage):
        if numberOfAxe == 1:
            self.axisHorizontal = voltage
        if numberOfAxe == 0:
            self.axisVertical = voltage
        if numberOfAxe == 4:
            self.axisHook = voltage

    def printAxis(self):
        print("Horizontal ", self.axisVertical)
        print("Vertical ", self.axisHorizontal)
        print("Hook ", self.axisHook)
        print("Sprint Button ", self.button)
        print("")

    def updateButton(self, buttonClicked, buttonValue):
        sprintButton = 5
        if buttonClicked == sprintButton:
            self.button = buttonValue

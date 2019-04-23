class AxeMapper:

    def __init__(self, axeNumber=0, plus=0, minus=0):
        self.axeNumber = axeNumber
        self.plus = plus
        self.minus = minus

    def getAxeNumber(self):
        return self.axeNumber

    def getPlus(self):
        return self.plus

    def getMinus(self):
        return self.minus

    def setAxeNumber(self, axeNumber):
        self.axeNumber = axeNumber

    def setPlus(self, plus):
        self.plus = plus

    def setMinus(self, minus):
        self.minus = minus


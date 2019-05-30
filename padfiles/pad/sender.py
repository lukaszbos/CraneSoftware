# Class used to send data from pad.py to AC software


class Sender:
    # directions - zrobic klase z tego i w zaleznosci od pary taki obiekt robic
    # a sender bedzie wysylal te 3 obiekty stworzone w senderze
    # beda 3 rodzaje obiektow zalezne od numeru axa?
    # albo moze wysylac po prostu axy po numerach

    def __init__(self, joystickNumber, voltage, nameOfJoystick):
        self.joystickNumber = joystickNumber
        self.voltage = voltage
        self.nameOfJoystick = nameOfJoystick

    def setVoltage(self, joystickNumber, voltage):
        self.joystickNumber = joystickNumber
        self.voltage = voltage

    def getVoltage(self, voltage):
        return voltage

    def printCurrentVoltage(self):
        print("Current voltage is: ")
        print(self.joystickNumber)
        print(self.voltage)
        print(self.nameOfJoystick)

    # TODO
    # te lefty to nie wiadomo jak
    # zamiast tekstow beda zmienne left right ip
    def mapVoltageToMessages(self, joystickNumber):
        if joystickNumber == 1:
            self.setNameOfJoystick("left-right")
        if joystickNumber == 2:
            self.setNameOfJoystick("forward-backward")
        if joystickNumber == 3:
            self.setNameOfJoystick("up-down")
        if joystickNumber == 4:
            self.setNameOfJoystick("error 4th joisticks called")

    def numberEquals(self, joystickNumber):
        return self.joystickNumber == joystickNumber

    def setNameOfJoystick(self, nameOfJoistick):
        self.nameOfJoystick = nameOfJoistick

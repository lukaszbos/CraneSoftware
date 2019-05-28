from math import *

'''
    GpsObjects.py:  File containing classes later used for coordinates calculation
    Python version: python3.7
    
    Authors: Mateusz Jaszek
'''

PI = pi


class Crane:
    def __init__(self, x, y, index):
        # def __init__(self, **kwargs):
        self._x = x
        self._y = y
        self._index = index

    def SetX(self, x):
        self._x = x

    def GetX(self):
        return self._x

    def SetY(self, y):
        self._y = y

    def GetY(self):
        return self._y

    def SetIndex(self, index):
        self._index = index

    def GetIndex(self):
        return self._index


class Hook(Crane):
    pass

    def __init__(self, z, r, theta):
        super().__init__(0, 0, 0)
        self._z = z
        self._r = r
        self._theta = theta

    def SetR(self, r):
        self._r = r

    def SetTheta(self, theta):
        self._theta = theta

    def GetZ(self):
        return self._z

    def GetR(self):
        return self._r

    def GetTheta(self):
        return self._theta

    # def passRadials(self, z, r, theta):
    def convertRadial(self, Crane):
        # print(Crane.GetX(), Crane.GetY())

        self._x = Crane.GetX() + self._r * cos(self._theta)
        self._y = Crane.GetY() + self._r * sin(self._theta)


class table:
    def __init__(self):
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 200
        self.x3 = 200
        self.y3 = 0
        self.x4 = 200
        self.y4 = 200

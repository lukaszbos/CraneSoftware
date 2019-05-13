from math import *
# import pygeodesy
# import geographiclib as geographiclib
# import scipy

# from geographiclib.geodesic import Geodesic

PI = pi


class Crane:
    def __init__(self, x, y, index):
    # def __init__(self, **kwargs):
        self._x = x
        self._y = y
        self._index = index

        # for x, y, index in kwargs.items():
        #     try:
        #         self._x = x
        #     except:
        #         print('missing x, setting as 0')
        #         self._x = 0
        #     try:
        #         self._y = y
        #     except:
        #         print('missing y, setting as 0')
        #         self._y = 0
        #     try:
        #         self._index = index
        #     except:
        #         print('missing index, setting as 0')
        #         self._index = 0
    # def __init__(self, x, y, index):
    #     self._x = x
    #     self._index = index

    #     self._y = y
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


# class Crane(point):
#     def __init__(self):
#         super().__init__()


class Hook(Crane):
    pass

    def __init__(self, z, r, theta):
        super().__init__(0, 0, 0)
        self._z = z
        self._r = r
        self._theta = theta

    # def __init__(self, **kwargs):
    #     super().__init__(x=0, y=0, index=0)
    #     for z, r, theta in kwargs.items():
    #         try:
    #             self._z = z
    #         except:
    #             print('missing z, setting as 50')
    #             self._z = 50
    #         try:
    #             self._r = r
    #         except:
    #             print('missing r, setting as 50')
    #             self._r = 50
    #         try:
    #             self._theta = theta
    #         except:
    #             print('missing theta, setting as 0')
    #             self._theta = 0

    def SetZ(self, z):
        self._z = z

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

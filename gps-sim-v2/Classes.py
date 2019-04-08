from math import cos, sin, pi

PI = pi

class point:
    def __init__(self, x=0, y=0, index=0):
        self._x = x
        self._y = y
        self._index = index

    def setX(self, x):
        self._x = x
    def setY(self, y):
        self._y = y
    def setIndex(self, index):
        self._index = index
    def getX(self):
        return self._x
    def getY(self):
        return self._y
    def getIndex(self):
        return self._index

class crane(point):
    def __init__(self):
        super().__init__()


class hook(point):
    pass

    def __init__(self, z=0, r=0, theta=0):
        super().__init__()
        self._z = z
        self._r = r
        self._theta = theta
    def setZ(self, z):
        self._z = z
    def setR(self, r):
        self._r = r
    def setTheta(self,theta):
        self._theta = theta
    def getZ(self):
        return self._z
    def getR(self):
        return self._r
    def getTheta(self):
        return self._theta
    # def passRadials(self, z, r, theta):
    def convertRadial(self, crane):
        print(crane.getX(), crane.getY())

        self._x = crane.getX() + self._r * cos(self._theta)
        self._y = crane.getY() + self._r * sin(self._theta)

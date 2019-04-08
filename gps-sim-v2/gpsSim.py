# print('hello world')

class point:
    def __init__(self, x=0, y=0, index = 0):
        self._x = x
        self._y = y
        self._index = index
    def setX(self, x):
        self._x = x

class crane(point):
    def __init__(self):
        super().__init__()




testPoint = crane()

print(testPoint._x, testPoint._y, testPoint._index)



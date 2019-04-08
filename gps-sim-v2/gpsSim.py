# print('hello world')

import Classes


testCrane = Classes.crane()
testHook = Classes.hook()

testCrane.setIndex(1)
testCrane.setX(10)
testCrane.setY(10)

testHook.setZ(90)
testHook.setR(50)
testHook.setTheta(Classes.PI/6)

testHook.convertRadial(testCrane)

print(testHook.getX(),testHook.getY(),testHook.getZ())

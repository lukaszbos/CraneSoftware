# print('hello world')
# from

# TODO: import geographicLib somehow and learn how to use this shit.
# TODO: then try to get ethernet on python working.



import Classes



testCrane = Classes.crane()
testHook = Classes.hook()

testCrane.setIndex(1)
testCrane.setX(10)
testCrane.setY(10)

testHook.setZ(90)
testHook.setR(50)
testHook.setTheta(Classes.PI/8)

testHook.convertRadial(testCrane)

print(testHook.getX(),testHook.getY(),testHook.getZ())

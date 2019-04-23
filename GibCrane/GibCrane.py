import pygame

from GpsObjects import *
from threading import *
from controller import Controller
import time
import logging
import queue

'''
    File name: GibCrane.py
    Author: Mateusz Jaszek
    mail: matijasz8@gmai.com
    python version: 3.6
    
    This is main Crane control file. It's main task is operation,
    and synchronization of all threads 
    
'''

# TODO Necessary integration of pad control program with threads


logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(asctime)s %(threadName)-10s %(message)s',
                    datefmt='%m/%d/%Y  %I:%M:%S %p')

"""     logger below will write logs out to file

logging.basicConfig(level=logging.INFO, filename='threadLogs.log',
                    format='%(levelname)s: %(asctime)s %(threadName)-10s %(message)s',
                    datefmt='%m/%d/%Y  %I:%M:%S %p')
"""


class CraneClient(Thread):
    def __init__(self, name, crane: Crane, hook: Hook, inc, delay, cond: Condition):
        Thread.__init__(self, name=f'{name}_{crane.GetIndex()}')
        self._crane = crane
        self._hook = hook
        self._hook.SetIndex(self._crane.GetIndex())
        self._inc = inc
        self._delay = delay
        self.index = crane.GetIndex()
        self._condition = cond

        # self.lock = Lock()
        # lockList.append(self.lock)
        # self.q = queue.LifoQueue()
        # queueList.append(self.q)

    tempCounter = 0
    _running = False

    def infoString(self, rot_count):
        return f"Hook_{self._crane.GetIndex()} coordinates are: " \
            f"X={self._hook.GetX()} " \
            f"Y={self._hook.GetY()} " \
            f"Z={self._hook.GetZ()} current rotation: {rot_count} degrees"

    def run(self) -> None:
        logging.info('Starting')
        _running = True
        while _running:
            self._hook.convertRadial(self._crane)
            self._hook.SetTheta(self._hook.GetTheta() + self._inc)

            with lockList[self.index - 1]:
                # if queueList[self.index -1].full():
                #     queueList[self.index -1].clear()
                self.tempCounter += self._inc
                queueList[self.index - 1].put(self.infoString(self.tempCounter))

                # print(f'{time.time()} {self.infoString()}')

                """  Console notifications
                # print(f'{time.time()} Hook_{self._crane.GetIndex()} '
                #       f'coordinates are: X={self._hook.GetX()} '
                #       f'Y={self._hook.GetY()} '
                #       f'Z={self._hook.GetZ()} ')
                """

                # TODO make conditions work better, or, basically work at all
                # self._condition.notifyAll()

                time.sleep(self._delay)

        logging.info('ending')

    # def getQ(self):
    #     with self.lock:
    #         return self.q

    @staticmethod
    def killThread():
        _running = False


def AcWorker(clients, condition: Condition):
    logging.info('Starting')
    running = True
    infoString = ''
    while running:
        for client in clients:
            # with condition:
            #     condition.wait(0.1)
            #     print(queueList[client.index - 1].get())

            with lockList[client.index - 1]:
                print(queueList[client.index - 1].get())
                queueList[client.index - 1].task_done()

        time.sleep(1)


def PadWorker():
    logging.info('Starting')
    running = True
    controller = Controller()
    myControllers = []
    for i in range(3):
        myControllers.append(controller)

    pygame.init()
    while running:
        print('working')
        for i in range(len(myControllers)):
            print(f'Pad_{i + 1} values: '
                  f'{myControllers[i].printAxis()}')
        time.sleep(1)




clientList = []
lockList = []
queueList = []

c = Condition(Lock())

testLock_1 = Lock()
testLock_2 = Lock()
lockList.append(testLock_1)
lockList.append(testLock_2)

testQueue_1 = queue.LifoQueue()
testQueue_2 = queue.LifoQueue()
queueList.append(testQueue_1)
queueList.append(testQueue_2)

if __name__ == "__main__":
    with open('threadLogs.log', 'w'):
        pass

    crane1 = CraneClient('Crane', Crane(x=20, y=20, index=1),
                         Hook(z=100, r=40, theta=0), inc=2 * PI / 360, delay=0.1, cond=c)

    crane2 = CraneClient('Crane', Crane(x=180, y=180, index=2),
                         Hook(z=150, r=80, theta=0), inc=-2 * PI / 360, delay=0.1, cond=c)

    clientList.append(crane1)
    clientList.append(crane2)

    crane1.start()
    crane2.start()

    # PadThread = Thread(target=PadWorker(), name='PadThread',)
    # PadThread.start()

    AcThread = Thread(target=AcWorker, name='AcThread', args=(clientList, c,))
    AcThread.start()

    # var = input()
    #
    # if var == 'kill':
    #     for x in clientList:
    #         x.killThread()

    # AcThread.

    # testTable = GpsObjects.table()
    # testCrane = GpsObjects.Crane()
    # testHook = GpsObjects.Hook()

    # testCrane.setIndex(1)
    # testCrane.setX(30)
    # testCrane.setY(30)

    # testHook.setZ(90)
    # testHook.setR(50)
    # testHook.setTheta(GpsObjects.PI / 8)

    # testHook.convertRadial(testCrane)

    # print(testHook.getX(), testHook.getY(), testHook.getZ())

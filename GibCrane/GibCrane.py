import pygame

import socket

from pip._vendor.distlib.compat import raw_input

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

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(asctime)s %(threadName)-10s %(message)s',
                    datefmt='%I:%M:%S %p')

"""     logger below will write logs out to file

logging.basicConfig(level=logging.INFO, filename='threadLogs.log',
                    format='%(levelname)s: %(asctime)s %(threadName)-10s %(message)s',
                    datefmt='%m/%d/%Y  %I:%M:%S %p')
"""


class CraneClient(Thread):
    def __init__(self, name, crane: Crane, hook: Hook, inc, delay, cond: Condition, ip, port):
        Thread.__init__(self, name=f'{name}_{crane.GetIndex()}')
        self._crane = crane
        self._hook = hook
        self._hook.SetIndex(self._crane.GetIndex())
        self._inc = inc
        self._delay = delay
        self.index = crane.GetIndex()
        self._condition = cond
        self._ip = ip
        self._port = port
        print("new crane connected")

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

    def run(self):
        _running = True
        logging.info('Starting')

        while _running:

            data = connection.recv(64)
            print(f'Server recived data:{data}')
            MESSAGE = raw_input("Enter response:")
            if MESSAGE == 'exit':
                break
            connection.send(MESSAGE)

            self._hook.convertRadial(self._crane)
            self._hook.SetTheta(self._hook.GetTheta() + self._inc)

            with lockList[self.index - 1]:
                # if queueList[self.index -1].full():
                #     queueList[self.index -1].clear()
                self.tempCounter += self._inc
                queueList[self.index - 1].put(self.infoString(self.tempCounter))

                # print(f'{time.time()} {self.infoString()}')

                """  Console notifications  """
                # print(f'{time.time()} Hook_{self._crane.GetIndex()} '
                #       f'coordinates are: X={self._hook.GetX()} '
                #       f'Y={self._hook.GetY()} '
                #       f'Z={self._hook.GetZ()} ')

                # TODO make conditions work better, or, thb,  work at all
                # self._condition.notifyAll()

                time.sleep(self._delay)

        logging.info('ending')

    # def getQ(self):
    #     with self.lock:
    #         return self.q

    @staticmethod
    def killThread():
        _running = False


class PadClient(Thread):
    def __init__(self, name, index, lock, queue):
        Thread.__init__(self, name=f'{name}_{index}')
        self._lock = lock
        self._queue = queue
        self._index = index

    _running = False

    def run(self):
        logging.info('Starting')
        self._running = True
        while self._running:
            logging.debug('Working')


def PadWorker(index):
    index = index
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


def AcWorker(clients, condition: Condition):
    logging.info(' Starting')
    running = True
    while running:
        for client in clients:
            # with condition:
            #     condition.wait(0.1)
            #     print(queueList[client.index - 1].get())

            with lockList[client.index - 1]:
                print(queueList[client.index - 1].get())
                queueList[client.index - 1].task_done()
        time.sleep(1 / 5)


# TODO fix client list, acThread sould check whether client is crane od pad

clientList = []
lockList = []
queueList = []

c = Condition(Lock())

craneLock_1 = Lock()
craneLock_2 = Lock()
padLock = Lock()
lockList.append(craneLock_1)
lockList.append(craneLock_2)
lockList.append(padLock)

craneQueue_1 = queue.LifoQueue()
craneQueue_2 = queue.LifoQueue()
padQueue = queue.LifoQueue()
queueList.append(craneQueue_1)
queueList.append(craneQueue_2)
queueList.append(padQueue)

if __name__ == "__main__":
    with open('threadLogs.log', 'w'):
        pass

    # server_address = ('localhost', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 10000
    sock.bind(('', port))

    while True:
        sock.listen(1)
        print('Server is waiting')
        (connection, (ip, port)) = sock.accept()
        try:
            print('client connected')
            crane1 = CraneClient('Crane', Crane(x=20, y=20, index=1),
                                 Hook(z=100, r=40, theta=0),
                                 inc=2 * PI / 360, delay=0.1, cond=c, ip=ip, port=port)
            crane1.start()
            clientList.append(crane1)
        except:
            print("something went horribly wrong")

'''
    # crane2 = CraneClient('Crane', Crane(x=180, y=180, index=2),
    #                      Hook(z=150, r=80, theta=0), inc=-2 * PI / 360, delay=1 / 50, cond=c)


    clientList.append(crane2)

    # crane1.start()
    # crane2.start()

    PadThread = Thread(target=PadWorker, name='PadThread', args=(3,))
    # clientList.append(PadThread)

    # PadThread.start()
    for t in clientList:
        t.start()

    AcThread = Thread(target=AcWorker, name='AcThread', args=(clientList, c,))
    # AcThread.start()
'''
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

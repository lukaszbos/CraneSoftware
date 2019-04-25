from GpsObjects import *
from threading import *
from controller import Controller
import time
import logging
import queue


class CraneClient(Thread):
    def __init__(self, name, crane: Crane, hook: Hook, inc, delay, cond: Condition, ip, port, queue, lock):
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
        self.queue = queue
        self.lock = lock
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
            ''' connection handling
            try:
                data = connection.recv(1024)
                print(f'Server recived data: {data}')
                # MESSAGE = raw_input("Enter response:")
                # if MESSAGE == 'exit':
                #     break
                # connection.send(MESSAGE)
            except:
                print("connection lost")
                self.killThread()
                break
            '''
            self._hook.convertRadial(self._crane)
            self._hook.SetTheta(self._hook.GetTheta() + self._inc)

            with self.lock:
                # if queueList[self.index -1].full():
                #     queueList[self.index -1].clear()
                self.tempCounter += self._inc
                self.queue.put(self.infoString(self.tempCounter))
                # queueList[self.index - 1]
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

    def isrunning(self):
        return self._running

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

from GpsObjects import *
from threading import *
import time
import logging
import queue

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(asctime)s %(threadName)-10s %(message)s',
                    datefmt='%m/%d/%Y  %I:%M:%S %p')


# logger below will write logs out to file

# logging.basicConfig(level=logging.INFO, filename='threadLogs.log',
#                     format='%(levelname)s: %(asctime)s %(threadName)-10s %(message)s',
#                     datefmt='%m/%d/%Y  %I:%M:%S %p')


class CraneClient(Thread):
    def __init__(self, name, crane: Crane, hook: Hook, inc, delay):
        Thread.__init__(self, name=f'{name}_{crane.GetIndex()}')
        self._crane = crane
        self._hook = hook
        self._hook.SetIndex(self._crane.GetIndex())
        self._inc = inc
        self._delay = delay
        self.index = crane.GetIndex()
        # self.lock = Lock()
        # lockList.append(self.lock)
        # self.q = queue.LifoQueue()
        # queueList.append(self.q)

    _running = False

    def infoString(self):
        return f'Hook_{self._crane.GetIndex()} coordinates are: ' \
            f'X={self._hook.GetX()} ' \
            f'Y={self._hook.GetY()} ' \
            f'Z={self._hook.GetZ()} '

    def run(self) -> None:
        logging.info('Starting')
        _running = True
        while _running:
            self._hook.convertRadial(self._crane)
            self._hook.SetTheta(self._hook.GetTheta() + self._inc)

            with lockList[self.index-1]:
                queueList[self.index-1].put(self.infoString())

            print(f'{time.time()} Hook_{self._crane.GetIndex()} '
                  f'coordinates are: X={self._hook.GetX()} '
                  f'Y={self._hook.GetY()} '
                  f'Z={self._hook.GetZ()} ')
            time.sleep(self._delay)

        logging.info('ending')
    # def getQ(self):
    #     with self.lock:
    #         return self.q


    @staticmethod
    def killThread():
        _running = False


def AcWorker(clients):

    logging.info('Starting')
    running =True
    infoString = ''
    while running:
        for client in clients:
            with lockList[client.index-1]:
                print(queueList[client.index-1].get())



clientList = []
lockList = []
queueList = []



testLock_1 = Lock()
testLock_2 = Lock()
lockList.append(testLock_1)
lockList.append(testLock_2)

testQueue_1 = queue.LifoQueue()
testQueue_2 = queue.LifoQueue()
queueList.append(testQueue_1)
queueList.append(testQueue_2)
#
# queueList[0].put
#
# def fill_queue(qL, i, hook):
#     qL[i-1].put(hook)
#     return qL

# class AcClient(Thread):
#     def __init__(self):
#         Thread.__init__(self)
#     runnig = True
#     def run(self):
#         for i in range()

if __name__ == "__main__":
    with open('threadLogs.log', 'w'):
        pass

    crane1 = CraneClient('Crane', Crane(x=20, y=20, index=1),
                         Hook(z=100, r=40, theta=0), 2 * PI / 360, 1)

    crane2 = CraneClient('Crane', Crane(x=180, y=180, index=2),
                         Hook(z=150, r=80, theta=0), -2 * PI / 360, 2)

    clientList.append(crane1)
    clientList.append(crane2)

    crane1.start()
    crane2.start()

    AcThread = Thread(target=AcWorker, name='AcThread', args=(clientList,))
    AcThread.start()
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

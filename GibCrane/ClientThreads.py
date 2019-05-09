from GpsObjects import *
from threading import *
from Controller import Controller
import time
import logging
import queue
import socket

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(asctime)s %(threadName)-10s %(message)s',
                    datefmt='%m/%d/%Y  %I:%M:%S %p')


class CraneClient(Thread):

    def __init__(self, name, crane: Crane, hook: Hook, inc, delay, cond: Condition, Queue, lock, connection):
        Thread.__init__(self, name=f'{name}_{crane.GetIndex() + 1}')
        self._crane = crane
        self._hook = hook
        self._hook.SetIndex(self._crane.GetIndex())
        self._inc = inc
        self._delay = delay
        self.index = crane.GetIndex()
        self._condition = cond
        self.queue = Queue
        self.lock = lock
        self.name = f'{name}_{crane.GetIndex() + 1}'
        self.conn = connection

        print("new crane connected")

        # self.lock = Lock()
        # lockList.append(self.lock)
        # self.q = queue.LifoQueue()
        # queueList.append(self.q)

    tempCounter = 0
    _running = False
    outputLock = Lock()
    outputMessage = []

    def setOutput(self, msg):
        with self.outputLock:
            self.outputMessage = msg

    def getOutput(self):
        with self.outputLock:
            return self.outputMessage

    def getFullOutput(self):
        message = ''
        for i in self.outputMessage:
            print(i)
            if len(self.outputMessage) != 0:
                message += f"{i} "
        return message

    # def to_bit(self):

    def infoString(self, rot_count):
        return f"Hook_{self._crane.GetIndex()} coordinates are: " \
            f"X={self._hook.GetX()} " \
            f"Y={self._hook.GetY()} " \
            f"Z={self._hook.GetZ()} current rotation: {rot_count} degrees"

    def run(self, iteratorek=0):
        logging.info('Starting')
        while True:
            messageList = []
            ''' connection handling '''
            try:
                data = self.conn.recv(1024)
                print(f'{self.name} recived data: {data}')
                # print(f"is server runing? {_running}")
                # MESSAGE = input("Enter response:")
            except:
                print(f"{self.name} data not recieved")
                # self.killThread()
                break
            try:
                stringMESSAGE = self.getFullOutput()
                print(f'info z pada to {self.getFullOutput()}')
                byte_message = bytes(stringMESSAGE, 'utf-8')
                MESSAGE = b'chuj ci w dupe'
                print(f'{type(byte_message)}    {type(MESSAGE)}')
                print(f'jebane gunwo {MESSAGE}')
                # for i in range(5):
                if iteratorek < 1:  # TODO Zrobic locki zeby tego nie trzeba bylo wysylac
                    self.conn.send(MESSAGE)
                    iteratorek = iteratorek + 1

                else:
                    self.conn.send(byte_message)

                # if MESSAGE == 'exit':
                #     break
            except Exception:
                print(f"{self.name}data not sent")
                # self.killThread()
                break

            self._hook.convertRadial(self._crane)
            self._hook.SetTheta(self._hook.GetTheta() + self._inc)

            # try:
            with self.lock:
                # if queueList[self.index -1].full():
                #     queueList[self.index -1].clear()
                self.tempCounter += self._inc
                messageList.append(self.infoString(self.tempCounter))
                self.queue.put(messageList)

            print(f'\n{self.name}\n{self.getFullOutput()}')

            # print

            # finally:
            #     print(f'Data not forwarded')

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

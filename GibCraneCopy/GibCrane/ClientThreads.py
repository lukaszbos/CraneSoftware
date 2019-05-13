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

'''
    Ta Klasa, jest uruchamiana jako wątek łączący się z arduino. musi być w oddzielnym wątku bo dla 4 dzwigów będzie 
    troche obliczeń do zrobienia w tym samym czasie.
'''


class CraneClient(Thread):

    def __init__(self, name, crane: Crane, hook: Hook, inc, delay, cond: Condition, Queue, lock):
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
        self.ip = None
        print("new crane connected")



    tempCounter = 0
    _running = False
    outputLock = Lock()
    outputMessage = []

    def CompareIP(self, craneIP):

        if self.ip == None:
            self.ip = craneIP
            return True
        elif craneIP == self.ip:
            return True
        else:
            return False

    def setOutput(self, msg):
        with self.outputLock:
            self.outputMessage = msg


    '''
        Metoda sklejająca tablicę danych otrzymaną z padów, do jednego stringa
    '''
    def getFullOutput(self):
        message = ''
        testMessage = self.name
        with self.outputLock:
            # return self.outputMessage
            for i in self.outputMessage:
                # print(i)
                if len(self.outputMessage) != 0:
                    message += f"{i} "
                # print(message)
            return bytes(message, 'utf-8')

    # def to_bit(self):

    def infoString(self, rot_count):
        return f"Hook_{self._crane.GetIndex()} coordinates are: " \
            f"X={self._hook.GetX()} " \
            f"Y={self._hook.GetY()} " \
            f"Z={self._hook.GetZ()} current rotation: {rot_count} degrees"

    def run(self):
        iteratorek = 0  #nie wiem po chuj to Łukasz cos wymyslił
        cnt = 0         #licznik danhych wyslanych do ARD
        logging.info('Starting')
        while True:
            messageList = []

            self._hook.convertRadial(self._crane)
            self._hook.SetTheta(self._hook.GetTheta() + self._inc)

            # try:
            with self.lock:
                # if queueList[self.index -1].full():
                #     queueList[self.index -1].clear()
                self.tempCounter += self._inc
                messageList.append(self.infoString(self.tempCounter))
                self.queue.put(messageList)

            # print(f'\n{self.name}\n{self.getFullOutput()}')

            # TODO make conditions work better, or, thb,  work at all
            # self._condition.notifyAll()

            time.sleep(self._delay)

    logging.info('ending')

    # def getQ(self):
    #     with self.lock:
    #         return self.q

import logging
import struct
import time
from threading import *

from GpsObjects import *

'''
    CraneClient.py: Crane client thread object is defined here. It handles all calculations 
    that happen after getting data from cranes.
    
    Authors: Mateusz Jaszek  
'''

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(asctime)s %(threadName)-10s %(message)s',
                    datefmt='%m/%d/%Y  %I:%M:%S %p',
                    handlers=[logging.FileHandler('threadLogs.log'), logging.StreamHandler()])


class CraneClient(Thread):

    def __init__(self, name, crane: Crane, hook: Hook, inc, delay, Queue, lock, ip):
        Thread.__init__(self, name=f'{name}_{crane.GetIndex()}')
        self._crane = crane
        self._hook = hook
        self._hook.SetIndex(self._crane.GetIndex())
        self._inc = inc
        self._delay = delay
        self.index = crane.GetIndex()
        self.queue = Queue
        self.lock = lock
        self.name = f'{name}_{crane.GetIndex()}'
        self.ip = None
        self.outputMessage = []
        self.ip = ip
        logging.info(f'{self.getName()} has been created')

    tempCounter = 0
    _running = False
    outputLock = Lock()

    def run(self):      # Main thread method, responsible for coordinate calculations 
        logging.info('Starting')
        while True:
            messageList = []

            self._hook.convertRadial(self._crane)
            self._hook.SetTheta(self._hook.GetTheta() + self._inc)

            # try:
            with self.lock:
                self.tempCounter += self._inc
                messageList.append(self.infoString(self.tempCounter))
                self.queue.put(messageList)

            time.sleep(self._delay)

    def setMessage(self, message):
        self.outputMessage = message

    def getMessage(self):
        return self.outputMessage

    def CompareIP(self, craneIP):    # Checks if ip of last received message is same as this client's
        if craneIP == self.ip:
            return True
        else:
            return False

    def setOutput(self, msg):
        with self.outputLock:
            self.setMessage(msg)

    #   returns data package in byte format. later it is being sent to correct crane
    def getFullOutput(self):
        message = 's '      # Starting character of package
        with self.outputLock:
            for i in self.outputMessage:
                if len(self.outputMessage) != 0:
                    message += f"{i} "
            message += 'e '     # ending character of package
            return bytes(message, 'utf-8')

    def getPackage(self):
        print(self.getMessage())
        try:
            print(self.outputMessage)
            return bytes(struct.pack('>bbbb',
                                     self.outputMessage[0],
                                     self.outputMessage[1],
                                     self.outputMessage[2],
                                     self.outputMessage[3]))
        except Exception as exception:
            print(f'{type(self.outputMessage[1])} Exception happened while converting to package:  {exception}')
            return None

    def infoString(self, rot_count):
        return f"Hook_{self._crane.GetIndex()} coordinates are: " \
            f"X={self._hook.GetX()} " \
            f"Y={self._hook.GetY()} " \
            f"Z={self._hook.GetZ()} current rotation: {rot_count} degrees"

from builtins import print
import socket
from queue import LifoQueue
from typing import Any

from ClientThreads import *
from PadThread import *

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

clientList = []

# TODO fix client list, acThread sould check whether client is crane od pad

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


# TODO get a hang of types

def AcWorker(clients, condition: Condition):
    logging.info(' Starting')
    running = True
    while running:
        inputList = []
        pad_commands = [[], []]
        receivedMessage = []
        for cl in clients:
            # with condition:
            #     condition.wait(0.1)
            #     print(queueList[client.index - 1].get())
            if isinstance(cl, PadClient):
                with lockList[cl.index]:
                    pad_commands = queueList[cl.index].get()
                    # for m in receivedMessage:
                    #     inputList.append(m)
                # print("pad")
            elif isinstance(cl, CraneClient):
                with lockList[cl.index]:
                    receivedMessage = queueList[cl.index].get()
                    # for m in receivedMessage:
                    #     inputList.append(m)
                # print('crane')
                # print(queueList[cl].get())
                # queueList[cl].task_done()
        print(len(inputList))
        # for input in inputList:
        #     print(input)

        # inputList.reverse()

        for i in range(len(pad_commands)):
            clientList[i].setOutput(pad_commands[i])

        time.sleep(1 / 10)


if __name__ == "__main__":
    with open('threadLogs.log', 'w'):
        pass

    # server_address = ('localhost', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 8888
    sock.bind(('', port))
    print(socket.gethostname())
    i = 0

    # tmpIP = "nah"
    tmpip = 'nah'
    tmpPort = 'nah'
    crane1 = CraneClient('Crane', Crane(x=20, y=20, index=0),
                         Hook(z=100, r=40, theta=0),
                         inc=2 * PI / 360, delay=0.1, cond=c, ip=tmpip, port=tmpPort,
                         queue=queueList[0], lock=lockList[0])

    crane2 = CraneClient('Crane', Crane(x=180, y=180, index=1),
                         Hook(z=150, r=80, theta=0),
                         inc=-2 * PI / 360, delay=1 / 50, cond=c, ip=tmpip, port=tmpPort,
                         queue=queueList[1], lock=lockList[1])

    clientList.append(crane1)
    clientList.append(crane2)
    # crane1.start()
    # crane2.start()

    # PadThread = Thread(target=PadWorker, name='PadThread', args=(3,))
    # clientList.append(PadThread)
    PadThread = PadClient(name='PadThread', index=2, queue=queueList[2], lock=lockList[2])
    clientList.append(PadThread)
    # PadThread.start()

    AcThread = Thread(target=AcWorker, name='AcThread', args=(clientList, c,))
    # clientList.append(AcThread)

    for t in clientList:
        t.start()

    AcThread.start()

    '''
        while True:
            for client in clientList:
                if client.isrunning():
                    pass
                else:
                    clientList.remove(client)

            sock.listen(1)

            print('Server is waiting')
            (connection, (ip, port)) = sock.accept()
            try:
                print('client connected')
                crane1 = CraneClient('Crane', Crane(x=20, y=20, index=i),
                                     Hook(z=100, r=40, theta=0),
                                     inc=2 * PI / 360, delay=0.1, cond=c, ip=ip, port=port)
                crane1.isDaemon()
                crane1.start()
                clientList.append(crane1)
                i += 1
            except:
                print("something went horribly wrong")
        '''

    # t.join()
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

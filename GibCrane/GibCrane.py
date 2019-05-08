from builtins import print

from ClientThreads import *
from PadClient import *

# from socket import socket

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

listOfThreads = []
listOfLocks = []
listOfQueues = []

testCondition = Condition(Lock())


# craneLock_1 = Lock()
# craneLock_2 = Lock()
# padLock = Lock()
# listOfLocks.append(craneLock_1)
# listOfLocks.append(craneLock_2)
# listOfLocks.append(padLock)
#
# craneQueue_1 = queue.LifoQueue()
# craneQueue_2 = queue.LifoQueue()
# padQueue = queue.LifoQueue()
# listOfQueues.append(craneQueue_1)
# listOfQueues.append(craneQueue_2)
# listOfQueues.append(padQueue)

def startWorkingYouFucker(fuckingShit):
    logging.info(' Starting')
    print(fuckingShit)
    while True:

        for i in range(len(fuckingShit)):
            logging.info(f'{fuckingShit[i].name} is alive')

        time.sleep(1.5)

# TODO: ogarnać czy przypadkiem sie nie jebią indeksy bo to wygląda podejrzanie. czasami sie gówno wyswietla na ardu a czasasmi ni hcuja 

def communicateThreads(threads, condition: Condition):
    delay = 1 / 10
    logging.info(' Starting')
    while True:
        inputList = []
        pad_commands = [[], []]
        receivedMessage = []
        for thread in threads:
            # with condition:
            #     condition.wait(0.1)
            #     print(queueList[client.index - 1].get())
            print("type threada")
            # print(type(thread))
            if isinstance(thread, PadClient):
                print("wchodzi to pierwsego ifa ")
                with getLock(thread, threads):
                    # print(threads.index(thread))
                    pad_commands = listOfQueues[threads.index(thread)].get()
                    # print("pad commands: ")
                    # print(pad_commands)
                    # for m in receivedMessage:
                    #     inputList.append(m)
                # print("pad")
            elif isinstance(thread, CraneClient):
                #  with getLock(thread, threads):
                print("wchodzi do ifa craneclient")
                try:
                    print(listOfQueues[threads.index(thread) - 1].qsize())
                    # receivedMessage = listOfQueues[threads.index(thread) - 1].get()  #TODO TUTAJ BLAD
                    # print(receivedMessage)
                except Exception:
                    print(Exception)

                # for m in receivedMessage:
                #     inputList.append(m)
            # print('crane')
            # print(queueList[thread].get())
            # queueList[thread].task_done()
        # print(len(inputList))
        # for input in inputList:

        for thread in listOfThreads:
            ii = 0
            # print("i chuj")
            if isinstance(thread, CraneClient):
                # while thread.isAlive():
                # print("i chujeeeee")
                current_command = pad_commands[ii]
                print(current_command)
                # try:
                thread.setOutput(current_command)
                print("pad commands: ")
                print(current_command)
                ii += 1
        # except IOError:
        #   print(IOError)
        #  print("Exeption in loop in commands")
        else:
            print("notting happened")

    # for command in pad_commands:
    #     if isinstance(getThreadByIndex(command, pad_commands), CraneClient):
    #         print("im in if gibcrane")
    #         print(command)
    #         try:
    #             getThreadByIndex(command, pad_commands).setOutput(command)
    #             print("pad commands: ")
    #             print(pad_commands)
    #         except IOError:
    #             print(IOError)
    #             print("Exeption in loop in commands")
    #     else:
    #         print("notting happened")

    time.sleep(delay)


def getThreadByIndex(command, pad_commands):
    return listOfThreads[pad_commands.index(command) - 1]


def getLock(thread, threads):
    return listOfLocks[threads.index(thread) - 1]


def createCraneThread():
    iterator = len(listOfThreads) - 1
    print('client connected')
    tempQueue = queue.LifoQueue()
    tempLock = Lock()
    listOfQueues.append(tempQueue)
    listOfLocks.append(tempLock)
    # crane_index = list
    crane = CraneClient('Crane', Crane(x=20, y=20, index=iterator),
                        Hook(z=100, r=40, theta=0),
                        inc=2 * PI / 360, delay=0.1, cond=testCondition, ip=ip, port=port,
                        queue=listOfQueues[iterator], lock=listOfLocks[iterator], connection=connection)
    crane.isDaemon()
    listOfThreads.append(crane)
    crane.start()


def serverInit():
    global sock, port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 10000
    sock.bind(('', port))
    print(socket.gethostname())
    # tmpIP = "nah"


if __name__ == "__main__":
    with open('threadLogs.log', 'w'):
        pass

    ''' Socket listening for connection is created here'''

    # server_address = ('localhost', 10000)
    serverInit()
    '''
    tmpip = 'nah'
    tmpPort = 'nah'
    
    crane1 = CraneClient('Crane', Crane(x=20, y=20, index=0),
                         Hook(z=100, r=40, theta=0),
                         inc=2 * PI / 360, delay=0.1, cond=c, ip=tmpip, port=tmpPort,
                         queue=queueList[0], lock=lockList[0])

    crane2 = CraneClient('Crane', Crane(x=180, y=180, index=1),
                         Hook(z=150, r=80, theta=0),
                         inc=-2 * PI / 360, delay=1 / 10, cond=c, ip=tmpip, port=tmpPort,
                         queue=queueList[1], lock=lockList[1])
    
    clientList.append(crane1)
    clientList.append(crane2)
    # crane1.start()
    # crane2.start()
    '''

    ''' Initialization of AcThread and Pad Thread. there is nothing to be changed'''
    # PadThread = Thread(target=PadWorker, name='PadThread', args=(3,))
    # clientList.append(PadThread)

    padLock = Lock()
    padQueue = queue.LifoQueue()

    listOfLocks.append(padLock)
    listOfQueues.append(padQueue)

    padThreadIndex = listOfQueues.index(padQueue)

    PadThread = PadClient(name='PadThread', index=padThreadIndex, queue=listOfQueues[padThreadIndex],
                          lock=listOfLocks[padThreadIndex])
    PadThread.start()
    listOfThreads.append(PadThread)
    # PadThread.start()

    DataExchangeThread = Thread(target=communicateThreads, name='DataExchangeThread',
                                args=(listOfThreads, testCondition,))

    fuckingThread = Thread(target=startWorkingYouFucker, name='motherfucker', args=(listOfThreads,))
    fuckingThread.start()
    listOfThreads.append(fuckingThread)
    # clientList.append(AcThread)
    # for t in clientList:
    #     t.start()

    if not DataExchangeThread.isAlive():
        DataExchangeThread.start()

    while True:
        for client in listOfThreads:
            if client.isAlive():
                pass
            else:
                listOfThreads.remove(client)

        sock.listen(True)
        print('Server is waiting for cranes')
        (connection, (ip, port)) = sock.accept()

        try:
            createCraneThread()

        except:
            print("something went horribly wrong")

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

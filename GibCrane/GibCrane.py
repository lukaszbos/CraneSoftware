from builtins import print

from ClientThreads import *
from PadClient import *

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(asctime)s %(threadName)-10s %(message)s',
                    datefmt='%m/%d/%Y  %I:%M:%S %p')

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(asctime)s %(threadName)-10s %(message)s',
                    datefmt='%I:%M:%S %p')


# TODO Necessary integration of pad control program with threads

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


# TODO: dodac oddzielne porty dla kazdego urzadzenia

def startWorkingYouFucker(listOfThreadsTest):
    logging.info(' Starting')
    print(listOfThreadsTest)
    while True:
        for shit in listOfThreadsTest:
            logging.info(f'{shit.name} is alive')

        time.sleep(1.5)


class GibCrane:
    listOfThreads = []
    listOfLocks = []
    listOfQueues = []
    testCondition = Condition(Lock())

    def __init__(self, numberOfCranes):
        # tmpIP = "nah"
        self.numberOfCranes = numberOfCranes
        self._run()

    # TODO: ogarnać czy przypadkiem sie nie jebią indeksy bo to wygląda podejrzanie. czasami sie gówno wyswietla na ardu a czasasmi ni hcuja

    def communicateThreads(self, threads, condition: Condition):
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
                # print("type threada")
                # print(type(thread))
                if isinstance(thread, PadClient):
                    print("wchodzi to pierwsego ifa ")
                    with self.getLock(thread, threads):
                        # print(threads.index(thread))
                        pad_commands = self.listOfQueues[threads.index(thread)].get()
                        print("pad commands: ")
                        print(pad_commands)
                        # for m in receivedMessage:
                        #     inputList.append(m)
                    # print("pad")
                elif isinstance(thread, CraneClient):
                    #  with getLock(thread, threads):
                    print("wchodzi do ifa craneclient")
                    try:
                        print(self.listOfQueues[threads.index(thread) - 1].qsize())
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

            for thread in self.listOfThreads:
                ii = 0
                # print("i chuj")
                if isinstance(thread, CraneClient):
                    # while thread.isAlive():
                    # print("i chujeeeee")
                    current_command = pad_commands[ii]
                    # try:
                    thread.setOutput(current_command)
                    thread.sendCommandsToCrane()
                    print("pad commandyy: ")
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

    def getThreadByIndex(self, command, pad_commands):
        return self.listOfThreads[pad_commands.index(command) - 1]

    def getLock(self, thread, threads):
        return self.listOfLocks[threads.index(thread) - 1]

    def createCraneThread(self, connect):
        iterator = len(self.listOfThreads) - 1
        print('client connected')
        tempQueue = queue.LifoQueue()
        tempLock = Lock()
        self.listOfQueues.append(tempQueue)
        self.listOfLocks.append(tempLock)
        # crane_index = list
        crane = CraneClient('Crane', Crane(x=20, y=20, index=iterator),
                            Hook(z=100, r=40, theta=0),
                            inc=2 * PI / 360, delay=0.1, cond=self.testCondition, Queue=self.listOfQueues[iterator],
                            lock=self.listOfLocks[iterator], connection=connect)
        crane.isDaemon()
        return crane

    #
    # @staticmethod
    # def serverInit():
    #     global sock, port
    #     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     host = socket.gethostname()
    #     port = 10000
    #     sock.bind(('', port))
    #     print(socket.gethostname())
    #     # tmpIP = "nah"
    #
    # serverInit()
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
    def _run(self):
        # global sock, port
        # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        port = 10000
        listOfSockets = []
        # sock.bind(('', port))
        # print(socket.gethostname())
        padLock = Lock()
        padQueue = queue.LifoQueue()
        self.listOfLocks.append(padLock)
        self.listOfQueues.append(padQueue)

        padThreadIndex = self.listOfQueues.index(padQueue)
        PadThread = PadClient(name='PadThread', index=padThreadIndex, queue=self.listOfQueues[padThreadIndex],
                              lock=self.listOfLocks[padThreadIndex])
        PadThread.start()
        self.listOfThreads.append(PadThread)
        # PadThread.start()
        DataExchangeThread = Thread(target=self.communicateThreads, name='DataExchangeThread',
                                    args=(self.listOfThreads, self.testCondition,))
        DataExchangeThread.start()
        fuckingThread = Thread(target=startWorkingYouFucker, name='motherfucker', args=(self.listOfThreads,))
        fuckingThread.start()
        self.listOfThreads.append(fuckingThread)
        self.createSockets(host, listOfSockets, port)

        while True:
            for client in self.listOfThreads:
                if client.isAlive():
                    pass
                else:
                    self.listOfThreads.remove(client)
            tmpPort = 0
            for s in range(len(listOfSockets)):
                tmpPort = port + s
                print('Server is waiting for cranes')
                listOfSockets[s].listen(1)
                print(f'[*] Server listening on {host} {tmpPort}')
                (connection, (ip, tmpPort)) = listOfSockets[s].accept()
                try:
                    print('wchodzi tu')
                    crane = self.createCraneThread(connection)
                    self.listOfThreads.append(crane)
                    crane.start()
                except Exception:
                    print("something went horribly wrong")

    def createSockets(self, host, listOfSockets, port):
        for i in range(self.numberOfCranes):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('', port + i))
            print(f'created free socket: {socket.getaddrinfo(host, port)} ')
            listOfSockets.append(sock)


if __name__ == "__main__":
    with open('threadLogs.log', 'w'):
        pass
    GibCrane(2)
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

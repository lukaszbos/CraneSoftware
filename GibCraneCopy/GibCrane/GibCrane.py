from builtins import print
import sys
from ClientThreads import *
from PadClient import *
from SupportThreads import startWorkingYouFucker, communicateThreads

''' Chosen port used for local communication, and list of IP adresses hardcoded in arduino'''
PORT = 10000
listOfIpAddresses = ['192.168.0.171', '192.168.0.173', '192.168.0.172', '192.168.0.174']


logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(asctime)s %(threadName)-10s %(message)s',
                    datefmt='%m/%d/%Y  %I:%M:%S %p')

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(asctime)s %(threadName)-10s %(message)s',
                    datefmt='%I:%M:%S %p')

''' GibCrane is main class of program. It creates and manages all threads and connection between UDP clients '''


class GibCrane:
    #   Ip adresses of all 4 cranes.
    listOfThreads = []
    listOfLocks = []
    listOfQueues = []
    testCondition = Condition(Lock())

    def __init__(self):
        self._runGibCrane()

    def _runGibCrane(self):
        self.createPadControllingThread()
        self.createDataExchangeThread()
        self.createThisFuckingThread()
        self.createAllCranes(len(listOfIpAddresses))
        sock = self.createUdpCompatibleSocket()
        while True:
            self.communicateCranesWithSoftware(sock)

    def communicateCranesWithSoftware(self, sock):
        d = sock.recvfrom(1024)
        data = d[0]
        addr = d[1]
        if not data:
            print("no data")
            pass
        self.communicateWithProperCraneBasedOnIP(addr, sock)

    def createThisFuckingThread(self):  # Thread responsible for logging informations about alive threads
        fuckingThread = Thread(target=startWorkingYouFucker, name='motherfucker', args=(self.listOfThreads,))
        fuckingThread.setDaemon(True)
        fuckingThread.start()
        self.listOfThreads.append(fuckingThread)

    def createDataExchangeThread(self):
        DataExchangeThread = Thread(target=communicateThreads, name='DataExchangeThread',
                                    args=(self.listOfThreads, self.listOfQueues,
                                          self.listOfLocks,))
        DataExchangeThread.setDaemon(True)
        DataExchangeThread.start()

    def createPadControllingThread(self):
        padLock = Lock()
        padQueue = queue.LifoQueue()
        self.listOfLocks.append(padLock)
        self.listOfQueues.append(padQueue)
        padThreadIndex = self.listOfQueues.index(padQueue)
        PadThread = PadClient(name='PadThread',
                              index=padThreadIndex,
                              queue=self.listOfQueues[padThreadIndex],
                              lock=self.listOfLocks[padThreadIndex])
        PadThread.setDaemon(True)
        PadThread.start()
        self.listOfThreads.append(PadThread)

    def createCraneThreads(self, ipAddress):
        iterator = len(self.listOfThreads) - 1
        print('client connected')
        newQueue = queue.LifoQueue()
        newLock = Lock()
        self.listOfQueues.append(newQueue)
        self.listOfLocks.append(newLock)
        crane = CraneClient('Crane',
                            Crane(x=20, y=20, index=iterator),
                            Hook(z=100, r=40, theta=0),
                            inc=2 * PI / 360, delay=0.1,
                            Queue=self.listOfQueues[iterator],
                            lock=self.listOfLocks[iterator],
                            ip=ipAddress)
        crane.setDaemon(True)
        return crane

    def createAllCranes(self, amount):
        for i in range(amount):
            crane = self.createCraneThreads(listOfIpAddresses[i])
            self.listOfThreads.append(crane)
            crane.start()

    def communicateWithProperCraneBasedOnIP(self, addr, sock):
        for thread in self.listOfThreads:   # For each loop iterating on threads
            if isinstance(thread, CraneClient):   # if Type of thread is CraneClient
                print(f'Ip to compare: {thread.name} -> {thread.ip} | <-|-> {addr[0]}')
                if thread.CompareIP(addr[0]):   # Compares ip of iterated thread with ip from latest message
                    try:
                        sock.sendto(thread.getFullOutput(), addr)
                        print(f'{thread.name} has sent message: {thread.getFullOutput()}')
                    except Exception as exception:
                        print(f'message not sent. Exception {exception}')
                    break
            else:
                pass

    @staticmethod
    def createUdpCompatibleSocket():

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print('Socket created')
        except socket.error:
            print('Failed to create socket.')
            sys.exit()

        # Bind socket to local host and port
        try:
            s.bind(('', PORT))  # bind, binds socket with localhost at given port
            print('Bind succesful')
        except socket.error:
            print('Bind failed.')
            sys.exit()

        print('Socket bind complete')
        return s


if __name__ == "__main__":
    with open('threadLogs.log', 'w'):
        pass
    GibCrane()

from builtins import print
import sys
from CraneClient import *
from PadClient import *
from SupportThreads import startWorkingYouFucker, communicateThreads

'''
    GibCrane.py: Main class of program. It creates and manages all threads and connection between UDP clients 
    As program includes Threading module, in classes: Crane client, and PadClient, method run() is one that actually 
    is being run as thread. 
    Python version: 3.7

    Authors: Mateusz Jaszek, Izabella Piorek, Lukasz Michowski
'''

#  Chosen port used for local communication, and list of IP adresses hardcoded in arduino
PORT = 10000
listOfIpAddresses = ['192.168.0.171', '192.168.0.173', '192.168.0.172', '192.168.0.174']

#   Logs at INFO level, are going to be saved into threadLogs.log and deleted after each run of program
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(asctime)s %(threadName)-10s | %(message)s |',
                    datefmt='%m/%d/%Y  %I:%M:%S %p',
                    handlers=[logging.FileHandler('threadLogs.log'), logging.StreamHandler()])

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(asctime)s %(threadName)-10s %(message)s',
                    datefmt='%I:%M:%S %p')


class GibCrane:
    listOfThreads = []
    listOfLocks = []
    listOfQueues = []
    testCondition = Condition(Lock())

    def __init__(self):
        self.run()

    def run(self):
        self._createPadControllingThread()
        self._createDataExchangeThread()
        self._createThisFuckingThread()
        self._createAllCranes(len(listOfIpAddresses))
        sock = self._createUdpCompatibleSocket()
        while True:
            self._communicateCranesWithSoftware(sock)

    def _communicateCranesWithSoftware(self, sock):
        #   sock.recvfrom() returns tuple with data and address.
        #   address is also a tuple consisting of ipAddress and port
        d = sock.recvfrom(1024)
        data = d[0]
        addr = d[1]
        if not data:
            print("no data")
            pass
        self._communicateWithProperCraneBasedOnIP(addr, sock)

    def _createThisFuckingThread(self):  # creates thread responsible for logging informations about alive threads
        fuckingThread = Thread(target=startWorkingYouFucker, name='motherfucker', args=(self.listOfThreads,))
        fuckingThread.setDaemon(True)
        fuckingThread.start()
        self.listOfThreads.append(fuckingThread)

    def _createDataExchangeThread(self):    # creates thread responsible for data exchange between different threads
        DataExchangeThread = Thread(target=communicateThreads, name='DataExchangeThread',
                                    args=(self.listOfThreads, self.listOfQueues,
                                          self.listOfLocks,))
        DataExchangeThread.setDaemon(True)
        DataExchangeThread.start()

    def _createPadControllingThread(self):
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

    def _createCraneThreads(self, ipAddress):
        iterator = len(self.listOfThreads) - 1
        print('client connected')
        newQueue = queue.LifoQueue()
        newLock = Lock()
        self.listOfQueues.append(newQueue)
        self.listOfLocks.append(newLock)
        # Crane and Hook from constructor below, are objects defined in GpsOpjects.py
        crane = CraneClient('Crane',
                            Crane(x=20, y=20, index=iterator),
                            Hook(z=100, r=40, theta=0),
                            inc=2 * PI / 360, delay=0.1,
                            Queue=self.listOfQueues[iterator],
                            lock=self.listOfLocks[iterator],
                            ip=ipAddress)
        crane.setDaemon(True)
        return crane

    def _createAllCranes(self, amount):
        for i in range(amount):
            crane = self._createCraneThreads(listOfIpAddresses[i])
            self.listOfThreads.append(crane)
            crane.start()

    def _communicateWithProperCraneBasedOnIP(self, addr, sock):
        for thread in self.listOfThreads:  # For each loop iterating on threads
            if isinstance(thread, CraneClient):  # if Type of thread is CraneClient
                print(f'Ip to compare: {thread.name} -> {thread.ip} | <-|-> {addr[0]}')
                if thread.CompareIP(addr[0]):  # Compares ip of iterated thread with ip from latest message
                    try:
                        sock.sendto(thread.getFullOutput(), addr)
                        print(f'{thread.name} has sent message: {thread.getFullOutput()}')
                    except Exception as exception:
                        logging.info(f'Exception Happened while sending data to {thread.name}. Exception: {exception}')
                        print(f'message not sent. Exception {exception}')
                    break
            else:
                pass

    @staticmethod
    def _createUdpCompatibleSocket():

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print('Socket created')
        except socket.error:
            print('Failed to create socket.')
            sys.exit()

        # Bind socket to local host and port
        try:
            s.bind(('', PORT))  # bind, binds socket with localhost at given port
            logging.info(f'Socket successfully bound to localhost')
            print('Bind succesful')
        except socket.error:
            logging.info('Bind has failed')
            print('Bind failed.')
            sys.exit()

        print('Socket bind complete')
        return s


if __name__ == "__main__":
    with open('threadLogs.log', 'w'):
        pass
    GibCrane()

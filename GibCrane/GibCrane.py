from builtins import print

from ClientThreads import *
from PadClient import *

''' Wersja działająca tak jak ci mówiłem, czyli:
        > czeka na połączenie
        > jesli uzyska połączenie to tworzy nowego clienta a główny wątek programu dalej czeka na połączenia
        > nowy client dostaje stale informacje 
        > jesli dostanie kolejne połączenie, to nowe zaczya dostawać dane a stare przestaje
'''

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(asctime)s %(threadName)-10s %(message)s',
                    datefmt='%m/%d/%Y  %I:%M:%S %p')

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(asctime)s %(threadName)-10s %(message)s',
                    datefmt='%I:%M:%S %p')


# TODO Necessary integration of pad control program with threads


# TODO: dodac oddzielne porty dla kazdego urzadzenia

class GibCrane:
    ''' Tutaj są stworzone wszystkie tablice wątków, zamków i kolejek '''
    listOfThreads = []
    listOfLocks = []
    listOfQueues = []
    testCondition = Condition(Lock())

    def __init__(self, Port):
        # tmpIP = "nah"
        self._run()

    # TODO: ogarnać czy przypadkiem sie nie jebią indeksy bo to wygląda podejrzanie. czasami sie gówno wyswietla na ardu a czasasmi ni hcuja

    ''' Ta metoda, jest odpalana jako watek który wypisuje logi informujące o każdym z aktywnych wątków'''

    def startWorkingYouFucker(self, listOfThreadsTest):
        logging.info(' Starting')
        print(listOfThreadsTest)
        while True:
            for shit in listOfThreadsTest:
                logging.info(f'{shit.name} is alive')

            time.sleep(1.5)

    ''' Ta metoda jest odpalana jako wątek obsługujacy komunikację między wątkami '''

    def communicateThreads(self, threads, condition: Condition):
        delay = 1 / 10
        logging.info(' Starting')
        while True:
            inputList = []
            pad_commands = [[], []]
            receivedMessage = []
            for thread in threads:  # pętla iterująca po tablicy wątków
                if isinstance(thread, PadClient):  # sprawdzenie typu wątku
                    # print("wchodzi to pierwsego ifa ")
                    with self.getLock(thread, threads):
                        # print(threads.index(thread))
                        pad_commands = self.listOfQueues[
                            threads.index(thread)].get()  # pobiera z kolejki komunikaty z padów
                        print("pad commands: ")
                        print(pad_commands)

                elif isinstance(thread, CraneClient):  # znowu sprawdza typ wątku ale ta część na razie nic nie robi
                    #  with getLock(thread, threads):
                    try:
                        print(self.listOfQueues[threads.index(thread) - 1].qsize())
                    except Exception:
                        print(Exception)

            ''' Po tym jak skonczy pobierac dane z wątków, wysyła je do odpowiednich klientów'''

            for thread in threads:
                ii = 0
                # print("i chuj")
                if isinstance(thread, CraneClient):
                    # while thread.isAlive():
                    # print("i chujeeeee")
                    current_command = pad_commands[ii]
                    # try:
                    thread.setOutput(current_command)
                    print("pad commandyy: ")
                    print(current_command)
                    ii += 1
                # except IOError:
                #   print(IOError)
                #  print("Exeption in loop in commands")
                else:
                    print("notting happened")

            time.sleep(delay)

    ''' zwraca odpowiedni lock dla wątku'''
    def getLock(self, thread, threads):
        return self.listOfLocks[threads.index(thread) - 1]

    ''' Tworzy i zwraca wątek klienta dzwigu '''
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

    ''' 
        Główna metoda klasy GibCrane, tworzy połączenie i przekazuje je do odpowiedniego wątku 
        który również tworzy po uzyskaniu połączenia
    '''
    def _run(self):
        global sock, port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        port = 10000

        sock.bind(('', port))
        print(socket.gethostname())

        padLock = Lock()
        padQueue = queue.LifoQueue()

        self.listOfLocks.append(padLock)
        self.listOfQueues.append(padQueue)

        padThreadIndex = self.listOfQueues.index(padQueue)

        PadThread = PadClient(name='PadThread', index=padThreadIndex, queue=self.listOfQueues[padThreadIndex],
                              lock=self.listOfLocks[padThreadIndex])    #utworzenie wątku obsługującego pady
        PadThread.start()
        self.listOfThreads.append(PadThread)
        # PadThread.start()

        DataExchangeThread = Thread(target=self.communicateThreads, name='DataExchangeThread',
                                    args=(self.listOfThreads, self.testCondition,))     #   Utworzenie wątku obsługującego
        DataExchangeThread.start()                                                      #   połączenia między wątkami

        fuckingThread = Thread(target=self.startWorkingYouFucker, name='motherfucker', args=(self.listOfThreads,))
        fuckingThread.start()   # Utworzenie wątku zwracającego ifo o działających w programie wątkach
        self.listOfThreads.append(fuckingThread)
        # clientList.append(AcThread)
        # for t in clientList:
        #     t.start()

        while True:
            for client in self.listOfThreads:
                if client.isAlive():
                    pass
                else:
                    self.listOfThreads.remove(client)

            sock.listen(1)
            print('Server is waiting for cranes')
            (connection, (ip, port)) = sock.accept()

            try:
                print('wchodzi tu')     # Tutaj po uzyskaniu połączenia tworzy się nowy wątek klienta opisany w ClientThreads.py
                crane = self.createCraneThread(connection)
                self.listOfThreads.append(crane)
                crane.start()
            except Exception:
                print("something went horribly wrong")


if __name__ == "__main__":
    with open('threadLogs.log', 'w'):
        pass
    GibCrane(10000)
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

from builtins import print
import sys
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
    listOfIpAddresses = ['192.168.0.172', '192.168.0.174', '192.168.0.171', '192.168.0.173']

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
        delay = 1 / 50
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
                        pass
                        # print(self.listOfQueues[threads.index(thread) - 1].qsize())
                    except Exception:
                        print(Exception)

            ''' Po tym jak skonczy pobierac dane z wątków, wysyła je do odpowiednich klientów'''

            ii = 0
            for thread in threads:
                # print("i chuj")
                if isinstance(thread, CraneClient):
                    # while thread.isAlive():
                    # print("i chujeeeee")
                    # print(thread.name)
                    # print(ii)
                    try:
                        current_command = pad_commands[ii]
                        # try:
                        thread.setOutput(current_command)
                    except Exception as e:
                        pass
                        # print(f'[*] Exception happened in {thread.name}: {e}')
                    # print("pad commandyy: ")
                    # print(f'FROM PAD {ii} : |{current_command}|')

                    ii += 1
                # except IOError:
                #   print(IOError)
                #  print("Exeption in loop in commands")
                else:
                    # print("notting happened")
                    pass

            time.sleep(delay)

    ''' zwraca odpowiedni lock dla wątku'''

    def getLock(self, thread, threads):
        return self.listOfLocks[threads.index(thread) - 1]

    ''' Tworzy i zwraca wątek klienta dzwigu '''

    def createCraneThreads(self, IPaddress):
        iterator = len(self.listOfThreads) - 1
        print('client connected')
        tempQueue = queue.LifoQueue()
        tempLock = Lock()
        self.listOfQueues.append(tempQueue)
        self.listOfLocks.append(tempLock)
        # crane_index = list
        crane = CraneClient('Crane', Crane(x=20, y=20, index=iterator),
                            Hook(z=100, r=40, theta=0),
                            inc=2 * PI / 360, delay=0.1,
                            cond=self.testCondition,
                            Queue=self.listOfQueues[iterator],
                            lock=self.listOfLocks[iterator],
                            ip=IPaddress)
        crane.isDaemon()
        return crane

    ''' 
        Główna metoda klasy GibCrane, tworzy połączenie i przekazuje je do odpowiedniego wątku 
        który również tworzy po uzyskaniu połączenia
    '''

    def _run(self):
        padLock = Lock()
        padQueue = queue.LifoQueue()

        self.listOfLocks.append(padLock)
        self.listOfQueues.append(padQueue)

        padThreadIndex = self.listOfQueues.index(padQueue)

        PadThread = PadClient(name='PadThread', index=padThreadIndex, queue=self.listOfQueues[padThreadIndex],
                              lock=self.listOfLocks[padThreadIndex])  # utworzenie wątku obsługującego pady
        PadThread.start()
        self.listOfThreads.append(PadThread)
        # PadThread.start()

        DataExchangeThread = Thread(target=self.communicateThreads, name='DataExchangeThread',
                                    args=(self.listOfThreads, self.testCondition,))  # Utworzenie wątku obsługującego
        DataExchangeThread.start()  # połączenia między wątkami

        fuckingThread = Thread(target=self.startWorkingYouFucker, name='motherfucker', args=(self.listOfThreads,))
        fuckingThread.start()  # Utworzenie wątku zwracającego ifo o działających w programie wątkach
        self.listOfThreads.append(fuckingThread)

        # clientList.append(AcThread)
        # for t in clientList:
        #     t.start()

        # socketList = []

        # iterator = 0

        # global sock, port
        # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # #
        # host = socket.gethostname()
        # port = 10000
        # sock.bind(('', port))
        # print(socket.gethostname())
        # connectionList = []

        self.createAllCranes(len(self.listOfIpAddresses))
        sock = self.createSocket()

        while True:

            # for client in self.listOfThreads:
            #     if client.isAlive():
            #         pass
            #     else:
            #         self.listOfThreads.remove(client)
            print('waiting for message')
            d = sock.recvfrom(1024)
            print('message received')
            data = d[0]
            addr = d[1]
            if not data:
                print("no data")
                pass
            print(addr[0])

            for thread in self.listOfThreads:
                # print('for dziala')
                if isinstance(thread, CraneClient):
                    # while True:

                    print(f'{thread.name}: jest dzwigiem')
                    print(f'Ip to compare: {thread.name} -> {thread.ip} | Current message -> {addr[0]}')
                    if thread.CompareIP(addr[0]):
                        print(f'{thread.name}: ip sie zgadza')
                        try:
                            sock.sendto(thread.getFullOutput(), addr)
                            print(f'{thread.name} has sent message')
                            # break
                        except Exception as e:
                            print(f'message not sent. Exception {e}')
                        # print(thread.getFullOutput())
                        break
                else:
                    # print('nie jest dzwigiem')
                    pass
            print('Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.decode())

    def createAllCranes(self, amount):
        for i in range(amount):
            crane = self.createCraneThreads(self.listOfIpAddresses[i])
            self.listOfThreads.append(crane)
            crane.start()

    def createSocket(self):
        host = ''
        port = 10000

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print('Socket created')
        except socket.error:
            print('Failed to create socket.')
            sys.exit()

        # Bind socket to local host and port
        try:
            s.bind(('', port))
            print('Bind succesful')
        except socket.error:
            print('Bind failed.')
            sys.exit()

        print('Socket bind complete')
        return s
        # listOfSockets.append(sock)


if __name__ == "__main__":
    with open('threadLogs.log', 'w'):
        pass
    GibCrane(10000)

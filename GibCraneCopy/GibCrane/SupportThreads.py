import time
import logging

from PadClient import PadClient
from ClientThreads import CraneClient


def startWorkingYouFucker(listOfThreadsTest):
    logging.info(' Starting')
    print(listOfThreadsTest)
    while True:
        for shit in listOfThreadsTest:
            logging.info(f'{shit.name} is alive')

        time.sleep(1.5)


def getLock(thread, threads, listOfLocks):
    return listOfLocks[threads.index(thread) - 1]


def communicateThreads(threads, listOfQueues, listOfLocks):
    delay = 1 / 50
    logging.info(' Starting')
    while True:
        pad_commands = [[], []]
        for thread in threads:  # pętla iterująca po tablicy wątków
            if isinstance(thread, PadClient):  # sprawdzenie typu wątku
                with getLock(thread, threads, listOfLocks):
                    pad_commands = listOfQueues[
                        threads.index(thread)].get()  # pobiera z kolejki komunikaty z padów

            elif isinstance(thread, CraneClient):  # znowu sprawdza typ wątku ale ta część na razie nic nie robi
                try:
                    pass
                except Exception as e:
                    print(e)

        ''' Po tym jak skonczy pobierac dane z wątków, wysyła je do odpowiednich klientów'''

        ii = 0
        for thread in threads:
            if isinstance(thread, CraneClient):
                try:
                    current_command = pad_commands[ii]
                    thread.setOutput(current_command)
                except Exception as e:
                    pass

                ii += 1
            else:
                pass

        time.sleep(delay)

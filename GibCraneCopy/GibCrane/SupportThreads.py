import time
import logging

from PadClient import PadClient
from CraneClient import CraneClient

'''
    SupportThreads.py: File contains definitions of 2 essential methods running as separate threads:
    > communicateThreads - thread handling communication between threads
    > loggingThreadFunction - thread responsible for logging information about status of all running threads
    
    Python version: 3.7
    
    Authors: Mateusz Jaszek
'''


def loggingThreadFunction(listOfThreadsTest):
    logging.info(' Starting')
    print(listOfThreadsTest)
    while True:
        for shit in listOfThreadsTest:
            logging.info(f'{shit.name} is alive')

        time.sleep(1.5)


def communicateThreads(threads, listOfQueues, listOfLocks):
    delay = 1 / 50
    logging.info(' Starting')
    while True:
        pad_commands = getDataFromThreads(listOfLocks, listOfQueues, threads)
        passDataToCraneThreads(pad_commands, threads)
        time.sleep(delay)


def passDataToCraneThreads(pad_commands, threads):
    ii = 0
    for thread in threads:
        if isinstance(thread, CraneClient):
            try:
                current_command = pad_commands[ii]
                thread.setOutput(current_command)
            except Exception as exception:
                logging.info(f'Exception has happend: {exception}')

            ii += 1
        else:
            pass


def getDataFromThreads(listOfLocks, listOfQueues, threads):
    pad_commands = [[], []]
    for thread in threads:
        # Below, type of thread is checked and things happen according to that
        if isinstance(thread, PadClient):
            with getLock(thread, threads, listOfLocks):
                pad_commands = listOfQueues[
                    threads.index(thread)].get()

        # TODO: Here we should add getting feedback from cranes
        elif isinstance(thread, CraneClient):
            try:
                pass
            except Exception as e:
                print(e)
    return pad_commands


#   Gets lock for right crane and uses it to get data from correct queue
def getLock(thread, threads, listOfLocks):
    return listOfLocks[threads.index(thread) - 1]

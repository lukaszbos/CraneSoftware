import GpsObjects
import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-5s %(message)s',)

def worker():
    print("This thread will count down to 5 seconds")

    logging.debug('running')
    for i in range(5):
        time.sleep(1)
        print(i+1)

    print("thread has finished", threading.current_thread().getName())
    logging.debug('has ended')

class testThread(threading.Thread):
    def __init__(self):
        super(testThread, self).__init__()
    def run(self):
        logging.debug('running'.format(self.getName()))
        time.sleep(3)
        logging.debug('has finished'.format(self.getName()))


if __name__ == "__main__":

    testTable = GpsObjects.table()
    testCrane = GpsObjects.crane()
    testHook = GpsObjects.hook()


    testCrane.setIndex(1)
    testCrane.setX(30)
    testCrane.setY(30)

    testHook.setZ(90)
    testHook.setR(50)
    testHook.setTheta(GpsObjects.PI / 8)

    testHook.convertRadial(testCrane)

    workerThread = threading.Thread(target=worker())
    classThread = testThread()

    classThread.start()
    workerThread.start()


    # print(testHook.getX(), testHook.getY(), testHook.getZ())



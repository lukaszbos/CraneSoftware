from GpsObjects import *
from threading import *
import time
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(asctime)s %(threadName)-10s %(message)s',
                    datefmt='%m/%d/%Y  %I:%M:%S %p')


# logger below will write logs out to file

# logging.basicConfig(level=logging.INFO, filename='threadLogs.log',
#                     format='%(levelname)s: %(asctime)s %(threadName)-10s %(message)s',
#                     datefmt='%m/%d/%Y  %I:%M:%S %p')


class CraneClient(Thread):
    def __init__(self, crane: Crane, hook: Hook, inc, delay):
        Thread.__init__(self)
        self._crane = crane
        self._hook = hook
        self._inc = inc
        self._delay = delay
    _running = False

    def run(self) -> None:
        logging.info('Starting')
        _running = True
        while _running:
            self._hook.convertRadial(self._crane)
            self._hook.SetTheta(self._hook.GetTheta()+self._inc)

            print(f'Hook_{self._crane.GetIndex()} '
                  f'coordinates are: X={self._hook.GetX()} '
                  f'Y={self._hook.GetY()} '
                  f'Z={self._hook.GetZ()} ')
            time.sleep(self._delay)

        logging.info('ending')

    def killThread(self):
        _running = False


if __name__ == "__main__":
    with open('threadLogs.log', 'w'):
        pass

    craneClientList = []

    crane1 = CraneClient(Crane(x=20, y=20, index=1),
                         Hook(z=100, r=40, theta=0), 2*PI/360, 1)

    crane2 = CraneClient(Crane(x=180, y=180, index=2),
                         Hook(z=150, r=80, theta=0), -2*PI/360, 2)

    crane1.start()
    crane2.start()

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

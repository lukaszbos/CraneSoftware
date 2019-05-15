import threading
# from threading import Thread
import time


class sleeperClass(threading.Thread):
    def __init__(self, n, value):
        threading.Thread.__init__(self)

        # threading.Thread.in
        self.n = n
        self.name = value

    def run(self):
        # print(f"hi, i am {self.name}. I am going to sleep for {self.n} seconds")
        for i in range(self.n):
            time.sleep(1)
            # print('zzZ')
        print(f'{self.name} is awake now')


# def sleeperMethod(n, name):
#     print(f"hi, i am {name}. I am going to sleep for {n} seconds")
#     for i in range(n):
#         time.sleep(1)
#         print('zzZ')
#     print('{} is awake now'.format(name))


# sleeperMethodThread = threading.Thread(target=sleeperMethod,
#                                  name='thread 1',
#                                  args=(3, 'thread 1'))
#
# sleeperMethodThread.start()

threads_list = []

start = time.time()

for i in range(5):
    # t = threading.Thread(target=sleeperMethod,
    #                      name = 'thread_{}'.format(i+1),
    #                      args=(5 - i, 'thread_{}'.format(i+1)))

    t = sleeperClass(5 - i, f'thread_{i + 1}')
    t.start()
    threads_list.append(t)

for t in threads_list:
    t.join()

end = time.time()

print('time taken: {}'.format(end - start))

print('all threads are awake')

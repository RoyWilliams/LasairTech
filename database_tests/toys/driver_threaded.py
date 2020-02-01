import threading
import toys
import time
import random

class insert_thread(threading.Thread):
    def __init__(self, threadID, nthread, number):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.number = number
        self.msl = toys.make_db_connection()
        toys.start_again(self.msl)

    def run(self):
        t = time.time()
        toys.insert_record(self.msl, self.number, debug=False)
        print("--%d-- %d inserts made in %.2f seconds" % (self.threadID, self.number, time.time()-t))

class select_thread(threading.Thread):
    def __init__(self, threadID, nthread, number):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.number = number
        self.msl = toys.make_db_connection()

    def run(self):
        t = time.time()
        for i in range(self.number):
            x = random.random()
            y = random.random()
            if x < y: toys.select_range(self.msl, x, y, debug=False)
            else:     toys.select_range(self.msl, y, x, debug=False)
        print("--%d-- %d selections in %.2f seconds" % (self.threadID, self.number, time.time()-t))

###################
import sys

if len(sys.argv) < 4:
    print('Usage: driver_threaded.py nthread number_insert number_select')
    sys.exit()
else:
    nthread =       int(sys.argv[1])
    number_insert = int(sys.argv[2])
    number_select = int(sys.argv[3])

start = time.time()
thread_list = []
for t in range(nthread):
    thread_list.append(insert_thread(t, nthread, number_insert))
for th in thread_list: th.start()
for th in thread_list: th.join()
print('=======Inserts %.1f seconds =========' % ((time.time()-start)))

start = time.time()
thread_list = []
for t in range(nthread):
    thread_list.append(select_thread(t, nthread, number_insert))
for th in thread_list: th.start()
for th in thread_list: th.join()
print('=======Selects %.1f seconds =========' % ((time.time()-start)))

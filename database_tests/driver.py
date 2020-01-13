import toys
import time
import random

class insert_thread():
    def __init__(self, msl, number):
        self.msl = msl
        self.number = number

    def run(self):
        t = time.time()
        toys.insert_record(self.msl, self.number, debug=False)
        print("%d inserts made in %.2f seconds" % (self.number, time.time()-t))

class select_thread():
    def __init__(self, msl, number):
        self.number = number
        self.msl = msl

    def run(self):
        t = time.time()
        for i in range(self.number):
            x = random.random()
            y = random.random()
            if x < y: toys.select_range(self.msl, x, y, debug=False)
            else:     toys.select_range(self.msl, y, x, debug=False)
        print("%d selections in %.2f seconds" % (self.number, time.time()-t))

###################
import sys

if len(sys.argv) < 3:
    print('Usage: driver_threaded.py number_insert number_select')
    sys.exit()
else:
    number_insert = int(sys.argv[1])
    number_select = int(sys.argv[2])
print(number_insert, number_select)

msl = toys.make_db_connection()
toys.start_again(msl)
print("ready")

start = time.time()
i = insert_thread(msl, number_insert)
i.run()
print('=======Inserts %.1f seconds =========' % ((time.time()-start)))

start = time.time()
s = select_thread(msl, number_insert)
s.run()
print('=======Selects %.1f seconds =========' % ((time.time()-start)))

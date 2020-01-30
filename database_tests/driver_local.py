import toys
import time
import random
import sys

if len(sys.argv) < 3:
    print('Usage: driver_threaded.py maxid number_insert')
    sys.exit()

maxid         = int(sys.argv[1])
number_insert = int(sys.argv[2])

msl = toys.make_db_connection(remote=False)
toys.start_again(msl)

start = time.time()
toys.insert_record(msl, maxid, number_insert, debug=False)
print("%d inserts made in %.2f seconds" % (number_insert, time.time()-start))

toys.write_file(msl, '~/scratch/out.txt', debug=False)

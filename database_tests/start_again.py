import toys
import time
import random
import sys

msl = toys.make_db_connection(remote=True)
toys.start_again(msl, memory=False)

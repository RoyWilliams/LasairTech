import mysql.connector
import settings
import random

def make_db_connection(remote=True):
    config = {
        'user'    : settings.DB_USER_WRITE,
        'password': settings.DB_PASS_WRITE,
        'host'    : settings.DB_HOST_REMOTE,
        'database': 'ztf'
    }
    if not remote:
        config['host'] = settings.DB_HOST_LOCAL
    msl = mysql.connector.connect(**config)
    return msl


def start_again(msl):
    test_table = """
    create table test_table(
    id         int,
    value      double,
    PRIMARY KEY (id)
    )
"""
# This function drops the two tables and recreates them
    cursor = msl.cursor(buffered=True, dictionary=True)
    query = 'DROP TABLE IF EXISTS test_table'
    cursor.execute(query)
    cursor.execute(test_table)

def print_numbers(msl):
    cursor = msl.cursor(buffered=True, dictionary=True)
    query = 'SELECT COUNT(*) AS ncand FROM test_table'
    cursor.execute(query)
    for record in cursor: break
    ncand = record['ncand']

    print('  %d values' % ncand)

def insert_record(msl, maxid, n, debug=False):
    for i in range(n):
        id = random.randrange(0, maxid)
        value = random.random()
        query = 'REPLACE INTO test_table (id, value) VALUES (%d, %f)' % (id, value)
        if debug: print(query)
        cursor = msl.cursor(buffered=True, dictionary=True)
        cursor.execute(query)
    msl.commit()

def select_range(msl, min, max, debug=False):
    query = 'SELECT value from test_table where value > %f and value < %f' % (min, max)

    if debug: print(query)
    cursor  = msl.cursor(buffered=True, dictionary=True)
    cursor.execute(query)
    msl.commit()
#    print('Found %d values' % cursor.rowcount)

def write_file(msl, filename, debug=False):
    f = open(filename, 'w')
    query = 'SELECT id,value from test_table'
    if debug: print(query)
    cursor  = msl.cursor(buffered=True, dictionary=True)
    cursor.execute(query)
    for row in cursor:
        f.write('%d\t%f\n' % (row['id'], row['value']))
    f.close()

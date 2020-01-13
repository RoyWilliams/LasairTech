import mysql.connector
import settings
import random

def make_db_connection():
    config = {
        'user'    : settings.DB_USER_WRITE,
        'password': settings.DB_PASS_WRITE,
        'host'    : settings.DB_HOST,
        'database': 'ztf'
    }
    msl = mysql.connector.connect(**config)
    return msl

test_table = """
create table test_table(
    id         int NOT NULL AUTO_INCREMENT,
    value      double,
    PRIMARY KEY (id)
)
"""

def start_again(msl):
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

def insert_record(msl, n, debug=False):
    for i in range(n):
        value = random.random()
        query = 'INSERT INTO test_table (value) VALUES (%f)' % value
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

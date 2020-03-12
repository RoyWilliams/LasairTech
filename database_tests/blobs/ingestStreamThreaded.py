"""Consumes stream for ingesting to database

"""

from __future__ import print_function
import argparse
import sys
import os
import time
import settings
import mysql.connector
import threading
import alertConsumer
import objectStore

def msg_text(message):
    """Remove postage stamp cutouts from an alert message.
    """
    message_text = {k: message[k] for k in message
                    if k not in ['cutoutDifference', 'cutoutTemplate', 'cutoutScience']}
    return message_text

def write_stamp_file(stamp_dict, store):
    """Given a stamp dict that follows the cutout schema,
       write data to a file in a given directory.
    """
    store.putObject(stamp_dict['fileName'], stamp_dict['stampData'])
#    try:
#        filename = stamp_dict['fileName']
#        try:
#            os.makedirs(output_dir)
#        except OSError:
#            pass
#        out_path = os.path.join(output_dir, filename)
#        with open(out_path, 'wb') as f:
#            f.write(stamp_dict['stampData'])
#    except TypeError:
#        print('%% Cannot get stamp\n')
    return

def alert_filter(alert, store):
    """Filter to apply to each alert.
       See schemas: https://github.com/ZwickyTransientFacility/ztf-avro-alert
    """
    candid = 0
    data = msg_text(alert)
    if data:  # Write your condition statement here
        if store:  # Collect all postage stamps
            write_stamp_file( alert.get('cutoutDifference'), store)
            write_stamp_file( alert.get('cutoutTemplate'),   store)
            write_stamp_file( alert.get('cutoutScience'),    store)
        return candid

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', type=str,
                        help='Hostname or IP of Kafka host to connect to.')
    parser.add_argument('--topic', type=str,
                        help='Name of Kafka topic to listen to.')
    parser.add_argument('--group', type=str,
                        help='Globally unique name of the consumer group. '
                        'Consumers in the same group will share messages '
                        '(i.e., only one consumer will receive a message, '
                        'as in a queue). Default is value of $HOSTNAME.')
    parser.add_argument('--maxalert', type=int,
                        help='Max alerts to be fetched per thread')
    parser.add_argument('--nthread', type=int,
                        help='Number of threads to use')
    parser.add_argument('--stampdir', type=str,
                        help='Directory for blobs')

    args = parser.parse_args()

    return args

class Consumer(threading.Thread):
    def __init__(self, threadID, args, store, conf):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.conf = conf
        self.store = store
        self.args = args

    def run(self):
        try:
            streamReader = alertConsumer.AlertConsumer(self.args.topic, **self.conf)
            streamReader.__enter__()
        except alertConsumer.EopError as e:
            print('INGEST Cannot start reader: %d: %s\n' % (self.threadID, e.message))
            return
    
        if self.args.maxalert:
            maxalert = self.args.maxalert
        else:
            maxalert = 50000
    
        nalert = 0
        startt = time.time()
        while nalert < maxalert:
            try:
                msg = streamReader.poll(decode=True, timeout=settings.KAFKA_TIMEOUT)
            except alertConsumer.EopError as e:
                print('INGEST',self.threadID, e)
                break

            if msg is None:
#                print(self.threadID, 'null message')
                break
            else:
                for record in msg:
                    # Apply filter to each alert
                    candid = alert_filter(record, self.store)
                    nalert += 1
                    if nalert%1000 == 0:
                        print('thread %d nalert %d time %.1f' % ((self.threadID, nalert, time.time()-startt)))
                        msl.close()
                        msl = make_database_connection()
    
        print('INGEST %d finished with %d alerts' % (self.threadID, nalert))

        streamReader.__exit__(0,0,0)

def main():
    args = parse_args()

    # Configure consumer connection to Kafka broker
#    print('Connecting to Kafka at %s' % args.host)
#    conf = {'bootstrap.servers': '{}:9092,{}:9093,{}:9094'.format(args.host,args.host,args.host),
#            'default.topic.config': {'auto.offset.reset': 'smallest'}}
    conf = {'bootstrap.servers': '{}:9092'.format(args.host,args.host,args.host),
            'default.topic.config': {'auto.offset.reset': 'smallest'}}

    if args.group: conf['group.id'] = args.group
    else:          conf['group.id'] = 'LASAIR'

    if args.stampdir:
        store = obj.objectStore(suffix='fits', fileroot='stampdir')

    print('Configuration = %s' % str(conf))

    if args.nthread:
        nthread = args.nthread
    else:
        nthread = 1
    print('Threads = %d' % nthread)

    # make the thread list
    thread_list = []
    for t in range(args.nthread):
        thread_list.append(Consumer(t, args, store, conf))
    
    # start them up
    t = time.time()
    for th in thread_list:
         th.start()
    
    # wait for them to finish
    for th in thread_list:
         th.join()

if __name__ == '__main__':
    main()

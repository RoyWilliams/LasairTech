"""Consumes stream for ingesting to database

"""

from __future__ import print_function
import argparse
import sys
import os
import time
import threading
import alertConsumer

# Configure Avro reader schema
schema_files = ['ztf-avro-alert/schema/candidate.avsc',
                'ztf-avro-alert/schema/cutout.avsc',
                'ztf-avro-alert/schema/prv_candidate.avsc',
                'ztf-avro-alert/schema/alert.avsc']

def msg_text(message):
    """Remove postage stamp cutouts from an alert message.
    """
    message_text = {k: message[k] for k in message
                    if k not in ['cutoutDifference', 'cutoutTemplate', 'cutoutScience']}
    return message_text

def alert_filter(alert):
    """Filter to apply to each alert.
       See schemas: https://github.com/ZwickyTransientFacility/ztf-avro-alert
    """
    candid = 0
    data = msg_text(alert)
    if data:  # Write your condition statement here

        objectId = data['objectId']
        candid   = data['candid']

# look for non detection limiting magnitude
        prv_array = data['prv_candidates']
        if prv_array:
            noncanlist = []
            query4 = ''
            for prv in prv_array:
                if prv['candid']:
                    if prv['magpsf']:
#                        insert_candidate(msl, prv, objectId, stalefile)
#                        print('%s %s' % (objectId, str(prv['candid'])))
                        pass
                else:
                    jd         = prv['jd']
                    fid        = prv['fid']
                    diffmaglim = prv['diffmaglim']
                    noncanlist.append('("%s", %.5f, %d, %.3f)' % (objectId, jd, fid, diffmaglim))
            if len(noncanlist) > 0:
                t = time.time()
                query4 = 'INSERT INTO noncandidates (objectId, jd, fid, diffmaglim) VALUES '
                query4 += ', '.join(noncanlist)

        t = time.time()
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
    parser.add_argument('--frombeginning', 
                         help='Start from the beginning of the topic',
                         action='store_true')
    parser.add_argument('--stampdump',
                        help='Write postage stamp to /stamps/<dir>')
    parser.add_argument('--avrodump', 
                        help='Write each avro alert to a file in /avros',
                        action='store_true')
    parser.add_argument('--logging', type=str,
                        help='Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL')
    parser.add_argument('--maxalert', type=int,
                        help='Max alerts to be fetched per thread')
    parser.add_argument('--timeout', type=int,
                        help='Kafka timeout in seconds')
    parser.add_argument('--nthread', type=int,
                        help='Number of threads to use')

    args = parser.parse_args()

    return args

class Consumer(threading.Thread):
    def __init__(self, threadID, args, conf):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.conf = conf
        self.args = args

    def run(self):
        try:
            streamReader = alertConsumer.AlertConsumer(self.args.topic, self.args.frombeginning, schema_files, **self.conf)
            streamReader.__enter__()
        except alertConsumer.EopError as e:
            print('Cannot start reader: %d: %s\n' % (self.threadID, e.message))
            return
    
        if self.args.maxalert: maxalert = self.args.maxalert
        else:                  maxalert = 50000
        if self.args.timeout:  timeout = self.args.timeout
        else:                  timeout = 60
    
        startt = time.time()
        nalert = 0
        while nalert < maxalert:
            t = time.time()
            try:
                msg = streamReader.poll(decode=True, timeout=timeout)
            except alertConsumer.EopError as e:
                print(self.threadID, e)
                break

            nalert += 1
            if nalert%5000 == 0:
                print('thread %d nalert %d time %.1f' % ((self.threadID, nalert, time.time()-startt)))

            if msg is None:
                break
            else:
                for record in msg:
                    candid = alert_filter(record)
        print('%d: finished with %d alerts' % (self.threadID, nalert))

        streamReader.__exit__(0,0,0)

def main():
    args = parse_args()
    conf = {'bootstrap.servers': '{}:9092'.format(args.host,args.host,args.host),
            'default.topic.config': {'auto.offset.reset': 'smallest'}}

    if args.group: conf['group.id'] = args.group
    else:          conf['group.id'] = 'LASAIR'

    if args.nthread:
        nthread = args.nthread
    else:
        nthread = 1
    print('Threads = %d' % nthread)

    # make the thread list
    thread_list = []
    for t in range(args.nthread):
        thread_list.append(Consumer(t, args, conf))
    
    # start them up
    t = time.time()
    for th in thread_list:
         th.start()
    
    # wait for them to finish
    for th in thread_list:
         th.join()

    time_total = time.time() - t
    print('Run time %f' % time_total)

if __name__ == '__main__':
    main()

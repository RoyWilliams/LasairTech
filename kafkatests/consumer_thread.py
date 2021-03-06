# Multi threaded consuming of ZTF alerts

# conda config --add channels conda-forge
# conda install python-confluent-kafka
# conda install -c conda-forge python-avro
# conda install -c conda-forge fastavro

from confluent_kafka import Consumer, KafkaError
import threading, logging, time
import alertConsumer
import random
import time

###################################################
#kafka_server = 'public.alerts.ztf.uw.edu'
kafka_server = '192.41.108.22'
###################################################

def msg_text(message):
    """Remove postage stamp cutouts from an alert message.
    """
    message_text = {k: message[k] for k in message
                    if k not in ['cutoutDifference', 'cutoutTemplate', 'cutoutScience']}
    return message_text

class Consumer(threading.Thread):
    def __init__(self, threadID, nthread, topic, group_id):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.topic = topic
        self.group_id = group_id

    def run(self):

        schema_files = [
            "ztf-avro-alert/schema/candidate.avsc",
            "ztf-avro-alert/schema/cutout.avsc",
            "ztf-avro-alert/schema/prv_candidate.avsc",
            "ztf-avro-alert/schema/alert.avsc"]

        conf = {
            'bootstrap.servers': kafka_server + ':9092',
            'group.id': self.group_id,
            'default.topic.config': {'auto.offset.reset': 'smallest'}
        }

#        print(conf)
        print("Topic: %s, Thread: %s " %(self.topic, self.name))

        frombeginning = False
        streamReader = alertConsumer.AlertConsumer(self.topic, frombeginning, schema_files, **conf)
        streamReader.__enter__()

        if self.threadID == 0:
            print(streamReader.topics())

        ialert = 0
        bytes = 0
        t = time.time()
        while 1:
            try:
                msg = streamReader.poll(decode=True, timeout=40)
            except alertConsumer.EopError as e:
                print('got EopError')
                print(e)
                break

            if msg is None:
                print('null message received')
                break
            for alert in msg:
                data = msg_text(alert)
                ialert += 1
                if ialert%1000 == 0:
                    print('thread %s has %d in %f sec' % (self.name, ialert, (time.time()-t)))

        # looks like thats all the alerts we will get
        streamReader.__exit__(0,0,0)
        print("Exiting %s with %d events in %.1f seconds" % (self.name, ialert, (time.time()-t)))

################
import sys
if len(sys.argv) < 3:
    print('Usage: Consumer.py topic nthread')
    print('Example topic ztf_20190902_programid1')
    sys.exit()
else:
    topic = sys.argv[1]
    nthread = int(sys.argv[2])

# make the thread list
group_id = 'LASAIR-test%03d' % random.randrange(1000)

start = time.time()
thread_list = []
for t in range(nthread):
    thread_list.append(Consumer(t, nthread, topic, group_id))
    
# start them up
for th in thread_list:
     th.start()
    
# wait for them to finish
for th in thread_list:
     th.join()
print('======= %.1f seconds =========' % ((time.time()-start)))

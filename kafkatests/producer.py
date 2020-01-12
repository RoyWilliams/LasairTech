from confluent_kafka import Producer, KafkaError
import random
import time
import sys
import json

if len(sys.argv) < 4:
    print('Usage: Producer.py server:port topic nmessage')
    sys.exit()

kafka_server = sys.argv[1]
topic        = sys.argv[2]
nmessage     = int(sys.argv[3])
output = []
for i in range(nmessage):
    out = {'random': random.random() }
    output.append(out)

conf = { 'bootstrap.servers': kafka_server }
p = Producer(conf)

start = time.time()
for out in output:
    jsonout = json.dumps(out)
    p.produce(topic, jsonout)
p.flush()
print('======= %.1f seconds =========' % ((time.time()-start)))

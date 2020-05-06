import sys
from confluent_kafka import Consumer, KafkaError

if len(sys.argv) < 2:
    print('Usage: Consumer.py server:port <topic> ')
    sys.exit()
kafka_server = sys.argv[1]

group_id = 'LASAIR5'
conf = {
    'bootstrap.servers': kafka_server,
    'group.id': group_id,
    'default.topic.config': {'auto.offset.reset': 'smallest'}
}
streamReader = Consumer(conf)

if len(sys.argv) < 3:
    # the topics that this server has
    t = list(streamReader.list_topics().topics.keys())
    print('Topics are ', t)
else:
    # content of given topic
    topic = sys.argv[2]
    streamReader.subscribe([topic])
    while 1:
        msg = streamReader.poll(timeout=20)
        if msg == None: break
        print(msg.value())
streamReader.close()

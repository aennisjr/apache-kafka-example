## import the pykafka package
from pykafka import KafkaClient

## Use PyKafka's KafkaClient method to connect to the server that is currently running
client = KafkaClient(hosts='127.0.0.1:9092')

## Create a new topic
topic = client.topics['bigDataProject']

## Print out a list of topics that we have
print(client.topics)
print(topic)

## create a Producer for the topic and start producing messages
producer = topic.get_sync_producer()

## the actual message that gets passed to the producer
producer.produce('First Test Message'.encode('ascii'));
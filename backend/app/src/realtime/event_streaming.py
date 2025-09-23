import asyncio
import uuid

from confluent_kafka import Consumer, Producer

__producer_config = {
        # User-specific properties that you must set
        'bootstrap.servers': "localhost:9092",
}
__consumer_config = {
        'bootstrap.servers': 'localhost:9092',
        'group.id'         : f'fast-api-consumer-group-{uuid.uuid4()}',
        'auto.offset.reset': 'latest',
        "enable.auto.commit": True,
}

producer = Producer(__producer_config)
consumer = Consumer(__consumer_config)


class EventStream:

     __topic = 'chat-app'

     @staticmethod
     # Optional per-message delivery callback (triggered by poll() or flush())
     # when a message has been successfully delivered or permanently
     # failed delivery (after retries).
     def delivery_callback(err, msg):
          if err:
               print('ERROR: Message failed delivery: {}'.format(err))
          else:
               print("Success Sending data")

     @classmethod
     def produce_data(cls, data: dict):

          try:
               producer.produce(cls.__topic, data, str(uuid.uuid4()), callback=cls.delivery_callback)
               # Block until the messages are sent.
               producer.poll(1.0)
               producer.flush()

          except Exception as e:
               raise e

     @classmethod
     async def consume_data(cls):
          try:
               consumer.subscribe([cls.__topic])
               while True:
                    message = await asyncio.to_thread(consumer.poll, 1.0)
                    if message is None:
                         continue  # no message yet
                    if message.error():
                         continue
                    # decode the data
                    print(message.value().decode('utf-8'))
                    consumer.commit()

          except Exception as e:
               raise e
          finally:
               consumer.close()

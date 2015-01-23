import os
import pika
import time


class MQHandler:
    def __init__(self):
        self.connection = self._create_connection()
        self.channel = self.connection.channel()
        self._setup()
        return

    def close_connection(self):
        self.connection.close()

    def publish(self, exchange, routing_key, body, persistent=False):
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=body,
            properties=self._publishing_properties(persistent))

    def start_consuming(self, callback, queue, no_ack):
        self.channel.basic_consume(callback,
                                   queue=queue,
                                   no_ack=no_ack)
        self.channel.start_consuming()

    def ack(self, method):
        self.channel.basic_ack(delivery_tag=method.delivery_tag)

    def _create_connection(self):
        credentials = pika.PlainCredentials('guest', 'guest')
        connection_params = pika.ConnectionParameters(
            host=os.environ['RABBITMQ_PORT_5672_TCP_ADDR'],
            port=int(os.environ['RABBITMQ_PORT_5672_TCP_PORT']),
            credentials=credentials)
        # Sometimes RabbitMQ is still starting, so we might need to wait
        for _ in range(10):
            try:
                return pika.BlockingConnection(connection_params)
            except pika.exceptions.AMQPConnectionError:
                time.sleep(1)
        return pika.BlockingConnection(connection_params)

    def _setup(self):
        self.channel.exchange_declare(
            exchange='new_sentence', type='fanout', durable=True)
        self.channel.exchange_declare(
            exchange='storage', type='fanout', durable=True)
        self.channel.queue_declare(queue='translation', durable=True)
        self.channel.queue_declare(queue='storage', durable=True)
        self.channel.queue_declare(queue='logging')
        self.channel.queue_bind(exchange='new_sentence', queue='translation')
        self.channel.queue_bind(exchange='new_sentence', queue='storage')
        self.channel.queue_bind(exchange='new_sentence', queue='logging')
        self.channel.queue_bind(exchange='storage', queue='storage')
        self.channel.queue_bind(exchange='storage', queue='logging')

    def _publishing_properties(self, persistent):
        if persistent:
            return pika.BasicProperties(delivery_mode=2)
        else:
            return pika.BasicProperties()

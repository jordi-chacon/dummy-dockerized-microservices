import os
import pika
import time

class RabbitmqHandler:
    def __init__(self):
        self.connection = self._create_connection()
        self.channel = self.connection.channel()
        return

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

    def get_channel(self):
        return self.channel

    def close_connection(self):
        self.connection.close()

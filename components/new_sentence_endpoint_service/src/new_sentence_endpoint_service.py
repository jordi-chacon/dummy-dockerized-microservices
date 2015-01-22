import logging
import os
import pika
from flask import Flask, request, jsonify
from logging.handlers import RotatingFileHandler
from rabbitmq_handler import RabbitmqHandler

app = Flask(__name__)

def publish_to_mq(sender, message, language):
    rabbitmq_channel.basic_publish(exchange='',
                                   routing_key='hello',
                                   body='Hello World!')
    return

@app.route('/sentences', methods=['POST'])
def new_sentence():
    json=request.get_json()
    sender=json["sender"]
    message=json["sentence"]
    language=json["language"]
    publish_to_mq(sender, message, language)
    return jsonify({}), 201

if __name__ == "__main__":
    rabbitmq_handler = RabbitmqHandler()
    rabbitmq_channel = rabbitmq_handler.get_channel()
    rabbitmq_channel.queue_declare(queue='hello')
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(host="0.0.0.0", port=3000, debug=True)

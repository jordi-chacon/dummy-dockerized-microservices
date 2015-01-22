import logging
import pika
from flask import Flask, request, jsonify
from logging.handlers import RotatingFileHandler
from mq_handler import MQHandler
from sentence import Sentence

app = Flask(__name__)


@app.route('/sentences', methods=['POST'])
def new_sentence():
    sentence = parse_request_body()
    publish_sentence_to_mq(sentence)
    return jsonify({}), 201


def parse_request_body():
    json = request.get_json()
    sender = json["sender"]
    text = json["text"]
    language = json["language"]
    return Sentence(sender, text, language)


def publish_sentence_to_mq(sentence):
    mq_handler.publish('new_sentence', '', sentence.to_json(), True)


def publishing_properties_to_persist_messages():
    return pika.BasicProperties(delivery_mode=2)


if __name__ == "__main__":
    mq_handler = MQHandler()
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(host="0.0.0.0", port=3000, debug=True)

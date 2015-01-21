from flask import Flask, request, jsonify
import os
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

def publish_to_mq(sender, message, language):
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
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(host="0.0.0.0", port=3000, debug=True)

from flask import Flask
import os
import logging
from logging.handlers import RotatingFileHandler
app = Flask(__name__)

@app.route('/messages', methods=['POST'])
def hello():
    app.logger.info('Request received')
    return 'BURRU'

if __name__ == "__main__":
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(host="0.0.0.0", port=3000, debug=True)

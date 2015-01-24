import sys
sys.path.append('common/src')

import logging
import time
import uuid
from mq_handler import MQHandler
from sentence import Sentence
from store_handler import StoreHandler


def _consume_message(ch, method, properties, body):
    try:
        sentence = Sentence()
        sentence.from_json(body)
        _persist_sentence(sentence)
        mq_handler.ack(method)
    except Exception as e:
        logging.error(
            "Could not consume message: " + body + ".\nException:" + str(e))


def _persist_sentence(sentence):
    query = """INSERT INTO my_key_space.sentences
    (language, time, id, author, text) VALUES (%s,%s,%s,%s,%s)"""
    params = (sentence.get_language(),
              _timestamp(),
              uuid.uuid4(),
              sentence.get_author(),
              sentence.get_text())
    store_handler.execute_query(query, params)


def _timestamp():
    return int(time.time() * 1000)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    store_handler = StoreHandler()
    mq_handler = MQHandler()
    mq_handler.start_consuming(_consume_message, 'storage', False)

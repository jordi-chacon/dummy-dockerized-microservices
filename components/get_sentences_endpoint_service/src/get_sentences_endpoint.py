import sys
sys.path.append('common/src')

import logging
import json
from flask import Flask, request, Response
from logging.handlers import RotatingFileHandler
from store_handler import StoreHandler

app = Flask(__name__)


@app.route('/sentences', methods=['GET'])
def new_sentence():
    language = request.args.get('language')
    response = _get_response(language)
    return Response(json.dumps(response),  mimetype='application/json'), 200


def _get_response(language):
    query_result = store_handler.execute_query(_query(language))
    return map(_query_result_entry_to_json, query_result)


def _query(language):
    return """SELECT * FROM my_key_space.sentences
    WHERE language = '""" + language + "';"


def _query_result_entry_to_json(entry):
    return {"author": entry.author,
            "text": entry.text,
            "time": str(entry.time)}


if __name__ == "__main__":
    store_handler = StoreHandler(should_create_schema=False)
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(host="0.0.0.0", port=4000, debug=True)

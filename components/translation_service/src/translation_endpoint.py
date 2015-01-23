import sys
sys.path.append('common/src')

import logging
import os
from microsofttranslator import Translator
from mq_handler import MQHandler
from sentence import Sentence


def _consume_message(ch, method, properties, body):
    try:
        original_sentence = Sentence()
        original_sentence.from_json(body)
        _translate_to_all_languages(original_sentence)
        mq_handler.ack(method)
    except Exception as e:
        logging.error(
            "Could not consume message: " + body + ".\nException:" + str(e))


def _translate_to_all_languages(original_sentence):
    languages = ["en", "es", "sv"]
    languages.remove(original_sentence.get_language())
    for language in languages:
        _translate_to(original_sentence, language)


def _translate_to(original_sentence, to_language):
    translation = translator.translate(
        original_sentence.get_text(),
        to_language,
        original_sentence.get_language())
    translated_sentence = Sentence()
    translated_sentence.set_author(original_sentence.get_author())
    translated_sentence.set_language(to_language)
    translated_sentence.set_text(translation)
    mq_handler.publish('storage', '', translated_sentence.to_json(), True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    translator = Translator(
        os.environ['TRANSLATE_API_CLIENT_ID'],
        os.environ['TRANSLATE_API_SECRET'])
    mq_handler = MQHandler()
    mq_handler.start_consuming(_consume_message, 'translation', False)

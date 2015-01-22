import sys
sys.path.append('common/src')

import logging
from mq_handler import MQHandler


def _consume_message(ch, method, properties, body):
    logging.info(body)


def _format():
    return 'LOGGING SERVICE - %(asctime)s - Message consumed: %(message)s'


if __name__ == '__main__':
    mq_handler = MQHandler()
    logging.basicConfig(format=_format(), level=logging.DEBUG)
    mq_handler.start_consuming(_consume_message, 'logging', True)

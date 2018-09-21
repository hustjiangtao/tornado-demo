# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Common utils"""


import logging
import random
import string
import hmac
import hashlib
import traceback
try:
    import ujson as json
except ImportError:
    import json
    logging.warning(traceback.format_exc())
from json import JSONDecodeError

from datetime import datetime


class Json:
    """Json handle"""

    @staticmethod
    def json_decode(data):
        if not data:
            return None
        try:
            result = json.loads(data)
        except JSONDecodeError:
            result = None
            logging.warning(traceback.format_exc())

        return result

    @staticmethod
    def json_encode(data):
        if not data:
            return None
        try:
            result = json.dumps(data)
        except JSONDecodeError:
            result = None
            logging.warning(traceback.format_exc())

        return result


class String:
    """String service"""
    @staticmethod
    def random_string(string_length=10):
        """using cryptographic safety random functions"""
        # system_random = random.SystemRandom()
        if string_length < 36:
            return ''.join(random.sample(string.ascii_lowercase + string.digits, string_length))

        return ''.join([random.choice(string.ascii_lowercase + string.digits)
                        for x in range(string_length)])

    @staticmethod
    def get_hashed_password(password, salt):
        """Generate hashed password with a salt"""
        return hmac.new(bytes(salt.encode('utf-8')), password.encode('utf-8'),
                        hashlib.sha256).hexdigest()

    @staticmethod
    def compare_digest(a, b):
        """compare_digest(a, b) -> bool"""
        return hmac.compare_digest(a, b)


class BaseLogging:
    """Logging service"""
    logging.basicConfig(level=logging.INFO)

    @staticmethod
    def do_logging(data):
        logging.info(f'\U0001F44D {data} @ {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

    @staticmethod
    def do_warning(data):
        logging.warning(f'\U0001F602 {data} @ {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')


json_service = Json()
json_encode = json_service.json_encode
json_decode = json_service.json_decode

string_service = String()
random_string = string_service.random_string
get_hashed_password = string_service.get_hashed_password
compare_digest = string_service.compare_digest

logging_service = BaseLogging()
do_logging = logging_service.do_logging
do_warning = logging_service.do_warning

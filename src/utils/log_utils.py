import json
import logging
from os import environ
from dotenv import load_dotenv

class AppLog:

    def __init__(self):

        self.log_obj = logging.getLogger(environ.get('APP_NAME'))
        self.log_obj.setLevel(environ.get('LOG_LEVEL'))

        custom_format = '{'\
                            '"appname" : "%(name)s",'\
                            '"loglevel": "%(levelname)s",'\
                            '"message": "%(message)s"'\
                        '}'

        fh = logging.FileHandler(environ.get('LOG_FILE'))
        fh.setLevel(environ.get('LOG_LEVEL'))

        ch = logging.StreamHandler()
        ch.setLevel(environ.get('LOG_LEVEL'))

        #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        formatter = logging.Formatter(str(custom_format))
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        self.log_obj.addHandler(ch)
        self.log_obj.addHandler(fh)

    def info(self, msg):
        message = msg
        self.log_obj.info(message)

    def error(self, msg):
        message = msg
        self.log_obj.error(message)

    def debug(self, msg):
        message = msg
        self.log_obj.debug(message)

load_dotenv()

log = AppLog()
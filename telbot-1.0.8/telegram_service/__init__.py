# -*- coding: utf-8 -*-
try:  # pragma: no cover
    import ConfigParser
    configparser = ConfigParser
except ImportError:  # pragma: no cover
    import configparser
import logging

telegram_logger = None
token = None
upload_domain = None
host = None

def initialize(config_file):
    global token
    global upload_domain
    global host

    parser = configparser.RawConfigParser()
    parser.read(config_file)

    token = parser.get('tel-service','token')
    upload_domain = parser.get('tel-service','upload_domain')
    initialize_logging(parser.get('tel-service','log_file'))

def initialize_logging(log_file):
    global telegram_logger
    
    formatter = logging.Formatter("%(asctime)s [%(name)s] %(levelname)s: %(message)s")

    log_file_handler = logging.FileHandler(log_file)
    log_file_handler.setLevel(logging.DEBUG)
    log_file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    telegram_logger = logging.getLogger("telegram_service")
    telegram_logger.setLevel(logging.INFO)
    telegram_logger.addHandler(log_file_handler)
    telegram_logger.addHandler(console_handler)

# TODO: initialize move to bootstrap
initialize("./config/service.cfg")

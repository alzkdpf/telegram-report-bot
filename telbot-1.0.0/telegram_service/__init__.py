try:  # pragma: no cover
    import ConfigParser
    configparser = ConfigParser
except ImportError:  # pragma: no cover
    import configparser
import logging

telegram_logger = None
token = None

def initialize(config_file):
    global token
    parser = configparser.RawConfigParser()
    parser.read(config_file)

    initialize_logging(parser.get('tel-service','log_file'))
    token = parser.get('tel-service','token')

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

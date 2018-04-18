from telegram_service import telegram_logger
LOGGER = telegram_logger

from flask import Flask

try:
    app = Flask(__name__)
except (KeyboardInterrupt, SystemExit):
    raise

@app.route('/')
def index():
    LOGGER.info('run')
    return 'It works'

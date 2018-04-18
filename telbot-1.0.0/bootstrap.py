import sys, signal
sys.path.append('src/main/python')

from multiprocessing import Pool, Process
import threading

from telegram_service.app import app
from telegram_service import initialize
from telegram_service.telegramTask import TelegramTask


import logging

from telegram_service import telegram_logger
LOGGER = telegram_logger

def flaskStart():
    LOGGER.info('app run')
    # app.debug = True
    app.run(host='localhost',port=5001)

def telegramMonitor():
    LOGGER.info('task run')
    telegram_task = TelegramTask()
    telegram_task.run()

def taskRun():
    flask_task = Process(target=flaskStart)
    flask_task.start()
    telegram_task = Process(target=telegramMonitor)
    telegram_task.start()

def signal_handler(signal, frame):
    print('terminate service pressed Ctrl+C!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Service exit Ctrl+C press')
## your code
taskRun()

forever = threading.Event()
forever.wait()
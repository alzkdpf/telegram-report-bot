import os
import sys, signal
sys.path.append('src/main/python')

from multiprocessing import Pool, Process
import threading

## TODO: 디렉토리 확인 및 없을 경우 생성하기
os.system('mkdir -p ./log')
os.system('touch ./log/telegram_bot.log')

from telegram_service.telegramTask import TelegramTask
from telegram_service.app import app
from telegram_service import initialize

def flaskStart():
    print('app run')
    # app.debug = True
    app.run(host='localhost',port=5001)

def telegramMonitor():
    print('task run')
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

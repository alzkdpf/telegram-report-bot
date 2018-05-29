# -*- coding: utf-8 -*-
import os
import io
import json
import datetime

import threading

import telegram
from telegram.ext import CommandHandler, Updater
from telegram.error import NetworkError, Unauthorized
from time import sleep

import functools

from telegram_service import telegram_logger, token
LOGGER = telegram_logger
TOKEN = token

### exception Handler ####
def catch_exception(f):
    @functools.wraps(f)
    def func(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print ('Caught an exception in', f.__name__,e)
    return func

#### class def ####
class TelegramTask:
    def __init__(self):
        pass

    # task run
    @catch_exception
    def run(self):
        LOGGER.info("Run the bot. {0}".format(__name__))

        updater = Updater(TOKEN)

        dp = updater.dispatcher
        dp.add_handler(CommandHandler("help",self.__help))
        dp.add_handler(CommandHandler("subscribe", self.__subscribe,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
        dp.add_handler(CommandHandler("stop", self.__stop, pass_chat_data=True))                                          

        # log all errors
        dp.add_error_handler(self.__error)

        # Start the Bot
        updater.start_polling()

        # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
        # SIGABRT. This should be used most of the time, since start_polling() is
        # non-blocking and will stop the bot gracefully.
        updater.idle()        

    # save user_id when user's apply subscribe
    # 구독을 신청한 사용자 저장
    def __saveSubscribeUsers(self, chat_id):
        
        directory = self.__getRelativePath('./storage')

        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except:
            raise

        jsonData = {"id":chat_id}
        filename = '{}/{}.json'.format(directory,chat_id)
        with io.open(filename, 'w', encoding='utf-8') as f:
            f.write(json.dumps(jsonData, ensure_ascii=False))
    
    # return relative path 
    # 프로젝트 기준 상대경로 path 전달
    def __getRelativePath(self, path):
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        filePath = os.path.join(fileDir, path)
        return filePath

    # return date string
    # 날짜 표시
    def __getDate(self):
        today = datetime.date.today()
        return "{0}".format(datetime.datetime.now().strftime("%y-%m-%d %H:%M"))

    #### command ####
    def __error(self, bot, update, error):
        LOGGER.info("Log Errors caused by Updates.")
        LOGGER.warning('Update "%s" caused error "%s"', update, error)

    def __help(self, bot, update):
        LOGGER.info('help call')
        update.message.reply_text('The available commands are /help /subscribe /stop')

    def __subscribe(self, bot, update, args, job_queue, chat_data):
        chat_id = update.message.chat_id
        LOGGER.info('subscribe')

        # 메세지 데이터 => update
        # print(update)

        try:
            if args[0] == '2816':
                self.__saveSubscribeUsers(chat_id)
                update.message.reply_text('subscribe regist')
            else:
                update.message.reply_text('access denied')

        except (IndexError, ValueError):
            update.message.reply_text('Usage: /subscribe <your id>')

        except Exception as e:
            update.message.reply_text('exception {0}'.format(e))

    def __stop(self, bot, update, chat_data):
        LOGGER.info("Remove the job if the user changed their mind.")
        if 'job' not in chat_data:
            update.message.reply_text('You have no active timer')
            return
        job = chat_data['job']
        job.schedule_removal()
        del chat_data['job']

        update.message.reply_text('subscribe cancel~!! Thank you')

import os
import io
import json
import datetime

import telegram
from telegram.ext import CommandHandler, Updater
from telegram.error import NetworkError, Unauthorized
from time import sleep

import functools

from telegram_service import telegram_logger
LOGGER = telegram_logger

### exception Handler ####
def catch_exception(f):
    @functools.wraps(f)
    def func(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print ('Caught an exception in', f.__name__,e)
    return func

#### command ####
def error(bot, update, error):
    LOGGER.info("Log Errors caused by Updates.")
    LOGGER.warning('Update "%s" caused error "%s"', update, error)

def help(bot, update):
    LOGGER.info('help call')
    update.message.reply_text('The available commands are /help /subscribe /stop')

def notice(bot, job):
    bot.send_message(job.context, text='test!')
    # bot.send_document(fileName[0],doc)

def subscribe(bot, update, args, job_queue, chat_data):
    chat_id = update.message.chat_id
    LOGGER.info('subscribe')
    print(args)

    try:
        if args:
            LOGGER.info('argument Exception')
            raise ValueError

        #default second
        interval = int(args[0]) * 1 
        if interval < 0:
            update.message.reply_text('Interval is biggern than 0')
            return

        job = job_queue.run_repeating(notice, interval, context=chat_id)
        chat_data['job'] = job

        update.message.reply_text('subscribe regist')

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /subscribe <Interval>')

    except Exception as e:
        update.message.reply_text('exception {0}'.format(e))

def stop(bot, update, chat_data):
    LOGGER.info("Remove the job if the user changed their mind.")
    if 'job' not in chat_data:
        update.message.reply_text('You have no active timer')
        return
    job = chat_data['job']
    job.schedule_removal()
    del chat_data['job']

    update.message.reply_text('subscribe cancel~!! Thank you')

#### class def ####
class TelegramTask:
    def __init__(self):
        pass

    # task run
    @catch_exception
    def run(self):
        LOGGER.info("Run the bot. {0}".format(__name__))

        token = 'TOKEN'
        updater = Updater(token)

        dp = updater.dispatcher
        dp.add_handler(CommandHandler("help",help))
        dp.add_handler(CommandHandler("subscribe", subscribe,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
        dp.add_handler(CommandHandler("stop", stop, pass_chat_data=True))                                          

        # log all errors
        dp.add_error_handler(error)

        # Start the Bot
        updater.start_polling()

        # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
        # SIGABRT. This should be used most of the time, since start_polling() is
        # non-blocking and will stop the bot gracefully.
        updater.idle()        

    # save user_id when user's apply subscribe
    # 구독을 신청한 사용자 저장
    def saveSubscribeUsers(self, jsonData):
        jsonData = json.loads(jsonData)
        LOGGER.info(jsonData)
        id = jsonData.get('message_id',0)
        LOGGER.info('chat id :: {0}'.format(id))

        filename = self.getRelativePath('./storage/{0}.json'.format(jsonData['chat']['id']))
        with io.open(filename, 'w', encoding='utf-8') as f:
            f.write(json.dumps(jsonData, ensure_ascii=False))

        # self.fileTojson()
    
    # read directory to user lists & send document
    # 구독중인 사용자에 문서 발송
    def fileTojson(self, bot):
        filePath = self.getRelativePath('./storage')
        lists = os.listdir(filePath)
        LOGGER.info(lists)

        doc = self.getDocument()

        for fileName in lists:
            fileName = fileName.split('.')
            LOGGER.info('sendUser {0}'.format(fileName[0]))
            LOGGER.info('docPath {0}'.format(docPath))
            bot.send_document(fileName[0],doc)

    # return relative path 
    # 프로젝트 기준 상대경로 path 전달
    def getRelativePath(self, path):
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        filePath = os.path.join(fileDir, path)
        return filePath

    # return date string
    # 날짜 표시
    def getDate(self):
        today = datetime.date.today()
        return "{0}".format(datetime.datetime.now().strftime("%y-%m-%d %H:%M"))

    # return document path
    # 발송문서 가져오기
    def getDocument(self):
        ## your code
        docPath = self.getRelativePath('./notice/report.txt')
        doc = open(docPath,'rb')
        return doc
    
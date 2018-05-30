# -*- coding: utf-8 -*-
import os
from telegram_service import telegram_logger, token
from flask import Flask, request, redirect, url_for
from flask import send_from_directory
from werkzeug import secure_filename

from telegram import Bot

TOKEN = token
LOGGER = telegram_logger

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'apk'])

try:
    app = Flask(__name__, static_folder='static')

    # contents max size
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    # upload folder setting
    # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

except (KeyboardInterrupt, SystemExit):
    raise

@app.route('/')
def index():
    LOGGER.info('run')
    return 'It works'

@app.route('/up', methods=['GET','POST'])
def upload():
    if request.url_root != 'http://192.168.0.106'
        LOGGER.info('domain invalide')
        return

    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            LOGGER.info('secure filename : {}'.format(filename))
            # option 1. upload custom folder
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # option 2. static folder
            file.save(os.path.join(app.static_folder, filename))
            __sendFilelinkToUsers(request, filename)
            return redirect(url_for('upload',
                                    filename=filename))
    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
        </form>
    '''

# 다운로드 파일 링크
@app.route('/down/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(app.static_folder, filename=filename, as_attachment=True)

# 파일 유효성 확인 check file validation
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def __sendFilelinkToUsers(request,fileName):
    bot = Bot(TOKEN)
    bot.send_message
    __fileTojson(request, bot, fileName)

# read directory to user lists & send document
# 구독중인 사용자에 문서 발송
def __fileTojson(request, bot, storedFile):
    filePath = __getRelativePath('./storage')

    try:
        if not os.path.exists(filePath):
            LOGGER.info('create path')
            os.makedirs(filePath)
    except:
        LOGGER.info('occur exception')
        raise

    lists = os.listdir(filePath)
    LOGGER.info(lists)

    for fileName in lists:
        fileName = fileName.split('.')
        LOGGER.info('sendUser {0}'.format(fileName[0]))

        ## important : url do not use localhost
        download_link = '"{}down/{}"'.format(request.url_root, storedFile)
        bot.send_message(chat_id=fileName[0],
        text="<b>update new version</b> <a href="+download_link+">down</a>",
        parse_mode='HTML');


# return relative path 
# 프로젝트 기준 상대경로 path 전달
def __getRelativePath(path):
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    filePath = os.path.join(fileDir, path)
    return filePath


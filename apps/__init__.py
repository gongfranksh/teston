import logging
import os
import time

from logging.handlers import RotatingFileHandler

from flask import Flask, request

from flask_login import LoginManager

from apps.Js.JsApi.JsApi import jsapi
from apps.Utils.common import make_dir
from config import LOG_LEVEL

login_manager = LoginManager()


def create_app(config=None):

    setup_log(config)
    app = Flask(__name__)
    #app.config.from_object(config)
    if config is not None:
        app.config.from_pyfile(config)
    # send CORS headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        if request.method == 'OPTIONS':
            response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
            headers = request.headers.get('Access-Control-Request-Headers')
            if headers:
                response.headers['Access-Control-Allow-Headers'] = headers
                ##response.headers['Authorization'] = 'xiaominggessdfs3432ds34ds32432cedsad332e23'
        return response

    from apps.Auth.Users import db
    db.init_app(app)

    login_manager.session_protection = "strong"
    login_manager.init_app(app)

    from apps.Portal.Entrance import init_api
    init_api(app)

    #注册增加模块
    app.register_blueprint(jsapi)

    return app

def setup_log(config=None):
    """配置日志"""
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    log_dir_name = "logs"
    log_file_name = 'logger-' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log'
    log_file_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)) \
                      + os.sep \
                      + log_dir_name
    make_dir(log_file_folder)

    log_file_str = log_file_folder + os.sep + log_file_name
    logging.basicConfig(level=LOG_LEVEL)
    file_log_handler = RotatingFileHandler(log_file_str, maxBytes=1024 * 1024 * 100, backupCount=10)
    print(log_file_str)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(asctime)s - %(levelname)s -%(pathname)s- %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    # # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)




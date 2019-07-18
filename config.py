# service setting
import logging

HOST = "192.168.81.136"
PORT =3333
DEBUG = True
LOG_LEVEL = logging.DEBUG

# token setting
VERIFY_EXP_DAYS=300
SECRET_KEY = '123456'

# database setting
SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@192.168.168.169/logins'
SQLALCHEMY_TRACK_MODIFICATIONS = False

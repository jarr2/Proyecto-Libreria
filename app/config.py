import os

class DevelopmentConfig():
    SECRET_KEY = os.urandom(24)
    DEBUG = True
    MYSQL_DATABASE_USER = 'root'
    MYSQL_DATABASE_PASSWORD = 'root'
    MYSQL_DATABASE_HOST = '127.0.0.1'
    MYSQL_DATABASE_PORT = 3306
    MYSQL_DATABASE_DB = 'LibOnline'

config = {
    'development': DevelopmentConfig
    }
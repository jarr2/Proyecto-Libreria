import os

class DevelopmentConfig():
    SECRET_KEY = os.urandom(24)
    DEBUG = True
    MYSQL_DATABASE_USER = 'Admintez2025'
    MYSQL_DATABASE_PASSWORD = 'Admin-tez2025!'
    MYSQL_DATABASE_HOST = 'libreria.cr8vhihvbu0n.us-east-1.rds.amazonaws.com'
    MYSQL_DATABASE_PORT = 3306
    MYSQL_DATABASE_DB = 'LibOnline'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'comics.infinities@gmail.com'
    MAIL_PASSWORD = 'lsjc loqk wgof snco'

config = {
    'development': DevelopmentConfig
    }
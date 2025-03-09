import os

class DevelopmentConfig():
    SECRET_KEY = os.urandom(24)
    DEBUG = True
    MYSQL_DATABASE_USER = 'Admintez2025'
    MYSQL_DATABASE_PASSWORD = 'Admin-tez2025!'
    MYSQL_DATABASE_HOST = 'libreria.cr8vhihvbu0n.us-east-1.rds.amazonaws.com'
    MYSQL_DATABASE_PORT = 3306
    MYSQL_DATABASE_DB = 'LibOnline'

config = {
    'development': DevelopmentConfig
    }
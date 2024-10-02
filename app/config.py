import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = '<<your secret frase>>' #example: 'S#perS3crEt_007'
    SQLALCHEMY_DATABASE_URI = "postgresql://<<your username>>:<<your password>>@<<the adress or localhost>>:<<port>>/<<name of a database>>"  #example: 'postgresql://postgres:123456789@localhost/Notebook'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True 
    MAIL_USERNAME = '<<your google gmail>>'  #example: 'example@gmail.com'
    MAIL_PASSWORD = '<<your generated password for apps in your account>>' #example: 'pdzr stlo gwgf icub'
    MAIL_DEFAULT_SENDER = '<<your google gmail adress>>'  #example: 'example@gmail.com'
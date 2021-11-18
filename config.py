from os import environ, path

basedir = path.abspath(path.dirname(__file__))


class Config:
    SECRET_KEY = environ.get('SECRET_KEY') or 'nobody-gonna-guess-it'
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL') or 'sqlite:///' + path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

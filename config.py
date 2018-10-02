import string
import random
import os


def id_generator(size=15, chars=string.printable):
    return ''.join(random.choices(chars, k=size))

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or id_generator()
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'pool.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# -*- coding: utf-8 -*-
#########################################################

import os
from dotenv import load_dotenv
from pathlib import Path


class Config:
    """Configuraciones de Flask"""
    load_dotenv()
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)

    DEBUG = True if int(os.getenv('DEBUG')) else False
    if DEBUG:
        ENV = 'development'
        SQLALCHEMY_RECORD_QUERIES = True
    else:
        ENV = 'production'
        SQLALCHEMY_RECORD_QUERIES = False

    """Tamaño de las peticiones"""
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024

    """Configuraciones de SQLAlchemy - ORM Database"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_use_lifo": True,
        "pool_size": int(os.getenv("POOL_SIZE")),
        "pool_recycle": int(os.getenv("POOL_RECYCLE")),
        "pool_timeout": int(os.getenv("POOL_TIMEOUT")),
        "max_overflow": int(os.getenv("POOL_MAX_OVERFLOW"))
    }
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{pwd}@{host}:{port}/{db}?charset=utf8'.format(
        user=os.getenv('DB_USER'),
        pwd=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        db=os.getenv('DB_DATABASE')
    )

    ECHO = True
    PATH_DOCS = os.getenv('PATH_DOCS')
    EMAIL_DOCS = os.getenv('EMAIL_DOCS')
    EMAIL_KEY_DOCS = os.getenv('EMAIL_KEY_DOCS')
    EMAIL_PORT_DOCS = os.getenv('EMAIL_PORT_DOCS')
    EMAIL_SMTP_DOCS = os.getenv('EMAIL_SMTP_DOCS')

    HOST = os.getenv('HOST')
    PORT = os.getenv('PORT')

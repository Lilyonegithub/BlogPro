# -*- coding: utf-8 -*-
from .base import *  # NOQA

DEBUG = True

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'NAME': 'TestDemo',
        'USER': 'root',
        'PASSWORD': 'luling.com',
        'PORT': '3306',
    }
}
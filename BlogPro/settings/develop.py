# -*- coding: utf-8 -*-
from .base import *  # NOQA

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'NAME': 'BlogPro',
        'USER': 'root',
        'PASSWORD': 'luling.com',
        'PORT': '3306',
    }
}
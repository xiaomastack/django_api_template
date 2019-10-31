# -*- coding:utf-8 -*-
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, '../static/')

DEBUG = {{cookiecutter.debug}}

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '{{cookiecutter.mysql_db}}',
        'USER': '{{cookiecutter.mysql_user}}',
        'PASSWORD': '{{cookiecutter.mysql_password}}',
        'HOST': '{{cookiecutter.mysql_host}}',
        'PORT': '{{cookiecutter.mysql_port}}',
    }
}

# Local Cache
LOCAL_CACHE = {{cookiecutter.local_cache}}

#
TOKEN_EXPIRE_MINUTES = 60 * 24 * 30

CORS_ORIGIN_ALLOW_ALL = {{cookiecutter.cors}}
CORS_ALLOW_CREDENTIALS = {{cookiecutter.cors}}

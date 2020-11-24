from settings import *
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'musifetch_website',
        'USER': 'postgres',
        'PASSWORD': 'LezdSql39',
        'HOST': 'localhost',
        'PORT' : '5433',
    }
}
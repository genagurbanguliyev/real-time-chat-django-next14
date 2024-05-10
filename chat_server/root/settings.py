from pathlib import Path
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

from dotenv import load_dotenv
import os

load_dotenv()

# Your secret key
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
APPEND_SLASH = False

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
ALLOWED_HOSTS = ["*"]
CORS_ALLOW_HEADERS = ["*"]

# Application definition
INSTALLED_APPS = [
    "daphne",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # 3rd party
    'rest_framework',
    'channels',
    'corsheaders',

    # local
    'chatapp'
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'root.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(BASE_DIR.joinpath('templates'))],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ASGI_APPLICATION = "root.asgi.application"
WSGI_APPLICATION = 'root.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("DB_NAME"),
        'USER': os.environ.get("DB_USER"),
        'PASSWORD': os.environ.get("DB_PASSWORD"),
        'HOST': os.environ.get("DB_HOST"),
        'PORT': os.environ.get("DB_PORT"),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6378/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        }
    }
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6378)],
        },
    },
}

# REST_FRAMEWORK = {
#     'DEFAULT_RENDERER_CLASSES': [
#         'rest_framework.renderers.JSONRenderer',
#     ],
# }


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    # Filters:
    "filters": {
        "info_only": {
            "()":  "logger.logger_filters.InfoOnlyFilter"
        },
        "exclude_django_log": {
            "()":  "logger.logger_filters.ExcludeDjangoLogsFilter"
        }
    },

    # Formatters' profiles:
    "formatters": {
        "base": {
            "format": "[{asctime}][{levelname}][{name} / {funcName}][{lineno}] {message}",
            "datefmt": "%d/%m/%Y %H:%M:%S",
            "style": "{"
        },
        "info": {
            "format": "[{asctime}][{name} / {funcName}] {message}",
            "datefmt": "%d/%m/%Y %H:%M:%S",
            "style": "{"
        },
        "django_sys_format": {
            "format": "[{asctime}][{levelname} | {name}] {message}",
            "datefmt": "%d/%m/%Y %H:%M:%S",
            "style": "{"
        }
    },

    # handlers:
    "handlers": {
        "important_file": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "formatter": "base",
            "filename": BASE_DIR / "logger/logs/important.log"
        },
        "info_file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "formatter": "info",
            "filters": ["info_only"],
            "filename": BASE_DIR / "logger/logs/events_info.log",
        },

        "django_file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "formatter": "django_sys_format",
            "filename": BASE_DIR / "logger/logs/django_sys.log"
        }
    },


    # loggers:
    "loggers": {
        "django": {
            "handlers": ["django_file"],
            "level": "INFO",
        },

        "root": {
            "handlers": ["important_file", "info_file"],
            "level": "INFO",
            "filters": ["exclude_django_log"],
        },
    }
}

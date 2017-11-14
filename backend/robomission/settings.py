"""Django settings for robomission project.
"""

import os
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_DIR = os.path.dirname(BASE_DIR)
TASKS_DIR = os.path.join(REPO_DIR, 'tasks')
FRONTEND_DIR = os.path.join(REPO_DIR, 'frontend')
JS_NODE_PATH = os.path.join(FRONTEND_DIR, 'node_modules', '.bin', 'babel-node')
JS_TOOLS_DIR = os.path.join(FRONTEND_DIR, 'tools')

SHOW_SQL_QUERIES = os.getenv('SHOW_SQL_QUERIES', 'False') == 'True'


SECRET_KEY = 'q6!cfknp62=d71he3@&kv1)8b@lkfh0#6wo^gt18i5twx01r2%'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')
ALLOWED_HOSTS = ['.robomise.cz', '.localhost', '127.0.0.1', 'testserver']


ON_STAGING = os.getenv('ON_STAGING', "False") == "True"
ON_PRODUCTION = os.getenv('ON_AL', "False") == "True" and not ON_STAGING
DEVELOPMENT = not ON_STAGING and not ON_PRODUCTION
DEBUG = (not ON_PRODUCTION) or (os.getenv('DJANGO_DEBUG', "False") == "True")


# Application definition

INSTALLED_APPS = [
    'learn.apps.LearnConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    'lazysignup',
    'webpack_loader',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'robomission.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Frontend build directory contains template for index.html
        'DIRS': [os.path.join(FRONTEND_DIR, 'build')],
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

WSGI_APPLICATION = 'robomission.wsgi.application'


# Database

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///{path}'.format(path=os.path.join(BASE_DIR, 'db.sqlite3')))
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGES = [
    ('cs', 'Czech'),
    ('en', 'English')
]
LANGUAGE_CODE = 'cs'


# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    # Top-level public files (such as favicon.ico) are marked as static files
    # under `public` namespace (e.g. /static/public/favicon.ico).
    ('public', os.path.join(FRONTEND_DIR, 'build')),
    # Webpack-controlled files (js, css, images) are copied to /static directly.
    os.path.join(FRONTEND_DIR, 'build', 'static'),)
STATIC_ROOT = os.path.join(REPO_DIR, '..', 'static')


SERVER_DIR = os.path.join(REPO_DIR, '.server') if DEVELOPMENT else os.path.join(REPO_DIR, '..')
MEDIA_ROOT = os.path.join(SERVER_DIR, 'media')
EXPORTS_DIR = os.path.join(MEDIA_ROOT, 'exports')


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(REPO_DIR, 'logs', 'robomission.log'),
            'formatter': 'simple',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
    },
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s "%(message)s"'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'mail_admins', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG' if SHOW_SQL_QUERIES else 'INFO',
        },
        'robomission': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
}



REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        #'rest_framework.authentication.BasicAuthentication',
        # Currently, we use only SessionAuthentication using LazyUsers
        'rest_framework.authentication.SessionAuthentication',
    ),
}


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    #'social_core.backends.google.GoogleOAuth2',
    #'social_core.backends.facebook.FacebookOAuth2',
    'lazysignup.backends.LazySignupBackend',
)


# Setup CORS headers for development.
# This allows to run FE server on one port and sending request to BE server
# running on another port (so-called "cross-site requests").
#if DEVELOPMENT:
#    INSTALLED_APPS.append('corsheaders')
#    MIDDLEWARE.insert(0, 'corsheaders.middleware.CorsMiddleware')
#    CORS_ORIGIN_WHITELIST = (
#        'localhost:8000',
#        'localhost:3000',)

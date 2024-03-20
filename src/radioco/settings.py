# Radioco - Broadcasting Radio Recording Scheduling system.
# Copyright (C) 2014  Iago Veloso Abalo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SITE_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(h_$1pj(&usx%kw^m6$7*x9pnar+t_136g!3)g#+eje5r^3(!+'

DEBUG = True

# Application definition
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'grappelli',
    'filebrowser',

    'django.contrib.admin',
    'django.contrib.humanize',

    'ckeditor',
    'django_filters',
    'recurrence',
    'rest_framework',
    'rest_framework.authtoken',

    # Local Project Apps
    'radioco.api.apps.API',
    'radioco.users.apps.Users',
    'radioco.programmes.apps.Programmes',
    'radioco.schedules.apps.Schedules',
    'radioco.global_settings.apps.Global_Settings',
    'radioco.example',
)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (
            os.path.join(SITE_ROOT, 'templates'),),
        'OPTIONS': {
            'context_processors': (
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.tz'),
            'loaders': (
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader'),
        },
    },
]

ROOT_URLCONF = 'radioco.urls'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(SITE_ROOT, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

LOCALE_PATHS = (
    os.path.join(SITE_ROOT, 'locale'),
)

LOGIN_URL = 'admin:index'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'npm.finders.NpmFinder'
)

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Filebrowser
FILEBROWSER_URL_FILEBROWSER_MEDIA = STATIC_URL + "filebrowser/"
FILEBROWSER_PATH_FILEBROWSER_MEDIA = os.path.join(STATIC_URL, 'filebrowser/')
FILEBROWSER_VERSIONS = {
    'admin_thumbnail': {
        'verbose_name': 'Admin Thumbnail',
        'width': 60,
        'height': 60,
        'opts': 'crop'
    },
    'thumbnail': {
        'verbose_name': 'Thumbnail (1 col)',
        'width': 60,
        'height': 60,
        'opts': 'crop'
    },
    'small': {
        'verbose_name': 'Small (2 col)',
        'width': 140,
        'height': '',
        'opts': ''
    },
    'medium': {
        'verbose_name': 'Medium (4col )',
        'width': 300,
        'height': '',
        'opts': ''
    },
    'big': {
        'verbose_name': 'Big (6 col)',
        'width': 460,
        'height': '',
        'opts': ''
    },
    'large': {
        'verbose_name': 'Large (8 col)',
        'width': 680,
        'height': '',
        'opts': ''
    },
    'item_overlap': {
        'verbose_name': 'Big (6 col)',
        'width': 600,
        'height': 450,
        'opts': 'crop upscale'
    },
}
FILEBROWSER_ADMIN_VERSIONS = [
    'thumb', 'small', 'medium', 'large',
]

# RadioCo Settings
# http://django-radio.readthedocs.org/en/latest/reference/configuration.html

USERNAME_RADIOCO_RECORDER = 'RadioCo_Recorder'

# CKEditor
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_JQUERY_URL = '/'.join([STATIC_URL, 'jquery/dist/jquery.min.js'])

# Available Languages
PROGRAMME_LANGUAGES = (
    ('es', 'Spanish'),
    ('en', 'English'),
    ('gl', 'Galician'),
)

# Admin
GRAPPELLI_ADMIN_HEADLINE = 'RadioCo'
GRAPPELLI_ADMIN_TITLE = 'RadioCo'

# XXX needed for proper time handling on DST switches,
# e.g. datetime(2024, 3, 31, 2, 30, tzinfo=ZoneInfo(key='Europe/Berlin'))
USE_DEPRECATED_PYTZ = True

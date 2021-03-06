"""
Django settings for user_management project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'q6jd&si(ni8i$jypq3&_h4c!aycl2&wv^+h-%o5fv7j+lnr0pf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '*']


# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'userapp',
	'social_django',
	'attendanceapp',
	'payment_request_form',
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

ROOT_URLCONF = 'user_management.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': ['templates'],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
				'social_django.context_processors.backends',
				'social_django.context_processors.login_redirect',
			],

			'libraries':{
			'my_temp_tags': 'userapp.templatetags.my_temp_tags',

			}
		},
	},
]

WSGI_APPLICATION = 'user_management.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {

	# Local db connection
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'demo',
		'USER': 'root',
		'PASSWORD': '',
		'HOST': 'localhost',
		'PORT': '3306',
	}

	# Testing DB connection

	#  'default': {
	#     'ENGINE': 'django.db.backends.mysql',
	#     'NAME': 'usermntdbs',
	#     'USER': 'root',
	#     'PASSWORD': 'pcil@1234',
	#     'HOST': 'localhost',
	#     'PORT': '3306',
	# }
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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = (os.path.join(BASE_DIR, "sfiles"), )


MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_URL='login'
LOGIN_REDIRECT_URL = '/'


# EMAIL SETTINGS

EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_PASSWORD =  'applebanana1' #my gmail password
EMAIL_HOST_USER = 'mailmytemp1@gmail.com' #my gmail username
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# Gmail Login authentication #

AUTHENTICATION_BACKENDS = (
 'django.contrib.auth.backends.ModelBackend',   
 'social_core.backends.open_id.OpenIdAuth',  # for Google authentication
 'social_core.backends.google.GoogleOpenId',  # for Google authentication
 'social_core.backends.google.GoogleOAuth2',  # for Google authentication
)


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY ='429820649646-2gqsqp0mk5v42qg8d48digstp8dh8p45.apps.googleusercontent.com'  #Paste CLient Key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'I30bdK0MO1RhXJA9ydIwePzr' #Paste Secret Key


#To set up the whitelist of domains

SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = ['rentokil-pci.com','rentokil-initial.com']


#.......Social authentication error pages...............#
SOCIAL_AUTH_LOGIN_ERROR_URL = '/authentication_error/'
SOCIAL_AUTH_BACKEND_ERROR_URL = '/authentication_error/'


#.......Social auth pipeline for associating django user to google user.......#
SOCIAL_AUTH_PIPELINE = (
	'social_core.pipeline.social_auth.social_details',
	'social_core.pipeline.social_auth.social_uid',
	'social_core.pipeline.social_auth.auth_allowed',
	'social_core.pipeline.social_auth.social_user',
	'social_core.pipeline.social_auth.associate_by_email', # associate using email
	'social_core.pipeline.social_auth.associate_user',
	'social_core.pipeline.social_auth.load_extra_data',
	'social_core.pipeline.user.user_details',
	# 'userapp.views.get_user_email',
)

# LOGGER 
from .logger import LOGGING
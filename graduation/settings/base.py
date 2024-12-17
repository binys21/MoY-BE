from pathlib import Path
import os
from datetime import timedelta
import environ
import redis

import pymysql  
pymysql.install_as_MySQLdb()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

env = environ.Env(
    DEBUG=(bool, True)
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))



# AUTH_USER_MODEL = 'accounts.User'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

SECRET_KEY = env('DJANGO_SECRET_KEY')
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')

# Application definition



INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    
    # django-rest-framework
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',

    # django-allauth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_auth.registration',
    
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    
    # 추가한 앱 이름
    'accounts',
    'main',
    'home'
    
]
SITE_ID = 1

REST_FRAMEWORK = {
		# 'DATETIME_FORMAT': '%y-%m-%d %H:%M',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}
REST_USE_JWT = True
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=3),
    'ROTATE_REFRESH_TOKENS': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'TOKEN_USER_CLASS': 'accounts.User',
    'BLACKLIST_AFTER_ROTATION': True, 
}

MIDDLEWARE = [
	"corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "allauth.account.middleware.AccountMiddleware",
]

# cors 
CORS_ORIGIN_ALLOW_ALL=True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ( 
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]


ROOT_URLCONF = "graduation.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "graduation.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ko-KR'
# settings.py
AUTH_USER_MODEL = 'accounts.User'  # 커스텀 User 모델 지정

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

KAKAO_CLIENT_ID =  env('KAKAO_CLIENT_ID')
KAKAO_APP_ID =  env('KAKAO_APP_ID')
KAKAO_CLIENT_SECRET_KEY =  env('KAKAO_CLIENT_SECRET_KEY')
KAKAO_REDIRECT_URI = env('KAKAO_REDIRECT_URI')
KAKAO_USERNAME = env('KAKAO_USERNAME')
KAKAO_PASSWORD = env('KAKAO_PASSWORD')
AWS_S3_ACCESS_KEY_ID = env('AWS_S3_ACCESS_KEY_ID')
AWS_S3_SECRET_ACCESS_KEY = env('AWS_S3_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
REDIS_HOST = env('REDIS_HOST')
REDIS_PORT = env('REDIS_PORT')
NAVER_CLIENT_ID = env('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = env('NAVER_CLIENT_SECRET')
API_KEY = env('API_KEY') 
YOUTUBE_API_SERVICE_NAME = env('YOUTUBE_API_SERVICE_NAME')
YOUTUBE_API_VERSION = env('YOUTUBE_API_VERSION')

TMDB_API_KEY = env('TMDB_API_KEY')
CLOUDFRONT_URL = env('CLOUDFRONT_URL')
LASTFM_API_KEY=env('LASTFM_API_KEY')

SPOTIFY_CLIENT_ID=env('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET=env('SPOTIFY_CLIENT_SECRET')

redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

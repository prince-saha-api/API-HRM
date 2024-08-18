import environ
from pathlib import Path
from datetime import timedelta
from rest_framework.settings import api_settings

env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_DIR= BASE_DIR / 'media'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@m4a+&2hm8_%7yl!i)6y6or1!a^)n)z7cq7)&*-nw(8dd19*d7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',

    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'django_rest_passwordreset',

    'contribution.apps.ContributionConfig',
    'user.apps.UserConfig',
    'user_auth.apps.UserAuthConfig',
    'company.apps.CompanyConfig',
    'branch.apps.BranchConfig',
    'department.apps.DepartmentConfig',
    'facility.apps.FacilityConfig',
    'attendance.apps.AttendanceConfig',
    'hrm_settings.apps.HrmSettingsConfig',
    'device.apps.DeviceConfig',
    'leave.apps.LeaveConfig',
    'payroll.apps.PayrollConfig',
    'jobrecord.apps.JobrecordConfig',
    'notice.apps.NoticeConfig',
]

AUTH_USER_MODEL = 'user.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=2),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    "http://10.10.22.220:8080",
    "http://10.10.23.61:8080",
    'http://10.10.23.16:4000',
    'http://10.10.23.16:3004',
    'http://192.168.0.100:3004',
    'http://192.168.0.100:4000',
    'http://192.168.0.100:49012',
    'http://10.10.23.68:3000',
    'http://10.10.23.68:4000',
    'http://10.10.20.218:3000',
    'http://10.10.20.218:4000',
    'http://10.10.20.218:3004',
    'http://10.10.23.89:3004',
    'http://10.10.23.89:4000',
    'http://10.10.23.68:3004',
    'http://113.212.109.147:3000',
    'http://113.212.109.147:4000',
    'http://10.10.22.220:3004',
    'http://10.10.22.220:4000',
    'http://192.168.31.24:3004',
    'http://192.168.31.24:4000',
    'http://10.10.23.61:3004',
    'http://10.10.23.61:4000',
    'http://192.168.0.105:3004',
    'http://10.10.20.14:3004',
    'http://10.10.20.14:4000',
    'http://10.10.22.220:3004',
    'http://10.10.23.89:5000',
    'http://10.10.23.16:5000',
    'http://10.10.23.16:7000',
    'http://10.10.23.89:7000',
    'http://10.10.20.20:49012',
    'http://113.212.109.147:49012',
    'http://10.10.23.89:49012',
    'http://10.10.23.16:49012',
    'http://*',
]
 
CORS_ALLOW_HEADERS = ['*']

ROOT_URLCONF = 'hrm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'hrm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'apihrm',
#         'USER': 'postgres',
#         'PASSWORD': 'API#2024@ltd',
#         'HOST': '10.10.20.20',
#         'PORT': '5432',
#     }
# }


DATABASES = {
   'default': {
       'ENGINE': env('DATABASE_ENGI'),
       'NAME': env('DATABASE_NAME'),
       'USER': env('DATABASE_USER'),
       'PASSWORD': env('DATABASE_PASS'),
       'HOST': env('DATABASE_HOST'),
       'PORT': env('DATABASE_PORT'),
   }
}


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
# TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
MEDIA_ROOT = MEDIA_DIR
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

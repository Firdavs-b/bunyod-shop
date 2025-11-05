import os
from pathlib import Path
from dotenv import load_dotenv  # ⬅️ .env файлни автоматик ўқиш учун

# .env файлни юклаймиз
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# 🧩 Muhit (environment) маълумотлари
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# Apps
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Static файллар учун
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bunyod_shop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'bunyod_shop.wsgi.application'

# 🗄️ Database (Render учун Postgres ёки local учун sqlite)
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    import dj_database_url
    DATABASES = {'default': dj_database_url.parse(DATABASE_URL)}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# 🔐 Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 🌍 Language ва TimeZone
LANGUAGE_CODE = 'tg'
TIME_ZONE = os.getenv('TIME_ZONE', 'Asia/Dushanbe')
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('en', 'English'),
    ('ru', 'Russian'),
    ('tg', 'Tajik'),
]

LOCALE_PATHS = [BASE_DIR / 'locale']

# 🖼️ Static ва Media файллар
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# WhiteNoise кэш учун
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 🔑 Default primary key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 🎨 Jazzmin
JAZZMIN_SETTINGS = {
    "site_title": "МАГОЗАИ БУНЁД",
    "site_header": "Админ панел — Магозаи Бунёд",
    "site_brand": "МАГОЗАИ БУНЁД",
    "site_logo": "store/img/logo.png",
    "login_logo": "store/img/logo.png",
    "welcome_sign": "Салом, Бунёд!",
    "copyright": "© 2025 Магозаи Бунёд",
    "show_ui_builder": False,
    "theme": "cyborg",
}

JAZZMIN_UI_TWEAKS = {
    "theme": "cosmo",
    "navbar": "navbar-dark bg-dark",
    "sidebar": "sidebar-dark-primary",
    "brand_colour": "navbar-green",
    "accent": "accent-green",
    "dark_mode_theme": "slate",
}

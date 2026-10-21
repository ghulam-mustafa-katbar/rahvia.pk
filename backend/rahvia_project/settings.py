"""
Django settings for rahvia_project.
Pakistan Student Career-Guidance Platform (MVP to Scale).
"""

import os
from pathlib import Path
from datetime import timedelta
import dotenv

# Load environment variables
dotenv.load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-rahvia-career-guidance-pakistan-2026-production-ready-key')

DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 't')

# Host configuration: environment-driven with safe dev fallbacks
raw_allowed_hosts = os.getenv('ALLOWED_HOSTS', '')
if raw_allowed_hosts:
    ALLOWED_HOSTS = [h.strip() for h in raw_allowed_hosts.split(',') if h.strip()]
elif DEBUG:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

AUTH_USER_MODEL = 'authentication.User'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    
    # Local apps
    'authentication',
    'schools',
    'students',
    'assessments',
    'careers',
    'recommendations',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rahvia_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rahvia_project.wsgi.application'

# Database configuration
# 1. Direct PostgreSQL URL support (Render, Supabase, Neon, Railway)
# 2. Discrete PostgreSQL environment variables fallback (Docker, local setups)
# 3. SQLite fallback for local offline development
DATABASE_URL = os.getenv('DATABASE_URL', '').strip()

if DATABASE_URL:
    import urllib.parse
    parsed_db = urllib.parse.urlparse(DATABASE_URL)
    query_params = urllib.parse.parse_qs(parsed_db.query)
    
    db_config = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': parsed_db.path.lstrip('/'),
        'USER': urllib.parse.unquote(parsed_db.username or ''),
        'PASSWORD': urllib.parse.unquote(parsed_db.password or ''),
        'HOST': parsed_db.hostname or 'localhost',
        'PORT': str(parsed_db.port or 5432),
        'CONN_MAX_AGE': int(os.getenv('DB_CONN_MAX_AGE', 600)),
    }
    if 'sslmode' in query_params:
        db_config['OPTIONS'] = {'sslmode': query_params['sslmode'][0]}
    
    DATABASES = {'default': db_config}

elif os.getenv('USE_POSTGRES', 'False').lower() in ('true', '1', 'yes'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_DB', 'rahvia_db'),
            'USER': os.getenv('POSTGRES_USER', 'postgres'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'postgres'),
            'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
            'PORT': os.getenv('POSTGRES_PORT', '5432'),
            'CONN_MAX_AGE': int(os.getenv('DB_CONN_MAX_AGE', 600)),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password hashing: Bcrypt prioritized as mandated by security specification
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# SimpleJWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(os.getenv('JWT_ACCESS_LIFETIME_MINUTES', 60))),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=int(os.getenv('JWT_REFRESH_LIFETIME_DAYS', 7))),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# Caching & Redis
REDIS_URL = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/1')
if os.getenv('USE_REDIS', 'False').lower() in ('true', '1', 'yes'):
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': REDIS_URL,
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'rahvia-local-cache',
        }
    }

# CORS & Cross-Origin Configuration
raw_cors_origins = os.getenv('CORS_ALLOWED_ORIGINS', '').strip()
if raw_cors_origins:
    CORS_ALLOWED_ORIGINS = [o.strip() for o in raw_cors_origins.split(',') if o.strip()]
    CORS_ALLOW_ALL_ORIGINS = os.getenv('CORS_ALLOW_ALL_ORIGINS', 'False').lower() in ('true', '1')
elif DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOWED_ORIGINS = []
else:
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = []

CORS_ALLOW_CREDENTIALS = True

# CSRF Trusted Origins (Mandatory for Django 4.0+ Admin behind HTTPS reverse proxies)
raw_csrf_origins = os.getenv('CSRF_TRUSTED_ORIGINS', '').strip()
if raw_csrf_origins:
    CSRF_TRUSTED_ORIGINS = [o.strip() for o in raw_csrf_origins.split(',') if o.strip()]
elif CORS_ALLOWED_ORIGINS:
    CSRF_TRUSTED_ORIGINS = [o for o in CORS_ALLOWED_ORIGINS if o.startswith(('http://', 'https://'))]
else:
    CSRF_TRUSTED_ORIGINS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Karachi'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security & Reverse-Proxy Hardening Configuration
# Respect TLS headers from Render, Cloudflare, Vercel, AWS ELB, Nginx
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

if not DEBUG:
    # Explicitly toggleable via env to avoid 301 redirect loops during proxy health checks
    SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'False').lower() in ('true', '1')
    SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', 31536000))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
else:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True


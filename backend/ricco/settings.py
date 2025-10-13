import os
import dj_database_url
from pathlib import Path
from datetime import timedelta
from decouple import config  # ✅ Lee las variables del archivo .env

# === BASE_DIR: ruta base del proyecto ===
BASE_DIR = Path(__file__).resolve().parent.parent

# === DEBUG: True para desarrollo, False para producción ===
DEBUG = config('DEBUG', default=False, cast=bool)

# === SECRET_KEY: clave secreta del proyecto Django ===
SECRET_KEY = config('SECRET_KEY', default='insecure-dev-key')

# === CORS: Controla qué frontends pueden comunicarse con el backend ===
CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=False, cast=bool)
CORS_ALLOWED_ORIGINS = [
    'https://burgerstack-dqyj.onrender.com',
    'https://ricco-web-frontend.onrender.com',
]


# === ALLOWED_HOSTS: dominios permitidos para acceder al backend ===
if DEBUG:
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
    CSRF_TRUSTED_ORIGINS = ['http://localhost:4200'] #Origen Para peticiones desde Angular local
    CORS_ALLOWED_ORIGINS += ['http://localhost:4200'] #i en algún momento SE desactiva CORS_ALLOW_ALL_ORIGINS, estos son los permitidos
else:
    ALLOWED_HOSTS = ['ricco-backend.onrender.com']  # Dominio de producción
    CSRF_TRUSTED_ORIGINS = [
        'https://burgerstack-dqyj.onrender.com',
        'https://ricco-web-frontend.onrender.com',
    ]



CORS_ALLOW_CREDENTIALS = True  # Para sesiones, cookies, etc.

# === Apps instaladas ===
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Paquetes externos
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework.authtoken',
    'corsheaders',

    # Tu app principal
    'ricco_app',
]

# === Middlewares (procesadores que se ejecutan en cada petición HTTP) ===
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Sirve archivos estáticos
    'corsheaders.middleware.CorsMiddleware',  # Habilita CORS
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# === URLs y WSGI ===
ROOT_URLCONF = 'ricco.urls'
WSGI_APPLICATION = 'ricco.wsgi.application'

# === Templates (HTML renderizado por Django) ===
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

# === Base de datos ===
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'abm_ispc',
            'USER': 'root',
            'PASSWORD': '123456',
            'HOST': 'localhost',
            'PORT': '3306',
            'OPTIONS': {
                'sql_mode': 'traditional',
            }
        }
    }
else:
    DATABASES = {
        'default': dj_database_url.config(
            default=config('DATABASE_URL', default=''),  # ✅ Coma corregida
            conn_max_age=600
        )
    }

# === Validación de contraseñas ===
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# === Internacionalización ===
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# === Archivos estáticos ===
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'ricco', 'staticfiles')
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# === Modelo de usuario personalizado ===
AUTH_USER_MODEL = "ricco_app.CustomUser"

# === Autenticación ===
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# === Configuración del API REST ===
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

# === Configuración de JWT ===
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# === Headers permitidos por CORS ===
CORS_ALLOW_HEADERS = [
    'content-type',
    'authorization',
    'autentification',
    'x-requested-with',
    'x-csrftoken',
]

# === Métodos HTTP permitidos por CORS ===
CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
]

# === Token de prueba MercadoPago ===
MERCADOPAGO_ACCESS_TOKEN = config(
    "MERCADOPAGO_ACCESS_TOKEN",
    default="TEST-902554988203207-050217-2c7bab6c62f22c3d4f51093bf311b466-146277237"
)

# === Campo por defecto para modelos ===
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = ['ricco_app.backends.EmailBackend']

#===== CONFIGURACION CLOUDINARY====
import cloudinary
from decouple import config

cloudinary.config( 
  cloud_name = config('CLOUDINARY_CLOUD_NAME'), 
  api_key = config('CLOUDINARY_API_KEY'), 
  api_secret = config('CLOUDINARY_API_SECRET') 
)

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# from pathlib import Path
# from datetime import timedelta
# import dj_database_url
# import os


# # SECRET_KEY = 'django-insecure--$1@3$_!5!^g#-o#wt#2mh91%mm0e8a5#-4)oyja*jh&6$*^4+'
# SECRET_KEY = os.getenv('SECRET_KEY', 'insecure-dev-key')


# ALLOWED_HOSTS = ['ricco-backend.onrender.com']

# # Para entorno de desarrollo y producción
# DEBUG = os.getenv('DEBUG', 'False') == 'True'

# CORS_ALLOW_ALL_ORIGINS = os.getenv('CORS_ALLOW_ALL_ORIGINS', 'False') == 'True'
# print("CORS_ALLOW_ALL_ORIGINS:", CORS_ALLOW_ALL_ORIGINS)

# if not CORS_ALLOW_ALL_ORIGINS:
#     CORS_ALLOWED_ORIGINS = [
#         'https://ricco-web-frontend.onrender.com',
#     ]
    
# # Application definition
# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'rest_framework',
#     'rest_framework_simplejwt',
#     'rest_framework.authtoken',
#     'corsheaders',
#     'ricco_app',
# ]

# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'whitenoise.middleware.WhiteNoiseMiddleware',
#     'corsheaders.middleware.CorsMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# ROOT_URLCONF = 'ricco.urls'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = 'ricco.wsgi.application'

# BASE_DIR = Path(__file__).resolve().parent.parent


# if DEBUG:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.mysql',
#             'NAME': 'abm_ispc',
#             'USER': 'root',
#             'PASSWORD': '12345',
#             'HOST': 'localhost',  # o la IP si no está local
#             'PORT': '3306',
#             'OPTIONS': {
#             'sql_mode': 'traditional',
#         }
#         }
#     }
# else:
#     # Producción: usa DATABASE_URL con dj_database_url
#     DATABASES = {
#         'default': dj_database_url.config(
#             default=os.getenv('DATABASE_URL'),
#             conn_max_age=600
#         )
#     }
# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#         'OPTIONS': {
#             'min_length': 8,
#         }
#     },
#      {
#          'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#      },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]


# LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'

# USE_I18N = True

# USE_TZ = True

# STATIC_URL = 'static/'

# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# AUTH_USER_MODEL = "ricco_app.CustomUser"

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#         'rest_framework.authentication.BasicAuthentication',
#         'rest_framework.authentication.TokenAuthentication',
        
#     ),
#     'DEFAULT_PERMISSION_CLASSES': (
#     'rest_framework.permissions.IsAuthenticated',
# )
# }

# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
#     'ROTATE_REFRESH_TOKENS': True,
#     'BLACKLIST_AFTER_ROTATION': True,
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
#     'SIGNING_KEY': SECRET_KEY,
#     'AUTH_HEADER_TYPES': ('Bearer',),
# }

# CORS_ALLOW_CREDENTIALS = True

# CORS_ALLOW_HEADERS = [
#     'content-type',
#     'authorization',
#     'autentification',
#     'x-requested-with',

# ]

# CORS_ALLOW_METHODS = [
#     'GET',
#     'POST',
#     'PUT',
#     'PATCH',
#     'DELETE',
#     'OPTIONS'
# ]

# AUTHENTICATION_BACKENDS = [
#     'django.contrib.auth.backends.ModelBackend',
# ]

# # MEDIA_URL = '/media/'
# # MEDIA_ROOT = BASE_DIR / 'media' 
# MERCADOPAGO_ACCESS_TOKEN = os.getenv("MERCADOPAGO_ACCESS_TOKEN", "TEST-902554988203207-050217-2c7bab6c62f22c3d4f51093bf311b466-146277237")

# STATIC_ROOT = os.path.join(BASE_DIR, 'ricco', 'staticfiles')
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
# # STATICFILES_DIRS = [BASE_DIR / "static"]
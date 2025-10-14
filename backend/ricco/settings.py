# import os
# import dj_database_url
# from pathlib import Path
# from datetime import timedelta
# from decouple import config  # ✅ Lee las variables del archivo .env
# import cloudinary
# from corsheaders.defaults import default_headers


# # === BASE_DIR: ruta base del proyecto ===
# BASE_DIR = Path(__file__).resolve().parent.parent

# # === DEBUG: True para desarrollo, False para producción ===
# DEBUG = config('DEBUG', default=False, cast=bool)

# # === SECRET_KEY: clave secreta del proyecto Django ===
# SECRET_KEY = config('SECRET_KEY', default='insecure-dev-key')

# # === CORS: Controla qué frontends pueden comunicarse con el backend ===
# CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=False, cast=bool)
# CORS_ALLOWED_ORIGINS = [
#     'https://burgerstack-dqyj.onrender.com',
#     'https://ricco-web-frontend.onrender.com',
# ]


# # === ALLOWED_HOSTS: dominios permitidos para acceder al backend ===
# # if DEBUG:
# #     ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
# #     CSRF_TRUSTED_ORIGINS = ['http://localhost:4200'] #Origen Para peticiones desde Angular local
# #     CORS_ALLOWED_ORIGINS += ['http://localhost:4200'] #i en algún momento SE desactiva CORS_ALLOW_ALL_ORIGINS, estos son los permitidos
# # else:
# #     ALLOWED_HOSTS = ['ricco-backend.onrender.com']  # Dominio de producción
# #     CSRF_TRUSTED_ORIGINS = [
# #         'https://burgerstack-dqyj.onrender.com',
# #         'https://ricco-web-frontend.onrender.com',
# #     ]



# # CORS_ALLOW_CREDENTIALS = True  # Para sesiones, cookies, etc.

# if DEBUG:
#     ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
#     CSRF_TRUSTED_ORIGINS = ['http://localhost:4200']
#     CORS_ALLOWED_ORIGINS = ['http://localhost:4200']
#     CORS_ALLOW_ALL_ORIGINS = True  # Solo en desarrollo
#     CORS_ALLOW_CREDENTIALS = False  # No necesario en local si usás tokens
# else:
#     ALLOWED_HOSTS = ['ricco-backend.onrender.com']
#     CSRF_TRUSTED_ORIGINS = ['https://ricco-web-frontend.onrender.com']
#     CORS_ALLOWED_ORIGINS = ['https://ricco-web-frontend.onrender.com']
#     CORS_ALLOW_ALL_ORIGINS = False  # 🚫 Obligatorio para credenciales
#     CORS_ALLOW_CREDENTIALS = True   # ✅ Necesario para cookies/sesiones
    
    
# # === Apps instaladas ===
# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',

#     # Paquetes externos
#     'rest_framework',
#     'rest_framework_simplejwt',
#     'rest_framework.authtoken',
#     'corsheaders',

#     # Tu app principal
#     'ricco_app',
# ]

# # === Middlewares (procesadores que se ejecutan en cada petición HTTP) ===
# MIDDLEWARE = [
#     'corsheaders.middleware.CorsMiddleware',  # Habilita CORS
#     'django.middleware.security.SecurityMiddleware',
#     'whitenoise.middleware.WhiteNoiseMiddleware',  # Sirve archivos estáticos
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# # === URLs y WSGI ===
# ROOT_URLCONF = 'ricco.urls'
# WSGI_APPLICATION = 'ricco.wsgi.application'

# # === Templates (HTML renderizado por Django) ===
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

# # === Base de datos ===
# if DEBUG:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.mysql',
#             'NAME': 'abm_ispc',
#             'USER': 'root',
#             'PASSWORD': '12345',
#             'HOST': 'localhost',
#             'PORT': '3306',
#             'OPTIONS': {
#                 'sql_mode': 'traditional',
#             }
#         }
#     }
# else:
#     DATABASES = {
#         'default': dj_database_url.config(
#             default=config('DATABASE_URL', default=''),  # ✅ Coma corregida
#             conn_max_age=600
#         )
#     }

# # === Validación de contraseñas ===
# AUTH_PASSWORD_VALIDATORS = [
#     {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
#     {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
# ]

# # === Internacionalización ===
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
# USE_I18N = True
# USE_TZ = True

# # === Archivos estáticos ===
# STATIC_URL = 'static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'ricco', 'staticfiles')
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# # === Modelo de usuario personalizado ===
# AUTH_USER_MODEL = "ricco_app.CustomUser"

# # === Autenticación ===
# AUTHENTICATION_BACKENDS = [
#     'django.contrib.auth.backends.ModelBackend',
# ]

# # === Configuración del API REST ===
# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#         'rest_framework.authentication.BasicAuthentication',
#         'rest_framework.authentication.TokenAuthentication',
#     ),
#     'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.IsAuthenticated',
#     )
# }

# # === Configuración de JWT ===
# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
#     'ROTATE_REFRESH_TOKENS': True,
#     'BLACKLIST_AFTER_ROTATION': True,
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
#     'SIGNING_KEY': SECRET_KEY,
#     'AUTH_HEADER_TYPES': ('Bearer',),
# }

# # === Headers permitidos por CORS ===
# # CORS_ALLOW_HEADERS = [
# #     'content-type',
# #     'authorization',
# #     'autentification',
# #     'x-requested-with',
# #     'x-csrftoken',
# # ]

# CORS_ALLOW_HEADERS = list(default_headers) + [
#     'authorization',
#     'x-csrftoken',
# ]

# CORS_ORIGIN_WHITELIST = CORS_ALLOWED_ORIGINS

# # === Métodos HTTP permitidos por CORS ===
# CORS_ALLOW_METHODS = [
#     'GET',
#     'POST',
#     'PUT',
#     'PATCH',
#     'DELETE',
#     'OPTIONS',
# ]

# # === Token de prueba MercadoPago ===
# MERCADOPAGO_ACCESS_TOKEN = config(
#     "MERCADOPAGO_ACCESS_TOKEN",
#     default="TEST-902554988203207-050217-2c7bab6c62f22c3d4f51093bf311b466-146277237"
# )

# # === Campo por defecto para modelos ===
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# AUTHENTICATION_BACKENDS = ['ricco_app.backends.EmailBackend']

# #===== CONFIGURACION CLOUDINARY====

# cloudinary.config( 
#   cloud_name = config('CLOUDINARY_CLOUD_NAME'), 
#   api_key = config('CLOUDINARY_API_KEY'), 
#   api_secret = config('CLOUDINARY_API_SECRET') 
# )

# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

import os
from pathlib import Path
from datetime import timedelta
from decouple import config  # ✅ Para leer variables de entorno desde .env
import dj_database_url
import cloudinary
from corsheaders.defaults import default_headers

# === BASE_DIR: ruta base del proyecto ===
BASE_DIR = Path(__file__).resolve().parent.parent

# === DEBUG: True para desarrollo local, False para producción ===
DEBUG = config('DEBUG', default=False, cast=bool)

# === SECRET_KEY: clave secreta del proyecto ===
SECRET_KEY = config('SECRET_KEY', default='insecure-dev-key')

# =======================
# === CORS / ALLOWED HOSTS
# =======================
CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=False, cast=bool)

# Lista de frontends permitidos
CORS_ALLOWED_ORIGINS = [
    'https://burgerstack-dqyj.onrender.com',
    'https://ricco-web-frontend.onrender.com',
]

# Configuración de dominios permitidos y CSRF según entorno
if DEBUG:
    # Desarrollo local
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
    CSRF_TRUSTED_ORIGINS = ['http://localhost:4200']
    CORS_ALLOWED_ORIGINS = ['http://localhost:4200']
    CORS_ALLOW_ALL_ORIGINS = True  # Permite todas las peticiones en desarrollo
    CORS_ALLOW_CREDENTIALS = False
    # Cookies en HTTP local
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
else:
    # Producción en Render
    ALLOWED_HOSTS = ['ricco-backend.onrender.com']
    CSRF_TRUSTED_ORIGINS = ['https://ricco-web-frontend.onrender.com']
    CORS_ALLOWED_ORIGINS = ['https://ricco-web-frontend.onrender.com']
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOW_CREDENTIALS = True
    # Cookies seguras en HTTPS
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# =======================
# === INSTALLED APPS ===
# =======================
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

# =======================
# === MIDDLEWARES ===
# =======================
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# =======================
# === URLs y WSGI ===
# =======================
ROOT_URLCONF = 'ricco.urls'
WSGI_APPLICATION = 'ricco.wsgi.application'

# =======================
# === TEMPLATES ===
# =======================
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

# =======================
# === BASE DE DATOS ===
# =======================
# Lógica para soportar MySQL local y PostgreSQL en Render
DATABASE_URL = config('DATABASE_URL', default=None)

if DATABASE_URL:
    # Producción: usar PostgreSQL de Render
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=True  # obliga SSL en Render
        )
    }
else:
    # Desarrollo local: MySQL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'abm_ispc',      # Nombre de la DB local
            'USER': 'root',          # Usuario MySQL
            'PASSWORD': '12345',     # Contraseña local
            'HOST': 'localhost',
            'PORT': '3306',
            'OPTIONS': {
                'sql_mode': 'traditional',  # Compatible con Django
            }
        }
    }

# =======================
# === VALIDACIÓN DE CONTRASEÑAS ===
# =======================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =======================
# === INTERNACIONALIZACIÓN ===
# =======================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# =======================
# === ARCHIVOS ESTÁTICOS ===
# =======================
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'ricco', 'staticfiles')
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# =======================
# === MODELO DE USUARIO PERSONALIZADO ===
# =======================
AUTH_USER_MODEL = "ricco_app.CustomUser"

# =======================
# === AUTENTICACIÓN ===
# =======================
AUTHENTICATION_BACKENDS = [
    'ricco_app.backends.EmailBackend',  # Login por email
    'django.contrib.auth.backends.ModelBackend',
]

# =======================
# === REST FRAMEWORK ===
# =======================
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

# =======================
# === JWT CONFIG ===
# =======================
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# =======================
# === CORS CONFIG ===
# =======================
CORS_ALLOW_HEADERS = list(default_headers) + [
    'authorization',
    'x-csrftoken',
]
CORS_ORIGIN_WHITELIST = CORS_ALLOWED_ORIGINS
CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
]

# =======================
# === MERCADOPAGO (token de prueba) ===
# =======================
MERCADOPAGO_ACCESS_TOKEN = config(
    "MERCADOPAGO_ACCESS_TOKEN",
    default="TEST-902554988203207-050217-2c7bab6c62f22c3d4f51093bf311b466-146277237"
)

# =======================
# === DEFAULT AUTO FIELD ===
# =======================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =======================
# === CLOUDINARY CONFIG ===
# =======================
cloudinary.config(
    cloud_name=config('CLOUDINARY_CLOUD_NAME'),
    api_key=config('CLOUDINARY_API_KEY'),
    api_secret=config('CLOUDINARY_API_SECRET')
)
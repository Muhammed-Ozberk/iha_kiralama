"""
Django settings for hava_araci_uretim project.
Bu dosya, Django projesinin tüm yapılandırmalarını içerir.
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY: Proje için gizli anahtar. Django'nun güvenlik önlemleri için kullanılır.
SECRET_KEY = 'django-insecure-xh-f!x9c^p=&ulaz@y4+$^=y&3cg$=9^-t6&=5nf8qv+oq)cs&'

# DEBUG
DEBUG = True

# ALLOWED_HOSTS
ALLOWED_HOSTS = []

# INSTALLED_APPS: Django'yu çalıştıracak uygulamaların listesidir.
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "parts",  
    "aircrafts",  
    "accounts",   
    "rest_framework",   
    "drf_yasg",  # Swagger dökümantasyon desteği
    "ui",   
]

# MIDDLEWARE: Proje için kullanılan middleware'lerin sırasıdır.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "hava_araci_uretim.middleware.LoginRequiredMiddleware",  # LoginRequiredMiddleware'i burada tanımlandı
]

# Login ve Logout için yönlendirme ayarları
LOGIN_REDIRECT_URL = "/"  # Kullanıcı giriş yaptıktan sonra yönlendirileceği sayfa
LOGOUT_REDIRECT_URL = "/login/"  # Kullanıcı çıkış yaptıktan sonra yönlendirileceği sayfa

# ROOT_URLCONF: Proje için URL yönlendirme dosyasının yolu
ROOT_URLCONF = 'hava_araci_uretim.urls'

# TEMPLATES: Django'nun şablon sistemine ilişkin ayarlar
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

# WSGI application: WSGI üzerinden Django uygulamasının çalıştırılması için yapılandırma
WSGI_APPLICATION = 'hava_araci_uretim.wsgi.application'

# DATABASES: Veritabanı bağlantı bilgileri
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "iha",  # Veritabanı adı
        "USER": "postgres",  # Kullanıcı adı
        "PASSWORD": "password",  # Parola
        "HOST": "postgres",  # Docker Compose içindeki 'postgres' servisi
        "PORT": "5432",  # PostgreSQL için varsayılan port
    }
}

# AUTH_PASSWORD_VALIDATORS: Şifre doğrulama ayarları
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Dil ve Zaman Ayarları
LANGUAGE_CODE = 'en-us'  
TIME_ZONE = 'UTC'  
USE_I18N = True
USE_TZ = True

# Static files: CSS, JavaScript, görseller için genel ayarlar
STATIC_URL = 'static/'  

# Default primary key field type: Varsayılan otomatik anahtar türü
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

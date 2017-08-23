"""
Django settings for myblog project.

Generated by 'django-admin startproject' using Django 1.10.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import configparser


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# config settings
CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(BASE_DIR, 'config.ini'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = CONFIG.get('secret_key', 'secret_key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.writeathink.cn']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # self-add django apps
    'django.contrib.sites',
    'django.contrib.sitemaps',
    # third-party apps
    'taggit',  # 标签
    'haystack',  # 搜索
    'ckeditor',  # 富文本编辑器
    'ckeditor_uploader',
    'mptt',
    'crispy_forms',
    'allauth',  # allauth第三方登录
    'allauth.account',
    'allauth.socialaccount',
    # 下面是第三方账号相关的，比如我选了weibo和github
    'allauth.socialaccount.providers.weibo',
    'allauth.socialaccount.providers.github',

    # local apps
    'blog',
    'comments',

]

# django-allauth相关设置
AUTHENTICATION_BACKENDS = (
    # django admin所使用的用户登录与django-allauth无关
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# user,comemnt,post绑定
COMMENT_ENTRY_MODEL = 'blog.post'
AUTH_USER_MODEL = 'auth.user'

# haystack 配置
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr/blog',
        'TIMEOUT': 60 * 5,
        'INCLUDE_SPELLING': True,
    },

}

HAYSTACK_DJANGO_CT_FIELD = 'my_django_ct'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myblog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'myblog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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


# 前面我们app里添加了django.contrib.sites,需要设置SITE_ID
SITE_ID = 1

# method作用是当用户登录时，既可以使用用户名也可以使用email， 其他可选的值是 "username"、"email" ，
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True  # 要求用户注册时必须填写email，默认False，emial是选填的。
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login'
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN = 180
ACCOUNT_LOGOUT_ON_GET = True


# email settings
# SMTP服务器
EMAIL_HOST = CONFIG.get('email', 'host')
EMAIL_HOST_USER = CONFIG.get('email', 'host_user')
EMAIL_HOST_PASSWORD = CONFIG.get('email', 'host_passwd')
EMAIL_PORT = CONFIG.get('email', 'port')
# 是否使用了SSL 或者TLS
EMAIL_USE_SSL = True
# 默认发件人，不设置的话django默认使用的webmaster@localhost
DEFAULT_FROM_EMAIL = CONFIG.get('email', 'default_from_email')


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# ckeditor settings
# media settings
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
CKEDITOR_UPLOAD_PATH = 'upload/'
CKEDITOR_IMAGE_BACKEND = 'pillow'

CKEDITOR_ALLOW_NONIMAGE_FILES = False  # 不允许非图片文件上传，默认为True
CKEDITOR_BROWSE_SHOW_DIRS = True  # 在编辑器里浏览上传的图片时，图片会以路径分组，日期排序
CKEDITOR_RESTRICT_BY_DATE = True
# 限制用户浏览图片的权限，只能浏览自己上传的图片，图片会传到以用户名命名的文件夹下，超级管理员依旧可以看所有图片
CKEDITOR_RESTRICT_BY_USER = True

CKEDITOR_CONFIGS = {
    # 配置名是default时，django-ckeditor默认使用这个配置
    'default': {
        # 使用简体中文
        'language': 'zh-cn',
        # 编辑器的宽高请根据你的页面自行设置
        'width': '750px',
        'height': '500px',



        # 添加按钮在这里
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'basicstyles',
                'items': ['Bold', 'Italic', 'Underline', 'Strike']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote',
                       '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock']},
            {'name': 'links', 'items': [
                'Link', 'Unlink', 'Anchor', '-', 'RemoveFormat']},
            {'name': 'insert',
             'items': ['Image', '-', 'Flash', 'Iframe', '-', 'Table', 'CodeSnippet', 'Templates']},
            '/',
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'styles', 'items': ['Format', 'Font', 'FontSize']},
            {'name': 'special', 'items': ['Subscript', 'Superscript', '-', 'HorizontalRule',
                                          'SpecialChar', 'Smiley']},
            {'name': 'tools', 'items': [
                'Undo', 'Redo', '-', 'Source', 'Preview', 'Save', '-', 'Maximize']}
        ],
        'toolbar': 'YourCustomToolbarConfig',
        'image_previewText': ' ',
        'tabSpaces': 4,
        'extraPlugins': ','.join(
            [
                'div',
                'autolink',
                'autoembed',
                'embedsemantic',
                'autogrow',
                'widget',
                'lineutils',
                'clipboard',
                'dialog',
                'dialogui',
                'elementspath',
                'codesnippet',
                'uploadimage',
                'prism',
            ]),
    },

    'comment': {
        # 编辑器的宽高请根据你的页面自行设置
        'language': 'zh_cn',
        'width': '555px',
        'height': '150px',
        'image_previewText': ' ',
        'tabSpaces': 4,
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline', 'Format', 'RemoveFormat'],
            ['NumberedList', 'BulletedList'],
            ['Blockquote', 'CodeSnippet'],
            ['Image', 'Link', 'Unlink']
        ],
        'extraPlugins': ','.join(['codesnippet', 'uploadimage', 'prism', 'widget', 'lineutils', ]),
    }

}

# -*- coding: utf-8 -*-
# {{{ imports
from __future__ import unicode_literals

import os

from decimal import Decimal
from django.conf import global_settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _

from socket import gethostname
# }}}
# {{{ paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.path.pardir))

DATA_DIR = os.environ.get(
    'OPENSHIFT_DATA_DIR',
    os.path.join(
        PROJECT_ROOT,
        'data'
    )
)
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

LOG_DIR = os.environ.get(
    'OPENSHIFT_LOG_DIR',
    os.path.join(
        PROJECT_ROOT,
        'log'
    )
)
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

PUBLIC_DIR = os.path.join(
    os.environ.get(
        'OPENSHIFT_REPO_DIR',
        PROJECT_ROOT,
    ),
    'wsgi',
    'static',
)
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    ('bower_components', os.path.join(PROJECT_ROOT, 'bower_components')),
    ('node_modules', os.path.join(PROJECT_ROOT, 'node_modules')),
)
if DATA_DIR:
    MEDIA_ROOT = os.path.join(DATA_DIR, 'media')
    COMPRESS_ROOT = os.path.join(DATA_DIR, 'compress')

if PUBLIC_DIR:
    STATIC_ROOT = os.path.join(PUBLIC_DIR, 'collected')
# }}}
# {{{ secret
SECRET_FILE = os.path.join(DATA_DIR, 'secret.txt')
if not os.path.exists(SECRET_FILE):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    with open(SECRET_FILE, 'w+') as f:
        f.write(get_random_string(50, chars))

with open(SECRET_FILE, 'r') as f:
    SECRET_KEY = f.read()

if SECRET_KEY == 'notsecret' and not DEBUG:
    raise Exception('Please export DJANGO_SECRET_KEY or DEBUG')
# }}}
# {{{ django
#AUTH_USER_MODEL = 'email_auth.User'
DEBUG = os.environ.get('DJANGO_DEBUG', False)
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = [
    gethostname(),
]
DNS = os.environ.get('OPENSHIFT_APP_DNS', None),
if DNS:
    ALLOWED_HOSTS += DNS

if 'DJANGO_ALLOWED_HOSTS' in os.environ:
    ALLOWED_HOSTS += os.environ.get('DJANGO_ALLOWED_HOSTS').split(',')
ROOT_URLCONF = 'lpc.urls'
LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', "English"),
    ('fr', "French"),
)

PARLER_DEFAULT_LANGUAGE = 'en'

PARLER_LANGUAGES = {
    1: (
        {'code': 'fr'},
        {'code': 'en'},
    ),
    'default': {
        'fallbacks': ['fr', 'en'],
    },
}

CMS_LANGUAGES = {
    'default': {
        'fallbacks': ['en', 'fr'],
        'redirect_on_fallback': True,
        'public': True,
        'hide_untranslated': False,
    },
    1: ({
        'public': True,
        'code': 'en',
        'hide_untranslated': False,
        'name': 'English',
        'redirect_on_fallback': True,
    }, {
        'public': True,
        'code': 'fr',
        'hide_untranslated': False,
        'name': 'Deutsch',
        'redirect_on_fallback': True,
    },)
}
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
MEDIA_URL = '/static/media/'
STATIC_URL = '/static/collected/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
    'compressor.finders.CompressorFinder',
)
WSGI_APPLICATION = 'lpc.wsgi.application'
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_SAVE_EVERY_REQUEST = True
SITE_ID = True
SILENCED_SYSTEM_CHECKS = ('auth.W004', 'auth.E003')
# }}}
# {{{ images

FILER_ADMIN_ICON_SIZES = ('16', '32', '48', '80', '128')

FILER_ALLOW_REGULAR_USERS_TO_ADD_ROOT_FOLDERS = True

FILER_DUMP_PAYLOAD = False

FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880

THUMBNAIL_HIGH_RESOLUTION = False

THUMBNAIL_OPTIMIZE_COMMAND = {
    'gif': '/usr/bin/optipng {filename}',
    'jpeg': '/usr/bin/jpegoptim {filename}',
    'png': '/usr/bin/optipng {filename}'
}

THUMBNAIL_PRESERVE_EXTENSIONS = True

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)
# }}}
# {{{ cms

CMS_TEMPLATES = (
    ('lpcshop/pages/default.html', _("Default Page")),
)

CMS_CACHE_DURATIONS = {
    'content': 600,
    'menus': 3600,
    'permissions': 86400,
}

CMS_PERMISSION = False

CACSCADE_WORKAREA_GLOSSARY = {
    'breakpoints': ['xs', 'sm', 'md', 'lg'],
    'container_max_widths': {'xs': 750, 'sm': 750, 'md': 970, 'lg': 1170},
    'fluid': False,
    'media_queries': {
        'xs': ['(max-width: 768px)'],
        'sm': ['(min-width: 768px)', '(max-width: 992px)'],
        'md': ['(min-width: 992px)', '(max-width: 1200px)'],
        'lg': ['(min-width: 1200px)'],
    },
}

CMS_PLACEHOLDER_CONF = {
    'Breadcrumb': {
        'plugins': ['BreadcrumbPlugin'],
        'glossary': CACSCADE_WORKAREA_GLOSSARY,
    },
    'Commodity Details': {
        'plugins': ['BootstrapRowPlugin', 'TextPlugin', 'ImagePlugin', 'PicturePlugin'],
        'text_only_plugins': ['TextLinkPlugin'],
        'parent_classes': {'BootstrapRowPlugin': []},
        'require_parent': False,
        'glossary': CACSCADE_WORKAREA_GLOSSARY,
    },
}


CMSPLUGIN_CASCADE_PLUGINS = ('cmsplugin_cascade.segmentation', 'cmsplugin_cascade.generic',
    'cmsplugin_cascade.link', 'shop.cascade', 'cmsplugin_cascade.bootstrap3',)

CMSPLUGIN_CASCADE = {
    'dependencies': {
        'shop/js/admin/shoplinkplugin.js': 'cascade/js/admin/linkpluginbase.js',
    },
    'alien_plugins': ('TextPlugin', 'TextLinkPlugin',),
    'bootstrap3': {
        'template_basedir': 'angular-ui',
    },
    'plugins_with_extra_fields': (
        'BootstrapButtonPlugin',
        'BootstrapRowPlugin',
        'SimpleWrapperPlugin',
        'HorizontalRulePlugin',
        'ExtraAnnotationFormPlugin',
        'ShopProceedButton',
    ),
    'segmentation_mixins': (
        ('shop.cascade.segmentation.EmulateCustomerModelMixin', 'shop.cascade.segmentation.EmulateCustomerAdminMixin'),
    ),
}

CMSPLUGIN_CASCADE_LINKPLUGIN_CLASSES = (
    'shop.cascade.plugin_base.CatalogLinkPluginBase',
    'cmsplugin_cascade.link.plugin_base.LinkElementMixin',
    'shop.cascade.plugin_base.CatalogLinkForm',
)

CKEDITOR_SETTINGS = {
    'language': '{{ language }}',
    'skin': 'moono',
    'toolbar': 'CMS',
    'toolbar_HTMLField': [
        ['Undo', 'Redo'],
        ['cmsplugins', '-', 'ShowBlocks'],
        ['Format', 'Styles'],
        ['TextColor', 'BGColor', '-', 'PasteText', 'PasteFromWord'],
        ['Maximize', ''],
        '/',
        ['Bold', 'Italic', 'Underline', '-', 'Subscript', 'Superscript', '-', 'RemoveFormat'],
        ['JustifyLeft', 'JustifyCenter', 'JustifyRight'],
        ['HorizontalRule'],
        ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Table'],
        ['Source']
    ],
}

SELECT2_CSS = 'bower_components/select2/dist/css/select2.min.css'
SELECT2_JS = 'bower_components/select2/dist/js/select2.min.js'
# }}}
# {{{ apps
SHOP_APP_LABEL = 'lpcshop'
NODE_MODULES_URL = STATIC_URL + 'node_modules/'
SASS_PROCESSOR_INCLUDE_DIRS = (
    os.path.join(PROJECT_ROOT, 'node_modules'),
)
COERCE_DECIMAL_TO_STRING = True
FSM_ADMIN_FORCE_PERMIT = True
ROBOTS_META_TAGS = ('noindex', 'nofollow')
# }}}
# {{{ installed apps
INSTALLED_APPS = (
    'django.contrib.auth',
    #'email_auth',
    'django.contrib.admin',
    'polymorphic',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djangocms_text_ckeditor',
    'django_select2',
    'cmsplugin_cascade',
    'cmsplugin_cascade.clipboard',
    'cmsplugin_cascade.sharable',
    'cmsplugin_cascade.extra_fields',
    'cmsplugin_cascade.segmentation',
    'cms_bootstrap3',
    'adminsortable2',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'django_fsm',
    'fsm_admin',
    'djng',
    'cms',
    'menus',
    'treebeard',
    'compressor',
    'sekizai',
    'sass_processor',
    'django_filters',
    'filer',
    'easy_thumbnails',
    'easy_thumbnails.optimize',
    'parler',
    'post_office',
    'shop',
    'shop_stripe',
    'lpcshop',
)

if DEBUG:
    try:
        import debug_toolbar  # noqa
    except:
        pass
    else:
        INSTALLED_APPS += ('debug_toolbar',)
# }}}
# {{{ middleware
MIDDLEWARE_CLASSES = (
    'djng.middleware.AngularUrlMiddleware',
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'shop.middleware.CustomerMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
)
# }}}
# {{{ templates
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'APP_DIRS': True,
    'DIRS': [],
    'OPTIONS': {
        'context_processors': (
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.debug',
            'django.template.context_processors.i18n',
            'django.template.context_processors.media',
            'django.template.context_processors.static',
            'django.template.context_processors.tz',
            'django.template.context_processors.csrf',
            'django.template.context_processors.request',
            'django.contrib.messages.context_processors.messages',
            'sekizai.context_processors.sekizai',
            'cms.context_processors.cms_settings',
            'shop.context_processors.customer',
            'shop.context_processors.version',
            'shop_stripe.context_processors.public_keys',
        )
    }
}]
# }}}
# {{{ database
DATABASES = {
    'default': {
        'NAME': os.environ.get('DJANGO_DATABASE_DEFAULT_NAME', 'db.sqlite'),
        'USER': os.environ.get('DJANGO_DATABASE_DEFAULT_USER', ''),
        'PASSWORD': os.environ.get('DJANGO_DATABASE_DEFAULT_PASSWORD', ''),
        'HOST': os.environ.get('DJANGO_DATABASE_DEFAULT_HOST', ''),
        'PORT': os.environ.get('DJANGO_DATABASE_DEFAULT_PORT', ''),
        'ENGINE': os.environ.get('DJANGO_DATABASE_DEFAULT_ENGINE',
                                 'django.db.backends.sqlite3'),

    }
}

if 'OPENSHIFT_DATA_DIR' in os.environ:
    DATABASES['default']['NAME'] = os.path.join(DATA_DIR, 'db.sqlite')

if 'OPENSHIFT_POSTGRESQL_DB_HOST' in os.environ:
    DATABASES['default']['NAME'] = os.environ['OPENSHIFT_APP_NAME']
    DATABASES['default']['USER'] = os.environ[
        'OPENSHIFT_POSTGRESQL_DB_USERNAME']
    DATABASES['default']['PASSWORD'] = os.environ[
        'OPENSHIFT_POSTGRESQL_DB_PASSWORD']
    DATABASES['default']['HOST'] = os.environ['OPENSHIFT_POSTGRESQL_DB_HOST']
    DATABASES['default']['PORT'] = os.environ['OPENSHIFT_POSTGRESQL_DB_PORT']
    DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'
# }}}
# {{{ email
EMAIL_HOST = 'smtp.example.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'no-reply@example.com'
EMAIL_HOST_PASSWORD = 'smtp-secret-password'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'My Shop <no-reply@example.com>'
EMAIL_REPLY_TO = 'info@example.com'
EMAIL_BACKEND = 'post_office.EmailBackend'
# }}}
# {{{ shop
SHOP_VALUE_ADDED_TAX = Decimal(19)
SHOP_DEFAULT_CURRENCY = 'EUR'
SHOP_CART_MODIFIERS = (
    'shop.modifiers.defaults.DefaultCartModifier',
    'shop.modifiers.taxes.CartExcludedTaxModifier',
    'lpcshop.modifiers.PostalShippingModifier',
    'lpcshop.modifiers.CustomerPickupModifier',
    'lpcshop.modifiers.StripePaymentModifier',
    'shop.modifiers.defaults.PayInAdvanceModifier',
)
SHOP_EDITCART_NG_MODEL_OPTIONS = "{updateOn: 'default blur', debounce: {'default': 2500, 'blur': 0}}"

SHOP_ORDER_WORKFLOWS = (
    'shop.payment.defaults.PayInAdvanceWorkflowMixin',
    'shop.shipping.delivery.PartialDeliveryWorkflowMixin',
    'shop_stripe.payment.OrderWorkflowMixin',
)

SHOP_STRIPE = {
    'PUBKEY': 'pk_test_stripe_secret',
    'APIKEY': 'sk_test_stripe_secret',
    'PURCHASE_DESCRIPTION': _("Thanks for purchasing at Libertalia Pirate Community"),
}
# }}}
# {{{ restframework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'shop.rest.money.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',  # can be disabled for production environments
    ),
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #   'rest_framework.authentication.TokenAuthentication',
    # ),
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 12,
}

SERIALIZATION_MODULES = {'json': str('shop.money.serializers')}
# }}}
# {{{ logging
LOG_LEVEL = os.environ.get('DJANGO_LOG_LEVEL', 'DEBUG' if DEBUG else 'INFO')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s[%(module)s]: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'post_office': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}

if DEBUG:
    LOGGING['handlers']['debug'] = {
        'level': 'DEBUG',
        'class': 'logging.FileHandler',
        'filename': os.path.join(LOG_DIR, 'debug.log'),
    }

    for logger in LOGGING['loggers'].values():
        logger['handlers'].append('debug')

RAVEN_FILE = os.path.join(DATA_DIR, 'sentry')
if os.path.exists(RAVEN_FILE):
    INSTALLED_APPS += ('raven.contrib.django.raven_compat',)

    LOGGING['handlers']['sentry'] = {
        'level': 'INFO',
        'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
    }
    LOGGING['loggers']['sentry.errors'] = LOGGING['loggers']['raven'] = {
        'level': 'INFO',
        'handlers': ['console'],
        'propagate': False,
    }

    with open(RAVEN_FILE, 'r') as f:
        RAVEN_CONFIG = {
            'dsn': f.read().strip()
        }
# }}}

"""Main settings."""
import os
import sys
from pathlib import Path

from django.utils.translation import ugettext_lazy as _


######################
# MEZZANINE SETTINGS #
######################

# The following settings are already defined with default values in
# the ``defaults.py`` module within each of Mezzanine's apps, but are
# common enough to be put here, commented out, for conveniently
# overriding. Please consult the settings documentation for a full list
# of settings Mezzanine implements:
# http://mezzanine.jupo.org/docs/configuration.html#default-settings

# Controls the ordering and grouping of the admin menu.
#
# ADMIN_MENU_ORDER = (
#     ("Content", ("pages.Page", "blog.BlogPost",
#        "generic.ThreadedComment", (_("Media Library"), "media-library"),)),
#     ("Site", ("sites.Site", "redirects.Redirect", "conf.Setting")),
#     ("Users", ("auth.User", "auth.Group",)),
# )

ADMIN_MENU_ORDER = (
    ("Carcerópolis Admin", (
        ("Áreas de Atuação", "caceropolis.AreaDeAtuacao"),
        ("Especialidades", "caceropolis.Especialidade"),
        ("Unidades Prisionais", "carceropolis.UnidadePrisional"),
        ("Logs", "django.contrib.admin.models.LogEntry"),
    )),
    ("Carcerópolis", (
        ("Especialistas", "caceropolis.Especialista"),
        ("Publicações", "caceropolis.Publicacao"),
    )),
    ("Conteúdos", (
        ("Páginas", "pages.Page"),
        ("Comentários", "generic.ThreadedComment"),
        ("Conteúdo de Mídia", "media-library"),
    )),
    ("Usuários", (
        ("Usuários", "auth.User"),
        ("Grupos", "auth.Group"),
    )),
    ("Sites", (
        ("Site", "sites.Site"),
        ("Redirecionamento", "redirects.Redirect"),
        ("Configurações", "conf.Setting"),
    )),
)

ADMIN_REMOVAL = ["django.contrib.sites.models.Site"]

ACCOUNTS_APPROVAL_REQUIRED = False

ACCOUNTS_VERIFICATION_REQUIRED = True

PUBLICACAO_PER_PAGE = 9

MUNICIPIOS_GEO = False

# A three item sequence, each containing a sequence of template tags
# used to render the admin dashboard.
#
# DASHBOARD_TAGS = (
#     ("blog_tags.quick_blog", "mezzanine_tags.app_list"),
#     ("comment_tags.recent_comments",),
#     ("mezzanine_tags.recent_actions",),
# )

# A sequence of templates used by the ``page_menu`` template tag. Each
# item in the sequence is a three item sequence, containing a unique ID
# for the template, a label for the template, and the template path.
# These templates are then available for selection when editing which
# menus a page should appear in. Note that if a menu template is used
# that doesn't appear in this setting, all pages will appear in it.

# PAGE_MENU_TEMPLATES = (
#     (1, _("Top navigation bar"), "pages/menus/dropdown.html"),
#     (2, _("Left-hand tree"), "pages/menus/tree.html"),
#     (3, _("Footer"), "pages/menus/footer.html"),
# )

# A sequence of fields that will be injected into Mezzanine's (or any
# library's) models. Each item in the sequence is a four item sequence.
# The first two items are the dotted path to the model and its field
# name to be added, and the dotted path to the field class to use for
# the field. The third and fourth items are a sequence of positional
# args and a dictionary of keyword args, to use when creating the
# field instance. When specifying the field class, the path
# ``django.models.db.`` can be omitted for regular Django model fields.
#
# EXTRA_MODEL_FIELDS = (
#     (
#         # Dotted path to field.
#         "mezzanine.blog.models.BlogPost.image",
#         # Dotted path to field class.
#         "somelib.fields.ImageField",
#         # Positional args for field class.
#         (_("Image"),),
#         # Keyword args for field class.
#         {"blank": True, "upload_to": "blog"},
#     ),
#     # Example of adding a field to *all* of Mezzanine's content types:
#     (
#         "mezzanine.pages.models.Page.another_field",
#         "IntegerField", # 'django.db.models.' is implied if path is omitted.
#         (_("Another name"),),
#         {"blank": True, "default": 1},
#     ),
# )

# Setting to turn on featured images for blog posts. Defaults to False.
#
# BLOG_USE_FEATURED_IMAGE = True

# If True, the django-modeltranslation will be added to the
# INSTALLED_APPS setting.
USE_MODELTRANSLATION = True

########################
# MAIN DJANGO SETTINGS #
########################

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "dev.carceropolis.org.br",
                 "carceropolis.org.br", "www.carceropolis.org.br"]

if os.getenv("IS_PRODUCTION"):
    ALLOWED_HOSTS.insert(0, "carceropolis.org.br")
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "America/Sao_Paulo"

# If you set this to True, Django will use timezone-aware datetimes.
USE_TZ = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pt-br'

# Supported languages
LANGUAGES = (
    ('pt-br', _('Portuguese')),
    ('en', _('English')),
)

# A boolean that turns on/off debug mode. When set to ``True``, stack traces
# are displayed for error pages. Should always be set to ``False`` in
# production. Best set to ``True`` in local_settings.py
DEBUG = os.getenv('DEBUG') not in ['False', 'false', 'FALSE']

# Whether a user's session cookie expires when the Web browser is closed.
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

AUTHENTICATION_BACKENDS = {
    "mezzanine.core.auth_backends.MezzanineBackend",
}

# The numeric mode to set newly-uploaded files to. The value should be
# a mode you'd pass directly to os.chmod.
FILE_UPLOAD_PERMISSIONS = 0o644

#########
# PATHS #
#########

# Full filesystem path to the project.
PROJECT_APP_PATH = Path(__file__).resolve().parent
PROJECT_APP = str(PROJECT_APP_PATH.stem)
PROJECT_ROOT = BASE_DIR = PROJECT_APP_PATH.parent

# Every cache key will get prefixed with this value - here we set it to
# the name of the directory the project is in to try and use something
# project specific.
CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_APP

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = PROJECT_ROOT / STATIC_URL.strip("/")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = STATIC_URL + "media/"

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = PROJECT_ROOT / MEDIA_URL.strip("/")

# Package/module name to import the root urlpatterns from for the project.
ROOT_URLCONF = f"{PROJECT_APP}.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            str(PROJECT_ROOT / "templates")
        ],
        #  "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.static",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.template.context_processors.tz",
                "mezzanine.conf.context_processors.settings",
                "mezzanine.pages.context_processors.page",
                "carceropolis.context_processors.add_login_form",
                "carceropolis.context_processors.add_registration_form",
                "carceropolis.context_processors.add_password_recover_form",
            ],
            "builtins": [
                "mezzanine.template.loader_tags",
            ],
            "loaders": [
                "mezzanine.template.loaders.host_themes.Loader",
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader"
            ]

        },
    },
]

################
# APPLICATIONS #
################

INSTALLED_APPS = (
    # "flat",
    # "moderna",
    # "nova",
    # "solid",
    "mezzanine.blog",
    "cidades",
    "carceropolis",
    "django_extensions",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.postgres",
    "django.contrib.redirects",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "phonenumber_field",
    "mezzanine.boot",
    "mezzanine.conf",
    "mezzanine.core",
    "mezzanine.generic",
    "mezzanine.pages",
    "mezzanine.forms",
    # "mezzanine.galleries",
    # "mezzanine.twitter",
    "mezzanine.accounts",
    # "mezzanine.mobile",
    "logentry_admin",
)

MIGRATION_MODULES = {
    'carceropolis': 'carceropolis.migrations.carceropolis',
    'pages': 'carceropolis.migrations.pages',
    'forms': 'carceropolis.migrations.forms',
    'blog': 'carceropolis.migrations.blog',
    'conf': 'carceropolis.migrations.conf',
}

# List of middleware classes to use. Order is important; in the request phase,
# these middleware classes will be applied in the order given, and in the
# response phase the middleware will be applied in reverse order.
MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    # Uncomment if using internationalisation or localisation
    # "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.SessionAuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    "mezzanine.core.request.CurrentRequestMiddleware",
    "mezzanine.core.middleware.RedirectFallbackMiddleware",
    "mezzanine.core.middleware.AdminLoginInterfaceSelectorMiddleware",
    "mezzanine.core.middleware.SitePermissionMiddleware",
    # Uncomment the following if using any of the SSL settings:
    # "mezzanine.core.middleware.SSLRedirectMiddleware",
    "mezzanine.pages.middleware.PageMiddleware",
]

if os.getenv('IS_PRODUCTION'):
    MIDDLEWARE.insert(0, "mezzanine.core.middleware.UpdateCacheMiddleware")
    MIDDLEWARE.append("mezzanine.core.middleware.FetchFromCacheMiddleware")

# Store these package names here as they may change in the future since
# at the moment we are using custom forks of them.
PACKAGE_NAME_FILEBROWSER = "filebrowser_safe"
PACKAGE_NAME_GRAPPELLI = "grappelli_safe"

#########################
# OPTIONAL APPLICATIONS #
#########################

# These will be added to ``INSTALLED_APPS``, only if available.
OPTIONAL_APPS = (
    "debug_toolbar",
    "django_extensions",
    "compressor",
    PACKAGE_NAME_FILEBROWSER,
    PACKAGE_NAME_GRAPPELLI,
)

#########################
# CARCEROPOLIS SETTINGS #
#########################
PHONENUMBER_DB_FORMAT = "E164"
PHONENUMBER_DEFAULT_REGION = "BR"
BLOG_SLUG = "publicacoes"

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        }
    },
    'loggers': {
        'carceropolis.views': {
            'handlers': ['console'],
            'level': os.getenv('CONSOLE_LOG_LEVEL') or 'DEBUG',
        }
    }
}

SECRET_KEY = os.getenv('SECRET_KEY') or '9b9n_5u!y-ge6+1+f##vt3ub9tp5hq(aq^4g&'
NEVERCACHE_KEY = os.getenv('NEVERCACHE_KEY') or '%vpsl!vjiw9m^4j(=c#gv47m849+t'

# Os valores DEFAULT aqui definidos são pensados para o projeto sendo rodado
# com o docker-compose do repositório do projeto.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv('DB_NAME') or 'postgres',
        "USER": os.getenv('DB_USER') or 'postgres',
        "PASSWORD": os.getenv('DB_PASS') or 'carceropolis',
        "HOST": os.getenv('DB_HOST') or 'db',
    }
}

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTOCOL", "https")

ACCOUNTS_APPROVAL_REQUIRED = True

ACCOUNTS_VERIFICATION_REQUIRED = True

try:
    PUBLICACAO_PER_PAGE = int(os.getenv('PUBLICACAO_PER_PAGE'))
except (ValueError, TypeError):
    PUBLICACAO_PER_PAGE = 9

# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
MAX_UPLOAD_SIZE = os.getenv("MAX_UPLOAD_SIZE") or "5242880"

COMMENTS_DISQUS_SHORTNAME = False

ENABLE_COMMENTS = False

# Converting from PosixPath to str
PROJECT_APP_PATH = str(PROJECT_APP_PATH)
PROJECT_APP = str(PROJECT_APP)
PROJECT_ROOT = str(PROJECT_ROOT)
STATIC_ROOT = str(STATIC_ROOT)
MEDIA_ROOT = str(MEDIA_ROOT)

##################
# EMAIL SETTINGS #
##################
if (os.getenv("EMAIL_HOST") and
        os.getenv("EMAIL_HOST_PASSWORD") and
        os.getenv("EMAIL_HOST_USER")):
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
    EMAIL_PORT = os.getenv("EMAIL_PORT", 25)
    EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", False)

if os.getenv("IS_PRODUCTION"):
    # First one on the list
    MIDDLEWARE.insert(0, 'django.middleware.cache.UpdateCacheMiddleware')
    # Last one on the list
    MIDDLEWARE.append('django.middleware.cache.FetchFromCacheMiddleware')

    # Timeout here is the time that the django-server will hold the cached
    # files on the server, it is not directly related to the http headers
    # timeout information (defined below).
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': 'memcache:11211',
            'TIMEOUT': 60*60*48
        }
    }

    # The number of seconds each page should be cached
    # https://docs.djangoproject.com/en/2.0/topics/cache/#the-per-site-cache
    CACHE_MIDDLEWARE_SECONDS = 60*60

####################
# DYNAMIC SETTINGS #
####################

# set_dynamic_settings() will rewrite globals based on what has been
# defined so far, in order to provide some better defaults where
# applicable. We also allow this settings module to be imported
# without Mezzanine installed, as the case may be when using the
# fabfile, where setting the dynamic settings below isn't strictly
# required.
try:
    from mezzanine.utils.conf import set_dynamic_settings
except ImportError:
    pass
else:
    set_dynamic_settings(globals())

"""
Django settings for starfish project.

Generated by 'django-admin startproject' using Django 5.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

from pathlib import Path

from configurations import Configuration, values
from django.urls import reverse_lazy


class Common(Configuration):
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Secrets definition (required to be set via environment variables)
    SECRET_KEY = values.SecretValue()

    # Application definition
    INSTALLED_APPS = [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'starfish',
        'users',
        'unfold',
        'unfold.contrib.filters',
        'unfold.contrib.forms',
        'unfold.contrib.inlines',
        'unfold.contrib.import_export',
        'unfold.contrib.simple_history',
        'simple_history',
        'django.contrib.admin',
        'import_export',
        'rules',
        'rest_framework',
        'regions',
        'chapters',
        'members',
        'partners',
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'allauth.socialaccount.providers.google',
        'allauth.socialaccount.providers.discord',
        'django_prometheus',
    ]

    AUTHENTICATION_BACKENDS = (
        'rules.permissions.ObjectPermissionBackend',
        'django.contrib.auth.backends.ModelBackend',
        'allauth.account.auth_backends.AuthenticationBackend',
    )

    MIDDLEWARE = [
        'django_prometheus.middleware.PrometheusBeforeMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'allauth.account.middleware.AccountMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'simple_history.middleware.HistoryRequestMiddleware',
        'django_prometheus.middleware.PrometheusAfterMiddleware',
    ]

    ROOT_URLCONF = 'starfish.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [BASE_DIR / 'starfish' / 'templates'],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    'starfish.context_processors.the_totals',
                    'starfish.context_processors.hide_save_and_add_another',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'starfish.wsgi.application'

    # Database
    # https://docs.djangoproject.com/en/5.2/ref/settings/#databases
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

    # Password validation
    # https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators
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
    # https://docs.djangoproject.com/en/5.2/topics/i18n/
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = values.Value('UTC')
    USE_I18N = True
    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/5.2/howto/static-files/
    STATIC_URL = 'static/'

    # Default primary key field type
    # https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field
    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    DEBUG = values.BooleanValue(False)

    SIMPLE_HISTORY_REVERT_DISABLED = True
    AUTH_USER_MODEL = 'users.User'
    MEMBER_HASH_SALT = values.SecretValue()
    FINAL_COUNT = 11000000

    # Allauth Configuration (updated to use new format)
    ACCOUNT_LOGIN_METHODS = {'username'}
    ACCOUNT_SIGNUP_FIELDS = [
        'username*',
        'password1*',
        'password2*',
    ]  # email is optional
    ACCOUNT_EMAIL_VERIFICATION = 'none'
    ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
    ACCOUNT_EMAIL_SUBJECT_PREFIX = '[Strikecard] '

    # Disable regular signup, only allow OAuth
    ACCOUNT_ADAPTER = 'adapters.CustomAccountAdapter'
    SOCIALACCOUNT_ADAPTER = 'adapters.CustomSocialAccountAdapter'
    ACCOUNT_SIGNUP_ENABLED = False  # Disable regular signup form

    # Social Account Settings
    SOCIALACCOUNT_AUTO_SIGNUP = True
    SOCIALACCOUNT_EMAIL_REQUIRED = False
    SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
    SOCIALACCOUNT_STORE_TOKENS = True  # Store OAuth tokens for future use
    SOCIALACCOUNT_PROVIDERS = {
        'google': {
            'SCOPE': [
                'profile',
                'email',
            ],
            'AUTH_PARAMS': {
                'access_type': 'online',
            },
        },
        'discord': {
            'SCOPE': [
                'identify',
                'email',
            ],
        },
    }

    # Login/Logout URLs
    LOGIN_REDIRECT_URL = '/'
    LOGOUT_REDIRECT_URL = '/'

    # Additional Allauth Settings
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'
    ACCOUNT_RATE_LIMITS = {
        'login_failed': '5/5m',  # 5 failed attempts per 5 minutes
    }
    ACCOUNT_LOGOUT_ON_GET = True  # Allow logout via GET request
    ACCOUNT_SESSION_REMEMBER = True  # Remember user session

    # Prometheus Configuration
    PROMETHEUS_EXPORT_MIGRATIONS = False  # Disable migration metrics in development
    PROMETHEUS_LATENCY_BUCKETS = [
        0.1,
        0.25,
        0.5,
        1.0,
        2.5,
        5.0,
        10.0,
    ]  # Response time buckets

    UNFOLD = {
        'SITE_TITLE': 'Strikecard Admin',
        'SITE_HEADER': 'Strikecard Admin',
        'SITE_SUBHEADER': 'Operation Starfish 2.0',
        'SITE_SYMBOL': 'flare',
        'ENVIRONMENT': lambda r: ['Dev', 'primary'],
        'SITE_DROPDOWN': [
            {
                'title': 'Public site',
                'link': '/',
                'target': '_blank',
            },
        ],
        'SIDEBAR': {
            'navigation': [
                {
                    'title': 'Navigation',
                    'collapsible': False,
                    'items': [
                        {
                            'title': 'Members',
                            'icon': 'person',
                            'link': reverse_lazy('admin:members_member_changelist'),
                        },
                        {
                            'title': 'Chapters',
                            'icon': 'groups',
                            'link': reverse_lazy('admin:chapters_chapter_changelist'),
                        },
                        {
                            'title': 'Partners',
                            'icon': 'group',
                            'link': reverse_lazy(
                                'admin:partners_partnercampaign_changelist'
                            ),
                        },
                        {
                            'title': 'Affiliates',
                            'icon': 'group',
                            'link': reverse_lazy('admin:partners_affiliate_changelist'),
                        },
                    ],
                },
                {
                    'title': 'Regions',
                    'collapsible': True,
                    'items': [
                        {
                            'title': 'States',
                            'icon': 'map',
                            'link': reverse_lazy('admin:regions_state_changelist'),
                        },
                        {
                            'title': 'ZIP Codes',
                            'icon': 'map',
                            'link': reverse_lazy('admin:regions_zip_changelist'),
                        },
                        {
                            'title': 'Chapter ZIPs',
                            'icon': 'map',
                            'link': reverse_lazy(
                                'admin:chapters_chapterzip_changelist'
                            ),
                        },
                    ],
                },
                {
                    'title': 'Access',
                    'collapsible': True,
                    'items': [
                        {
                            'title': 'Users',
                            'icon': 'person',
                            'link': reverse_lazy('admin:users_user_changelist'),
                        },
                        {
                            'title': 'Groups',
                            'icon': 'group',
                            'link': reverse_lazy('admin:auth_group_changelist'),
                        },
                    ],
                },
            ],
        },
    }
    DEBUG_TOOLBAR = False


class Dev(Common):
    DEBUG = values.BooleanValue(True)
    DEBUG_TOOLBAR = True
    INSTALLED_APPS = Common.INSTALLED_APPS + ["debug_toolbar"]
    MIDDLEWARE = [
        'starfish.middleware.ipdb_exception.IPDBExceptionMiddleware',
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ] + Common.MIDDLEWARE
    INTERNAL_IPS = ["127.0.0.1"]
    ALLOWED_HOSTS = values.ListValue(["localhost"])
    STATIC_ROOT = Common.BASE_DIR / 'static/'

    # Development-specific Allauth settings - allow both OAuth and regular signup
    ACCOUNT_SIGNUP_ENABLED = True  # Re-enable regular signup for development
    ACCOUNT_ADAPTER = 'adapters.DevAccountAdapter'  # Use dev-specific adapter


class Production(Common):
    DEBUG = False
    ALLOWED_HOSTS = values.ListValue([".generalstrikeus.com"])
    ACCOUNT_SIGNUP_ENABLED = False  # Disable regular signup for production
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

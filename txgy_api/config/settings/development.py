"""
开发环境配置
"""
from .base import *

# 开发环境特定配置
DEBUG = True

# 允许的主机
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# 开发环境数据库配置
DATABASES['default'].update({
    'NAME': config('DB_NAME', default='txgy_platform_dev'),
})

# 开发工具 (暂时注释掉，后续需要时再启用)
# INSTALLED_APPS += [
#     'django_extensions',
# ]

# 开发环境中间件
# if DEBUG:
#     MIDDLEWARE += [
#         'django_extensions.management.debug_toolbar.DebugToolbarMiddleware',
#     ]
#
#     INSTALLED_APPS += [
#         'debug_toolbar',
#     ]
#
#     INTERNAL_IPS = [
#         '127.0.0.1',
#         'localhost',
#     ]

# 邮件配置（开发环境使用控制台后端）
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# 缓存配置（开发环境使用本地内存缓存）
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# 日志配置（开发环境更详细的日志）
LOGGING['handlers']['console']['level'] = 'DEBUG'
LOGGING['loggers']['apps']['level'] = 'DEBUG'

# CORS配置（开发环境允许所有来源）
CORS_ALLOW_ALL_ORIGINS = True

# 静态文件配置
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

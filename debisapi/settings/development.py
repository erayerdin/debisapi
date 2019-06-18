from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

# CORS
INSTALLED_APPS.append("corsheaders")
MIDDLEWARE.insert(0, "corsheaders.middleware.CorsMiddleware")
CORS_ORIGIN_ALLOW_ALL = True

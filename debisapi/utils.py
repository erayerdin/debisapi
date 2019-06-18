import jwt
from django.conf import settings


def get_token(request):
    author_header = request.META.get("HTTP_AUTHORIZATION", None)

    if author_header is None:
        return None

    return author_header[6:]


def get_payload(request):
    token = get_token(request)

    if token is None:
        return None

    return jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")

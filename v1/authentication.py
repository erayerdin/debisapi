import jwt
from django.conf import settings
from rest_framework import authentication, exceptions


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        author_header = request.META.get("Authorization", None)

        if author_header is None:
            raise exceptions.AuthenticationFailed("Token must be provided.")

        token = author_header[6:]
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms="HS256"
            )
        except jwt.exceptions.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token has expired.")
        except (
            jwt.exceptions.DecodeError,
            jwt.exceptions.InvalidSignatureError,
        ):
            raise exceptions.AuthenticationFailed("Token is invalid.")

        return (None, None)

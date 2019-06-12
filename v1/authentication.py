import jwt
import requests
from django.conf import settings
from rest_framework import authentication, exceptions

from debisapi.utils import get_payload


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


class CredentialsAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        payload = get_payload(request)

        username = payload["username"]
        password = payload["password"]

        soup_response = requests.post(
            "http://debis.deu.edu.tr/debis.php",
            data={
                "username": username,
                "password": password,
                "emailHost": "ogr.deu.edu.tr",
            },
        )

        if "hatal" in soup_response.text:
            raise exceptions.AuthenticationFailed("User is invalid.")

        return (None, None)

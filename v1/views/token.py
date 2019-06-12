import logging

import jwt
import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.views import Request, Response, status


@api_view(["POST"])
def token_claim(request: Request):
    logger = logging.getLogger(token_claim.__name__)

    if "username" not in request.POST or "password" not in request.POST:
        return Response(
            {"detail": "You must provide both username and password fields."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    logger.debug("Requesting DEBİS login...")
    scrap_response = requests.post(
        "http://debis.deu.edu.tr/debis.php",
        data=dict(
            username=request.POST["username"],
            password=request.POST["password"],
        ),
    )

    if "hatal" in scrap_response.text:
        logger.debug(
            "Login has failed for {}.".format(request.POST["username"])
        )
        return Response(
            {"detail": "Username or password is invalid."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    logger.debug("Generating payload...")
    payload = {
        "username": request.POST["username"],
        "password": request.POST["password"],
        "exp": settings.JWT_EXPIRATION(),
    }

    token = jwt.encode(payload, settings.SECRET_KEY)
    return Response({"token": token.decode("utf-8")})

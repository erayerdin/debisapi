import typing

import requests
from bs4 import BeautifulSoup
from rest_framework import decorators, response, status

from debisapi.utils import get_payload
from v1 import authentication

RESULTS_URL = (
    "http://debis.deu.edu.tr/OgrenciIsleri/Ogrenci/OgrenciNotu/index.php"
)


@decorators.api_view(["GET"])
@decorators.authentication_classes(
    [
        authentication.JWTAuthentication,
        authentication.CredentialsAuthentication,
    ]
)
def results_terms(request):
    def parse(soup_response) -> typing.List[dict]:
        soup = BeautifulSoup(soup_response.content, "lxml")

        select_elm = soup.find("select", attrs={"id": "ogretim_donemi_id"})
        option_elms = select_elm.find_all("option")[1:]

        data = []

        for elm in option_elms:
            obj = {"id": None, "name": None}
            obj["id"] = elm["value"]
            obj["name"] = elm.text.strip()
            data.append(obj)

        return data

    payload = get_payload(request)
    payload.pop("exp", None)
    payload["emailHost"] = "ogr.deu.edu.tr"
    soup_response = requests.post(RESULTS_URL, data=payload)

    return response.Response(parse(soup_response))


@decorators.api_view(["GET"])
@decorators.authentication_classes(
    [
        authentication.JWTAuthentication,
        authentication.CredentialsAuthentication,
    ]
)
def results_klasses(request):
    def parse(soup_response) -> typing.List[dict]:
        soup = BeautifulSoup(soup_response.content, "lxml")

        select_elm = soup.find("select", attrs={"id": "ders"})
        option_elms = select_elm.find_all("option")[1:]

        data = []

        for elm in option_elms:
            obj = {"id": None, "name": None}
            obj["id"] = elm["value"]
            obj["name"] = elm.text.strip()
            data.append(obj)

        return data

    term_id = request.GET.get("termId", None)

    if term_id is None:
        return response.Response(
            {"detail": "termId parameter must be provided."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    payload = get_payload(request)
    payload.pop("exp", None)
    payload["emailHost"] = "ogr.deu.edu.tr"
    soup_response = requests.post(RESULTS_URL, data=payload)

    return response.Response(parse(soup_response))

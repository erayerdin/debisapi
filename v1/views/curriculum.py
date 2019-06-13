import typing

import requests
from bs4 import BeautifulSoup
from rest_framework import decorators, request, response, views

from debisapi.utils import get_payload
from v1 import authentication

CURRICULUM_URL = (
    "http://debis.deu.edu.tr/OgrenciIsleri/Ogrenci/DersProgrami/index.php"
)


@decorators.api_view(["GET"])
@decorators.authentication_classes(
    [
        authentication.JWTAuthentication,
        authentication.CredentialsAuthentication,
    ]
)
def curriculum_terms(request):
    def parse(soup_response) -> typing.List[dict]:
        soup = BeautifulSoup(soup_response.content, "lxml")

        select_elm = soup.find("select", attrs={"id": "ogretim_donemi_id"})
        option_elms = select_elm.find_all("option")

        data = []

        for elm in option_elms:
            obj = {"id": None, "name": None}
            obj["id"] = int(elm["value"])
            obj["name"] = elm.text.strip()
            data.append(obj)

        return data

    payload = get_payload(request)
    payload.pop("exp", None)
    soup_response = requests.post(CURRICULUM_URL, data=payload)

    return response.Response(parse(soup_response))

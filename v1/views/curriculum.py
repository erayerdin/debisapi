import re
import typing

import requests
from bs4 import BeautifulSoup
from rest_framework import decorators, request, response, status, views

from debisapi.utils import get_payload
from v1 import authentication

CURRICULUM_URL = (
    "http://debis.deu.edu.tr/OgrenciIsleri/Ogrenci/DersProgrami/index.php"
)


@decorators.api_view(["GET"])
@authentication.AUTHENTICATION_DECORATOR
def curriculum(request):
    def parse_session(elm) -> dict:
        """Parses "from" and "to" hours."""
        vals = elm.text.strip().split(" ")  # "17:00 17:45"
        return {
            "fromHour": vals[0] if len(vals) > 0 else None,
            "toHour": vals[1] if len(vals) > 1 else None,
        }

    def parse_td(elm, day: int, session: dict) -> dict:
        obj = {
            "day": day,
            "department": None,
            "code": None,
            "name": None,
            "branch": None,
            "is_theoric": False,
            "lecturer": None,
            "location": None,
        }
        obj.update(session)

        text = elm.get_text("\n").strip()  # type: str
        if not text:  # empty
            return None
        lines = text.splitlines()

        obj["department"] = lines[0]

        code = re.findall("[A-ZÇĞİÖŞÜ]{3} [0-9]{4}", text)
        obj["code"] = code[0] if len(code) else None

        # ref: https://regex101.com/r/sC54Yv/1
        name = re.findall("[A-ZÇĞİÖŞÜ]{3} [0-9]{4} ?- ?(.+)\n", text)
        obj["name"] = name[0] if len(name) else None

        branch = re.findall("(.+) Şubesi", text)
        obj["branch"] = branch[0] if len(branch) else None

        obj["is_theoric"] = True if "Teorik" in text else False
        obj["lecturer"] = lines[-3]

        location = re.findall("Derslik:\n(.+)", text)
        obj["location"] = location[0].strip() if len(location) else None

        return obj

    def parse_tr(elm) -> typing.List[dict]:
        td_elms = elm.find_all("td")

        session_elm = td_elms[0]
        session = parse_session(session_elm)

        objs = []
        for index, td_elm in enumerate(td_elms[1:]):
            obj = parse_td(td_elm, index + 1, session)
            if obj is not None:
                objs.append(obj)

        return objs

    def parse(soup_response):
        soup = BeautifulSoup(soup_response.content, "lxml")

        table_elm = soup.find("table", attrs={"bordercolor": "#FF9900"})
        tbody_elm = table_elm.find("tbody")
        inspection_elm = table_elm if tbody_elm is None else tbody_elm
        tr_elms = inspection_elm.find_all("tr")

        data = []
        for tr_elm in tr_elms[1:]:  # without table header
            objs = data.extend(parse_tr(tr_elm))

        return data

    term_id, week_id = (
        request.GET.get("termId", None),
        request.GET.get("weekId", None),
    )

    if None in (term_id, week_id):
        return response.Response(
            {"detail": "termId and weekId must be provided as parameter."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    payload = get_payload(request)
    payload.pop("exp", None)
    payload["emailHost"] = "ogr.deu.edu.tr"
    payload["ogretim_donemi_id"] = request.GET["termId"]
    payload["hafta"] = request.GET["weekId"]
    soup_response = requests.post(CURRICULUM_URL, data=payload)

    return response.Response(parse(soup_response))


@decorators.api_view(["GET"])
@authentication.AUTHENTICATION_DECORATOR
def curriculum_terms(request):
    def parse(soup_response) -> typing.List[dict]:
        soup = BeautifulSoup(soup_response.content, "lxml")

        select_elm = soup.find("select", attrs={"id": "ogretim_donemi_id"})
        option_elms = select_elm.find_all("option")

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
    soup_response = requests.post(CURRICULUM_URL, data=payload)

    return response.Response(parse(soup_response))


@decorators.api_view(["GET"])
@authentication.AUTHENTICATION_DECORATOR
def curriculum_weeks(request):
    def parse(soup_response) -> typing.List[dict]:
        soup = BeautifulSoup(soup_response.content, "lxml")

        select_elm = soup.find("select", attrs={"id": "hafta"})
        option_elms = select_elm.find_all("option")

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
    payload["ogretim_donemi_id"] = str(term_id)
    soup_response = requests.post(CURRICULUM_URL, data=payload)

    return response.Response(parse(soup_response))

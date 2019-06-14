import requests
from bs4 import BeautifulSoup
from rest_framework import decorators, response

from debisapi.utils import get_payload
from v1 import authentication
from v1.views.results import RESULTS_URL as INFO_URL


@decorators.api_view(["GET"])
@decorators.authentication_classes(
    [
        authentication.JWTAuthentication,
        authentication.CredentialsAuthentication,
    ]
)
def info(request):
    def parse_tr(elm):
        return elm.find_all("td")[1]

    def parse_whole(elm):
        td_elm = parse_tr(elm)
        return td_elm.text.strip()

    def parse_class(elm) -> int:
        td_elm = parse_tr(elm)
        return int(td_elm.text.strip()[0])

    def parse_system(elm) -> bool:
        td_elm = parse_tr(elm)
        return td_elm.text.strip() == "BAĞIL"

    def parse_term(soup) -> int:
        select_elm = soup.find("select", attrs={"id": "ogretim_donemi_id"})
        option_elms = select_elm.find_all("option")
        return len(option_elms) - 1

    def parse(soup_response):
        soup = BeautifulSoup(soup_response.content, "lxml")

        form_elm = soup.find("form", attrs={"name": "form_donem"})
        tbody_elm = form_elm.find("tbody")

        tr_elms = tbody_elm.find_all("tr")

        name_surname_elm = tr_elms[0]
        student_id_elm = tr_elms[1]
        official_class_elm = tr_elms[2]
        faculty_elm = tr_elms[3]
        department_elm = tr_elms[4]
        system_elm = tr_elms[5]

        data = {
            "name": parse_whole(name_surname_elm),
            "studentId": parse_whole(student_id_elm),
            "officialClass": parse_class(official_class_elm),
            "term": parse_term(soup),
            "faculty": parse_whole(faculty_elm),
            "department": parse_whole(department_elm),
            "isRelative": parse_system(system_elm),
        }

        return data

    payload = get_payload(request)
    payload.pop("exp", None)
    payload["emailHost"] = "ogr.deu.edu.tr"

    soup_response = requests.post(INFO_URL, data=payload)

    return response.Response(parse(soup_response))

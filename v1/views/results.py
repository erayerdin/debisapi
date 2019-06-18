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
@authentication.AUTHENTICATION_DECORATOR
def results(request):
    def parse_table_section(table_elm, is_left=True):
        sections = table_elm.find_all("tr")[2]
        td_elms = sections.find_all("td", recursive=False)

        if is_left:
            return td_elms[0].find("table")

        return td_elms[1].find("table")

    def parse_klass(table_elm) -> dict:
        def parse_code_name(
            table_elm
        ) -> typing.Tuple[typing.Union[str, None]]:
            header_tr_elm = table_elm.find_all("tr")[0]
            content = header_tr_elm.text.strip()
            parsed_content = content.split(" - ")
            return (
                parsed_content[0] if len(parsed_content) > 0 else None,
                parsed_content[1] if len(parsed_content) > 1 else None,
            )

        def parse_has_completed(table_elm) -> typing.Union[bool, None]:
            footer_tr_elm = table_elm.find_all("tr")[-1]
            if footer_tr_elm is None:
                return None

            content = footer_tr_elm.text.strip()
            return content != "ALIYOR"

        def parse_left_section(
            left_section, index: int, wrapper=str
        ) -> typing.Union[str, int, bool]:
            elm = left_section.find_all("tr")[index].find_all("td")[2]
            try:
                return wrapper(elm.text.strip())
            except Exception:
                return None

        code_name = parse_code_name(table_elm)
        left_section = parse_table_section(table_elm)

        data = {
            "code": code_name[0],
            "name": code_name[1],
            "faculty": parse_left_section(left_section, 0),
            "department": parse_left_section(left_section, 1),
            "branch": parse_left_section(left_section, 2, lambda s: str(s[0])),
            "credit": parse_left_section(left_section, 3, int),
            "isMandatory": parse_left_section(
                left_section, 4, lambda s: s == "Zorunlu"
            ),
            "repetitionCount": parse_left_section(left_section, 5, int),
            "lecturer": parse_left_section(
                left_section, 6, lambda s: s.split(" (")[0]
            ),
            "mandatoryParticipancy": parse_left_section(
                left_section, 7, lambda s: "DEVAM MECBURİ" in s
            ),
            "hasCompleted": parse_has_completed(table_elm),
        }

        return data

    def parse_results(table_elm) -> typing.List[dict]:
        def parse_right_section(right_section, index) -> dict:
            elm = right_section.find_all("tr")[index].find_all("td")
            name_elm = elm[0]
            announcement_elm = elm[1]
            median1_elm = elm[2]
            median2_elm = elm[3]
            grade_elm = elm[4]

            data = {
                "name": name_elm.text.strip(),
                "announcement": announcement_elm.text.strip()
                if announcement_elm.text.strip() != "İLAN EDİLMEMİŞ"
                else None,
                "median1": int(median1_elm.text.strip())
                if median1_elm.text.strip()
                else None,
                "median2": int(median2_elm.text.strip())
                if median2_elm.text.strip()
                else None,
                "grade": grade_elm.text.strip()
                if grade_elm.text.strip()
                else None,
            }

            return data

        results = []
        right_section = parse_table_section(table_elm, False)
        result_length = len(right_section.find_all("tr")) - 1

        for index in range(result_length):
            result = parse_right_section(right_section, index + 1)
            results.append(result)

        return results

    def parse(soup_response) -> dict:
        soup = BeautifulSoup(soup_response.content, "lxml")
        table_elm = soup.find("table", attrs={"bgcolor": "99CCFF"})

        data = {
            "class": parse_klass(table_elm),
            "results": parse_results(table_elm),
        }

        return data

    term_id = request.GET.get("termId", None)
    klass_id = request.GET.get("classId", None)

    if None in (term_id, klass_id):
        return response.Response(
            {"detail": "termId and classId parameters must be provided."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    payload = get_payload(request)
    payload.pop("exp", None)
    payload["emailHost"] = "ogr.deu.edu.tr"
    soup_response = requests.post(RESULTS_URL, data=payload)

    return response.Response(parse(soup_response))


@decorators.api_view(["GET"])
@authentication.AUTHENTICATION_DECORATOR
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
@authentication.AUTHENTICATION_DECORATOR
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

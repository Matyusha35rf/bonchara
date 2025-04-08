from selectolax.parser import HTMLParser
from datetime import datetime
import requests

from lk import lk_func


def parsing_profile(session):
    url = 'https://lk.sut.ru/cabinet/project/cabinet/forms/profil.php'
    profile = lk_func.connect_session(url, session)
    profile = HTMLParser(profile)
    trs = profile.css("tr")
    prof = ""
    for tr in trs:
        prof += tr.text().strip() + "\n"
    prof = prof.split("Учебное заведение:")[-1]
    prof = "Учебное заведение:" + prof
    lines = prof.split("\n")
    prof_dict = {}
    for line in lines:
        if ":" in line:
            line = line.split(':')
            prof_dict[line[0]] = line[1]
            if line[0] == "Курс":
                month = datetime.now().month
                sem = 2 if 1 < month < 9 else 1
                prof_dict["Семестр"] = str((int(line[1])-1)*2 + sem)
    return prof_dict


if __name__ == "__main__":
    session = requests.Session()
    lk_func.auth(session, 'mosenkov16@mail.ru', 'i5jRHseAQjaS')
    parsing_profile(session)



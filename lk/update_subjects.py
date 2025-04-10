import requests
from selectolax.parser import HTMLParser
from lk import lk_func
from data.database import add_to_db_subjects


def update_subjects(session, user_sem, user_id):
    url = "https://lk.sut.ru/cabinet/project/cabinet/forms/uch_grafik.php"
    uchplan = lk_func.connect_session(url, session)
    lines = HTMLParser(uchplan).css("tr")
    subjects = []
    for line in lines[1:]:
        uchplan_sem = int(line.text(strip=True)[1])
        columns = line.css("td")
        if uchplan_sem == user_sem:
            subjects.append(columns[3].text(strip=True))
    add_to_db_subjects(int(user_id), subjects)


if __name__ == "__main__":
    with requests.Session() as session:
        lk_func.auth(session, 'mosenkov16@mail.ru', 'i5jRHseAQjaS')
        update_subjects(session, 4, 1331469795)


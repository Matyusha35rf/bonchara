import requests
from selectolax.parser import HTMLParser
from lk import lk_func


def parsing_uchplan(session, user_sem):
    url = "https://lk.sut.ru/cabinet/project/cabinet/forms/uch_grafik.php"
    uchplan = lk_func.connect_session(url, session)
    lines = HTMLParser(uchplan).css("tr")
    for line in lines[1:]:
        uchplan_sem = int(line.text(strip=True)[1])
        if user_sem == uchplan_sem:
            columns = line.css("td")
            print(columns[3].text(strip=True))


if __name__ == "__main__":
    with requests.Session() as session:
        lk_func.auth(session, 'mosenkov16@mail.ru', 'i5jRHseAQjaS')
        parsing_uchplan(session, 4)


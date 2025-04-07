import os
import sqlite3
import requests
import config
from selectolax.parser import HTMLParser

session = requests.Session()
session.get(config.base_url, headers=config.headers)
# Авторизация
payload = {
    'users': 'mosenkov16@mail.ru',  # Замените на ваш логин
    'parole': 'i5jRHseAQjaS'  # Замените на ваш пароль
}
auth_response = session.post(
    config.login_url,
    data=payload,
    headers=config.headers,
    allow_redirects=False
)

url = 'https://lk.sut.ru/cabinet/project/cabinet/forms/profil.php'
sem = session.get(
    url,
    headers=config.headers
).text

sem = HTMLParser(sem).css('.col-md-1')
print(sem)

url = 'https://lk.sut.ru/cabinet/project/cabinet/forms/uch_grafik.php'

subjects = session.get(
    url,
    headers=config.headers
).text

subjects2 = HTMLParser(subjects).css('tr')



import os
import sqlite3
import requests
from selectolax.parser import HTMLParser

import config
from lk_func import auth

def parsing_profile(session):
    url = 'https://lk.sut.ru/cabinet/project/cabinet/forms/profil.php'
    profile = session.get(
        url,
        headers=config.headers
    ).text
    return profile



session = requests.Session()
auth(session, 'mosenkov16@mail.ru', 'i5jRHseAQjaS')
print(parsing_profile(session))

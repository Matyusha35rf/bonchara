from urllib.parse import urljoin

# ссылки и хедеры
base_url = "https://lk.sut.ru/cabinet/"
login_url = urljoin(base_url, 'lib/autentificationok.php')
target_url = urljoin(base_url, 'project/cabinet/forms/raspisanie.php')
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.124 Safari/537.36",
    "Referer": base_url,
    "Origin": "https://lk.sut.ru"
}

# токен бота
api_token = '8179996730:AAFrP2nOYQhZCeGugEDJRxHwQjAVe3jWcIg'

# имя файла с клиентами
db_file = "users.db"

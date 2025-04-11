from urllib.parse import urljoin

import bot_token

# ссылки и хедеры
base_url = "https://lk.sut.ru/cabinet/"
login_url = urljoin(base_url, 'lib/autentificationok.php')
schedule_url = urljoin(base_url, 'project/cabinet/forms/raspisanie.php')
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.124 Safari/537.36",
    "Referer": base_url,
    "Origin": "https://lk.sut.ru"
}


start_lessons = ['09:00', '10:45', '13:00', '14:45', '16:30', '18:15', '20:00']
end_lessons   = ['10:35', '12:20', '14:35', '16:20', '18:05', '19:50', '21:35']

# токен бота
api_token = bot_token.token

# путь к ключам
KEYS_FILE_PATH = 'keys.txt'

import csv
import time
from dbm import error

from av.auto_visit import System


class App:
    def __init__(self):
        self.system = System()

    def read_csv(self, filename):
        with open(filename, encoding='utf-8-sig', mode="r", ) as file:
            reader = csv.DictReader(file, delimiter=",")
            clients = []
            for r in reader:
                clients.append(r)
        return clients

    def run(self, filename):
        users = self.read_csv(filename)
        for user in users:
            email, password, is_available = user['e-mail'], user['password'], user['is_available']
            if is_available == "True":
                self.system.run(email, password)


def fn() -> (Exception, str):
    return Exception, 5


if __name__ == "__main__":
    app = App()
    start = time.time()
    while True:
        app.run("users.csv")
        time.sleep(25)

    # finish = time.time()
    # print(finish - start)


import os
import datetime
from functools import wraps
import requests


path = 'main_log.log'
if os.path.exists(path):
    os.remove(path)


def logger(path):
    @wraps(path)
    def __logger(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            start = datetime.datetime.now()

            result = old_function(*args, **kwargs)

            with open(path, 'a', encoding='utf-8') as file:
                file.writelines(
                    f'Сейчас будет вызвана функция {old_function.__name__}, с аргументами {args} и {kwargs}.\n'
                    f'Начало работы {start}\n'
                    f'Возвращаемое значение: {old_function(*args, **kwargs)}\n'
                )

            return result

        return new_function

    return __logger


class Superhero:
    def __init__(self, name):
        self.name = name
        self.intelligence = self.get_intelligence()

    @logger(path)
    def get_intelligence(self):
        headers = {'Accept': 'application/json'}
        resp = requests.get(URL, headers=headers)

        if resp.status_code == 200:
            for hero in resp.json():
                if hero.get('name') == self.name:
                    self.intelligence = hero.get('powerstats').get('intelligence')
                    break

        return self.intelligence


@logger(path)
def head_intellegence(heroes):
    heroes_dict = {}

    for hero in heroes:
        heroes_dict[hero.name] = hero.intelligence

    sorted_dict = dict(sorted(heroes_dict.items(), key=lambda item: item[1], reverse=True))

    return list(sorted_dict.keys())[0]


if __name__ == '__main__':
    URL = 'https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/all.json'

    Hulk = Superhero('Hulk')
    Captain_America = Superhero('Captain America')
    Thanos = Superhero('Thanos')

    print(head_intellegence([Hulk, Captain_America, Thanos]))

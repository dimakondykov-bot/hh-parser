from black.trans import ABC
import requests


class HeadHunterApi():
    """ Класс для работы с API """
    def __init__(self):
        """ Инициализация класса """
        self.base_url = 'https://api.hh.ru'

    def get_vacancies(self, page=1, page_size=20):
        """ функция позволяет отправлять запросы и получать ответ преобразуя его в json файл """
        params = {'page': page, 'page_size': page_size}

        response = requests.get(self.base_url + '/vacancies', params=params)

        if response.status_code == 200:
            json = response.json()
            return json['items']

        return None

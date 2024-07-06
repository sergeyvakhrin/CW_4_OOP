from abc import ABC, abstractmethod

import requests


class Parser(ABC):
    """ Абстрактный класс """
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def load_vacancies(self):
        pass


class HH(Parser):
    """ Класс для работы с API HeadHunter """
    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 100}
        self.vacancies = []
        print("Загрузка данных с ресурса HH.ru. Ждите.")

    def load_vacancies(self, keyword):
        """ Метод для получения данных с ресурса HH.ru """
        self.params['text'] = keyword
        while self.params.get('page') != 20:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            vacancies = response.json()['items']
            self.vacancies.extend(vacancies)
            self.params['page'] += 1
        return self.vacancies
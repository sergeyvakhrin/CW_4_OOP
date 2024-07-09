from abc import ABC, abstractmethod

import requests


class Parser(ABC):
    """ Абстрактный класс """
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def load_vacancies(self, keyword: str):
        pass


class HH(Parser):
    """ Класс для работы с API HeadHunter """
    def __init__(self):
        self.url: str = 'https://api.hh.ru/vacancies'
        self.headers: dict = {'User-Agent': 'HH-User-Agent'}
        self.params: dict = {'text': '', 'page': 0, 'per_page': 100}
        self.vacancies: list = []
        print("Загрузка данных с ресурса HH.ru. Ждите.")

    def load_vacancies(self, keyword: str):
        """ Метод для получения данных с ресурса HH.ru """
        self.params['text'] = keyword
        while self.params.get('page') != 20:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            vacancies = response.json()['items']
            self.vacancies.extend(vacancies)
            self.params['page'] += 1
        return self.vacancies
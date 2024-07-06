import json
from abc import ABC, abstractmethod


class Worker(ABC):
    """ Асбтрактный класс """
    @abstractmethod
    def save_data(self):
        pass

    @abstractmethod
    def load_data(self):
        pass


class FileWorker:
    """ Класс для сохранения и загруки данных """

    def save_data(self, path: str, mode: str, data: list[dict]):
        """ Метод для записи данных в файл """
        with open(path, mode, encoding="UTF=8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def load_data(self, path: str):
        """ Метод для загрузки из .json """
        self.vacancies_list = []
        with open(path, 'rt', encoding="UTF=8") as file:
            self.vacancies_list = json.load(file)
            return self.vacancies_list

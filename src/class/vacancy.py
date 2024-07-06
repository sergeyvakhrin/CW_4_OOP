from config import NONE_DATA
from fileworker import FileWorker


class Vacancy(FileWorker):
    """ Класс для работы с объектами вакансий """
    vacancies_list: list = []

    def __init__(self, id_vac: str, name: str, requirement: str, responsibility: str, link: str, salary_from, salary_to):
        self.id_vac = id_vac
        self.name = name
        self.requirement = requirement
        self.responsibility = responsibility
        self.link = link
        self.salary_from = salary_from
        self.salary_to = salary_to

    def __str__(self):
        return (f'{self.id_vac}: {self.name}\n'
               f'Описание: {self.requirement}\n'
               f'Требования: {self.responsibility}\n'
               f'Сcылка: {self.link}\n'
               f'Зарплата: {self.salary_from} - {self.salary_to}')

    def __repr__(self):
        return f'{self.__class__} Поля:\n {self.__dict__}'

    @classmethod
    def get_vacancy_instance(cls, vacancies):
        """ Метод для создания списка экземпляров класса Вакансия с проверкой наличия данных """
        cls.vacancies_list = []
        for vacan in vacancies:

            id_vac = cls.validation_data(vacan.get("id", NONE_DATA))
            name = cls.validation_data(vacan.get("name", NONE_DATA))
            requirement = cls.validation_data(vacan.get("snippet").get("requirement", NONE_DATA)) \
                if isinstance(vacan.get("snippet"), (dict, str, list, int, float)) else NONE_DATA
            responsibility = cls.validation_data(vacan.get("snippet").get("responsibility", NONE_DATA)) \
                if isinstance(vacan.get("snippet"), (dict, str, list, int, float)) else NONE_DATA
            link = cls.validation_data(vacan.get("alternate_url", NONE_DATA))
            salary_from = cls.validation_data(vacan.get("salary").get("from", NONE_DATA)) \
                if isinstance(vacan.get("salary"), (dict, str, list, int, float)) else NONE_DATA
            salary_to = cls.validation_data(vacan.get("salary").get("to", NONE_DATA)) \
                if isinstance(vacan.get("salary"), (dict, str, list, int, float)) else NONE_DATA

            cls.vacancies_list.append(
                cls.add_vacanсy(id_vac=id_vac, name=name, requirement=requirement, responsibility=responsibility,
                                link=link, salary_from=salary_from, salary_to=salary_to))
        return cls.vacancies_list

    @classmethod
    def validation_data(cls, valid_data):
        """ Метод для замены значения None на иное значение """
        return valid_data if valid_data is not None else NONE_DATA

    @classmethod
    def add_vacanсy(cls, id_vac, name, requirement, responsibility, link, salary_from, salary_to):
        """ Классметод для создания эксемпляра класса Вакансия """
        return cls(id_vac, name, requirement, responsibility, link, salary_from, salary_to)

    def check_for_sort(self, other):
        """ Метод для замены строки "Не указано" на 0 для сортировке по зарплате """
        self.salary_from = 0 if self.salary_from == NONE_DATA else self.salary_from
        other.salary_from = 0 if other.salary_from == NONE_DATA else other.salary_from
        self.salary_to = 0 if self.salary_to == NONE_DATA else self.salary_to
        other.salary_to = 0 if other.salary_to == NONE_DATA else other.salary_to

    @staticmethod
    def sorted_vacancy(vacancies_list):
        """ Метод для запуска сортировки списка экземпляров класса """
        return vacancies_list.sort(reverse=True)

    def __lt__(self, other):
        """ Магический метод ля сортировки по возрастанию """
        self.check_for_sort(other)
        return self.salary_from < other.salary_from

    def __gt__(self, other):
        """ Магический метод ля сортировки по убыванию """
        self.check_for_sort(other)
        return self.salary_from > other.salary_from

    @classmethod
    def del_data(cls):
        """ Метод удаления вакансий по id """
        del_vacancy = input("Введите id вакансии: ")
        for vacan in cls.vacancies_list:
            if vacan.id_vac == del_vacancy:
                cls.vacancies_list.remove(vacan)
                return cls.vacancies_list
        print("Вакансии с таким id нет")
        return


    def get_vacations_filter(self, list_word, vacancies_list):
        """ Метод для получения списка вакансий по ключевым словам """
        self.filter_list = []
        for vacan in vacancies_list:
            find_str = vacan.name + vacan.requirement + vacan.responsibility

            # Все слова должны быть найдены в описании
            # for key, word in enumerate(list_word, 1):
            #     if word not in find_str:
            #         break
            #     if key == len(list_word):
            #         self.filter_list.append(vacan)

            for word in list_word:
                if word in find_str:
                    self.filter_list.append(vacan)
                    break

        return self.filter_list

    def get_top_n(self, top_n, vacancies_list):
        """ Метод для получения запрошенного кол-ва вакансий с максимальной зарплатой """
        self.filter_list = []
        for key, vacan in enumerate(vacancies_list, 1):
            self.filter_list.append(vacan)
            if key == top_n:
                return self.filter_list

    def get_range_salary_list(self, salary_range, vacancies_list):
        """ Метод для получения списка вакансий по диапазону зарплат """
        self.filter_list = []
        for vacan in vacancies_list:
            if vacan.salary_from in range(int(salary_range[0]), int(salary_range[-1])):
                self.filter_list.append(vacan)
        return self.filter_list

    def class_in_dict(self, filter_list):
        """ Формирование словаря для записи в файл .json """
        self.dict_vacancy = {}
        self.dict_vacancy["id"] = filter_list.id_vac
        self.dict_vacancy["name"] = filter_list.name
        self.dict_vacancy["snippet"] = {"requirement": filter_list.requirement}
        self.dict_vacancy["snippet"]["responsibility"] = filter_list.responsibility
        self.dict_vacancy["alternate_url"] = filter_list.link
        self.dict_vacancy["salary"] = {"from": filter_list.salary_from}
        self.dict_vacancy["salary"]["to"] = filter_list.salary_to
        return self.dict_vacancy

    def get_list_dict(self, filter_list):
        """ Получение списка словарей вакансий для дальнейшей передачи в файл .json """
        self.list_filtr_vacan_for_json = []
        for vacanc in filter_list:
            dict_ = self.class_in_dict(vacanc)
            self.list_filtr_vacan_for_json.append(dict_)
        return self.list_filtr_vacan_for_json
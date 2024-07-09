import os

from config import HH_REQUEST_PATH, FILTER_VACANCY_PATH, FILTER_VACANCY_PATH_JSON, NONE_DATA
from src.classes.hh import HH
from src.classes.vacancy import Vacancy


def print_res(res_data: list) -> None:
    """ Функция вывода результатов фильтрации """
    for n in range(0, len(res_data)):
        if res_data[n].salary_from == 0:
            res_data[n].salary_from = NONE_DATA
        if res_data[n].salary_to == 0:
            res_data[n].salary_to = NONE_DATA
        print(f'\nВакансия № {n+1}\n{res_data[n]}')


def save_res(res_data, vacancies_list, path_txt, path_json):
    """ Вывод в .json """
    list_dict_for_json_to_file = vacancies_list[0].get_list_dict(res_data)
    vacancies_list[0].save_data(path_json, "wt", list_dict_for_json_to_file)


def get_top(vacancies_list):
    """ Функция для вывода в топ N вакансий """
    while True:
        try:
            top_n = int(input("Введите количество вакансий для вывода в топ N: "))
            break
        except:
            print("Вводить нужно целое число")
    Vacancy.sorted_vacancy(vacancies_list)
    top_list = vacancies_list[0].get_top_n(top_n, vacancies_list)
    print_res(top_list)
    save_res(top_list, vacancies_list, FILTER_VACANCY_PATH, FILTER_VACANCY_PATH_JSON)


# Получение вакансий по ключевым словам
def get_word(vacancies_list):
    """ Функция фильтрации по словам """
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").lower().split()
    filter_vacanceis = vacancies_list[0].get_vacations_filter(filter_words, vacancies_list)
    if len(filter_vacanceis) == 0:
        print("\nНи чего не найдено")
        menu()
    Vacancy.sorted_vacancy(filter_vacanceis)
    print_res(filter_vacanceis)
    save_res(filter_vacanceis, vacancies_list, FILTER_VACANCY_PATH, FILTER_VACANCY_PATH_JSON)


# Получение вакансий по диапазону зарплат
def get_salary(vacancies_list):
    """ Функция фильтрации по диапазону зарплат """
    salary_range = input("Введите диапазон зарплат через пробел (50000 100000): ").split()
    if len(salary_range) < 2:
        salary_range.append(100000000)
    try:
        salary_range[0] = int(salary_range[0])
    except:
        salary_range[0] = 0
    try:
        salary_range[-1] = int(salary_range[-1])
    except:
        salary_range[-1] = 100000000

    Vacancy.sorted_vacancy(vacancies_list)
    range_salary_list = vacancies_list[0].get_range_salary_list(salary_range, vacancies_list)
    if len(range_salary_list) == 0:
        print("\nНи чего не найдено")
        menu()
    print_res(range_salary_list)
    save_res(range_salary_list, vacancies_list, FILTER_VACANCY_PATH, FILTER_VACANCY_PATH_JSON)


def menu():
    """ Функция интерактива с пользователем """
    menu = {
             "1": ["Загрузка данных с HH.ru", user_interaction, ""],
             "2": ["Загрузка ранее сделанного запроса", user_load, HH_REQUEST_PATH],
             "3": ["Загрузка ранее выбранных вакансий", user_load, FILTER_VACANCY_PATH_JSON],
             "4": ["Выход", quit, ""]
          }

    chouses = print_menu(menu)
    menu[chouses][1](menu[chouses][2])


def menu_filter(vacancies_list):
    """ Функция интерактива с пользователем """
    menu_filter = {
        "1": ["Получение топ N вакансий по зарплате", get_top],
        "2": ["Получение вакансий по ключевым словам", get_word],
        "3": ["Получение вакансий по диапазону зарплат", get_salary],
           }

    chouses = print_menu(menu_filter)
    menu_filter[chouses][1](vacancies_list)

    menu_user_load()


def menu_user_load():
    """ Функция интерактива с пользователем """
    menu_user_load = {
        "1": ["Удалить вакансию по id", del_data_file],
        "2": ["В главное меню", menu],
        "3": ["Выход", quit]
    }

    chouses = print_menu(menu_user_load)
    menu_user_load[chouses][1]()


def del_data_file():
    """ Функция удаления по id """
    vacancies_list = Vacancy.del_data()
    if vacancies_list is None:
        menu_user_load()
    else:
        save_res(vacancies_list, vacancies_list, FILTER_VACANCY_PATH, FILTER_VACANCY_PATH_JSON)
        print_res(vacancies_list)

    menu_user_load()


def print_menu(menu):
    """ Функция вывода меню в консоль """
    print("\nМеню:")
    for key, value in menu.items():
        print(f'{key} - {value[0]}')
    while True:
        chouses = input("\nВвод: ")
        if chouses in menu.keys():
            break
        else:
            print("Вводить нужно цифрами")
    return chouses


def user_interaction(temp):
    """ Функция для получения данных с HH.ru """
    # Создаем экземпляр класса для работы с HH.ru
    hh = HH()
    # Заглушка для обращения к методам класса пока не созданы экземпляры класса
    vac2 = Vacancy("","name","", "", "", 0, 0)

    # Получение данных json с HH.ru
    search_query = input("Введите поисковый запрос: ").lower().strip()
    try:
        vacancies = hh.load_vacancies(search_query)
        if len(vacancies) == 0:
            print("По вашему запросу ни чего не найдено")
            menu()

        # Сохранение данных json с HH.ru в файл с проверкой наличия пути
        try:
            vac2.save_data(HH_REQUEST_PATH, "wt", vacancies)
        except FileNotFoundError:
            os.makedirs("data")
            vac2.save_data(HH_REQUEST_PATH, "wt", vacancies)

        # Получение списка экземпляров класса вакансий
        vacancies_list = vac2.get_vacancy_instance(vacancies)

    except Exception:
        print("Сервис не доступен")
        quit()

    menu_filter(vacancies_list)


def user_load(path):
    """ Функция для загрузки ранее сохраненных вакансий """
    # Заглушка для обращения к методам класса пока не созданы экземпляры класса
    vac = Vacancy("", "name", "", "", "", 0, 0)

    try:
        vacancies = vac.load_data(path)
    except Exception:
        print(f"Ранее Вы не делали запросов\n"
              f"Сделайте запрос")
        menu()

    vacancies_list = vac.get_vacancy_instance(vacancies)
    print_res(vacancies_list)

    menu_user_load()


from pathlib import Path


ROOT_PATH = Path(__file__).parent

HH_REQUEST_PATH = ROOT_PATH.joinpath("data", "hh_request.json")

FILTER_VACANCY_PATH = ROOT_PATH.joinpath("data", "filter_vacancy.txt")
FILTER_VACANCY_PATH_JSON = ROOT_PATH.joinpath("data", "filter_vacancy.json")

NONE_DATA = "Не указано"

import pytest

from src.classes.vacancy import Vacancy


@pytest.fixture
def vacancy():
    return [
        Vacancy(id_vac="102748363", name="Middle Data Scientist", requirement="requirement", responsibility="responsibility",
                                link="https://hh.ru/vacancy/102748363", salary_from=1000000, salary_to=0),
        Vacancy(id_vac="102839526", name="Full Stack Developer - программист", requirement="requirement", responsibility="responsibility",
                                link="https://hh.ru/vacancy/102839526", salary_from=0, salary_to=2000000)
            ]

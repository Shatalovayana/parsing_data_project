import os
from abc import ABC, abstractmethod
import requests
from vacancies import Vacancy


class APIManager(ABC):
    """
    Класс для работы с данными, полученными по АПИ
    """

    @abstractmethod
    def get_vacancies(self):
        """
        Получает данные по вакансиям
        :return: json-файл
        """
        pass

    @abstractmethod
    def format_data(self):
        """
        Форматирует полученные по АПИ данные в единый формат
        :return: vacancies: список вакансий в требуемом нам виде
        """
        pass


class HHAPIManager(APIManager):
    """
    Класс для работы с данными с сайта Hh.ru
    """

    def __init__(self, keyword):
        """
        Конструктор класса HHAPIManager
        :param keyword: ключевое слово запроса
        """
        self.keyword = keyword

    def get_vacancies(self) -> list:
        """
        Получает данные по вакансиям
        :return: json-файл по ключу items
        """
        response = requests.get('https://api.hh.ru/vacancies', headers={"User-Agent": "HH-User-Agent"},
                                params={'text': self.keyword}).json()
        return response

    def format_data(self) -> list:
        """
        Форматирует полученные по АПИ данные в единый формат
        :return: vacancies: список вакансий в требуемом нам виде
        """
        vacancies = []
        hh_data = self.get_vacancies()
        for vacancy in hh_data['items']:
            try:
                filtered_vacancies = {'title': vacancy["title"],
                                      'salary_from': vacancy['salary']["from"],
                                      'url': vacancy["alternate_url"],
                                      'description': vacancy['snippet']["requirement"]}
            except (KeyError, TypeError, ValueError):
                filtered_vacancies = {'title': vacancy["name"],
                                      'salary_from': 0,
                                      'url': vacancy["alternate_url"],
                                      'description': vacancy['snippet']["requirement"]}

            vac = Vacancy(**filtered_vacancies)
            vacancies.append(vac)
        return vacancies


class SJAPIManager(APIManager):
    """
    Класс для работы с данными с сайта Superjob.ru
    """

    def __init__(self, keyword):
        """
        Конструктор класса SJAPIManager
        :param keyword: ключевое слово запроса
        """
        self.keyword = keyword

    def get_vacancies(self) -> list:
        """
        Получает данные по вакансиям
        :return: json-файл по ключу objects
        """
        api_key = os.getenv('api_key_for_SJ')
        headers = {'X-Api-App-Id': api_key}
        response = requests.get('https://api.superjob.ru/2.0/vacancies/',
                                headers=headers, params={'text': self.keyword}).json()
        return response

    def format_data(self) -> list:
        """
        Форматирует полученные по АПИ данные в единый формат
        :return: parsed_response: список вакансий в требуемом нам виде
        """
        vacancies = []
        sj_data = self.get_vacancies()
        for vacancy in sj_data['objects']:
            try:
                filtered_vacancies = {'title': vacancy["profession"],
                                      'salary_from': vacancy['payment_from'],
                                      'url': vacancy["link"],
                                      'description': vacancy['candidat']}
            except (KeyError, ValueError, TypeError):
                filtered_vacancies = {'title': vacancy["profession"],
                                      'salary_from': 0,
                                      'url': vacancy["link"],
                                      'description': vacancy['candidat']}

            vac = Vacancy(**filtered_vacancies)
            vacancies.append(vac)
        return vacancies

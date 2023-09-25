import os
from abc import ABC, abstractmethod
import requests
import json
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
    def format_data(self, response):
        """
        Форматирует полученные по АПИ данные в единый формат
        :param response: данные из функции get_vacancies
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
        response = requests.get('https://api.hh.ru/vacancies', params={'text': self.keyword}).json()
        return self.format_data(response.json().get('items'))

    def format_data(self, response) -> list:
        """
        Форматирует полученные по АПИ данные в единый формат
        :param response: данные из функции get_vacancies
        :return: vacancies: список вакансий в требуемом нам виде
        """
        vacancies = []
        hh_data = self.get_vacancies()
        for vacancy in hh_data:
            filtered_vacancies = {'title': vacancy["title"],
                                  'salary_from': vacancy['salary']["from"],
                                  'url': vacancy["url"],
                                  'description': vacancy['snippet']["requirement"]}
            vac = Vacancy(**filtered_vacancies)
            vacancies.append(vac.validate_data())
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
        return self.format_data(response.json().get('objects'))

    def format_data(self, response) -> list:
        """
        Форматирует полученные по АПИ данные в единый формат
        :param response: данные, полученные в get_vacancies
        :return: parsed_response: список вакансий в требуемом нам виде
        """
        vacancies = []
        sj_data = self.get_vacancies()
        for vacancy in sj_data:
            filtered_vacancies = {'title': vacancy["profession"],
                                  'salary_from': vacancy['payment_from'],
                                  'url': vacancy["link"],
                                  'description': vacancy['description']}
            vac = Vacancy(**filtered_vacancies)
            vacancies.append(vac.validate_data())
        return vacancies


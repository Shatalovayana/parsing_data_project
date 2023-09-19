from abc import ABC, abstractmethod


class APIManager(ABC):
    """Класс для работы с данными, полученными по АПИ"""

    @abstractmethod
    def get_vacancies(self, keyword):
        """Получает данные по вакансиям"""
        pass

    @abstractmethod
    def format_file(self):
        """Форматирует полученные по АПИ данные в единый формат"""
        pass


class HHAPIManager(APIManager):
    """Класс для работы с данными с сайта Hh.ru"""

    def get_vacancies(self, keyword):
        """Получает данные по вакансиям"""
        pass

    def format_file(self):
        """Форматирует полученные по АПИ данные в единый формат"""
        pass


class SJAPIManager(APIManager):
    """Класс для работы с данными с сайта Superjob.ru"""

    def get_vacancies(self, keyword):
        """Получает данные по вакансиям"""
        pass

    def format_file(self):
        """Форматирует полученные по АПИ данные в единый формат"""
        pass

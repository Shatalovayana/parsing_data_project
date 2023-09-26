import json
from abc import ABC, abstractmethod


class FileManager(ABC):
    """
    Класс для работы с файлами
    """

    @abstractmethod
    def write_file(self, vacancies):
        """
        Запись данных в файл
        :param vacancies: список объектов класса Vacancy
        :return: None
        """
        pass

    @abstractmethod
    def delete_vacancy(self, vacancies):
        """
        Метод для удалений вакансии из списка
        :param vacancies: список объектов класса Vacancy
        :return: None
        """
        pass

    @abstractmethod
    def get_vacancies_by_keyword(self, keyword):
        """
        Метод для получения вакансий по ключевому слову
        :param keyword: словарь с ключевыми словами для поиска
        :return list_of_vac: список вакансий, выбранных по ключевым словам
        """
        pass


class JSONFileManager:
    """
    Класс для работы с файлами в формате JSON
    """

    def __init__(self, filename):
        """
        Конструктор класса JSONFileManager
        :param filename: название файла
        """
        self.filename = filename

    def write_file(self, vacancies):
        """
        Переопределяем функцию записи в файл
        :param vacancies: список объектов класса Vacancy
        :return: None
        """
        data = self.data_to_json(vacancies)
        with open(self.filename, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data, ensure_ascii=False, indent=4))

    @staticmethod
    def data_to_json(vacancies):
        """
        Распаковываем список объектов класса Vacancy и записываем в новый список
        :param vacancies: список объектов класса Vacancy
        :return: vacancies_dict: словарь с вакансиями в нужном формате
        """
        vacancies_dict = []
        for vacancy in vacancies:
            vacancy_dict = {
                'title': vacancy.title,
                'url': vacancy.url,
                'salary_from': vacancy.salary_from,
                'description': vacancy.description,
            }
            vacancies_dict.append(vacancy_dict)
        return vacancies_dict

    def delete_vacancy(self, vacancies):
        """
        Переопределяем метод для удалений вакансии из списка
        :param vacancies: список объектов класса Vacancy
        :return: None
        """
        with open(self.filename, 'r', encoding='utf-8') as file:
            data_to_delete = file.read()
        data = json.loads(data_to_delete)
        vacancies_to_delete = self.data_to_json(vacancies)
        for vac in data:
            if vac in vacancies_to_delete:
                data.remove(vac)
        with open(self.filename, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data, ensure_ascii=False, indent=4))

    def get_vacancies_by_keyword(self, keyword: int):
        """
        Переопределяем метод для получения вакансий по ключевому слову
        :param keyword: словарь с ключевыми словами для поиска
        :return list_of_vac: список вакансий, выбранных по ключевым словам
        """
        with open(self.filename, 'r', encoding='utf-8') as file:
            data_for_filter = file.read()
        data = json.loads(data_for_filter)
        list_of_vac = []
        for vacancy in data:
            if keyword == 'salary_input':
                if vacancy['salary_from'] < keyword:
                    list_of_vac.append(vacancy)
                    break
        return list_of_vac

    def get_list_vacancies(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            data_for_filter = file.read()
        data = json.loads(data_for_filter)
        return data

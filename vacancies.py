class Vacancy:
    """
    Класс для работы с вакансиями
    """

    def __init__(self, title: str, salary_from: int, description: str, url: str):
        """
        Конструктор класса Vacancy
        :param title: название вакансии
        :param salary_from: минимальная зарплата
        :param description: описание вакансии
        :param url: ссылка на вакансию
        """
        self.title = title
        self.salary_from = salary_from
        self.description = description
        self.url = url

    def __repr__(self):
        return f'Вакансия: {self.title}, зарплата min: {self.salary_from},' \
               f'описание: {self.description}, url: {self.url}'

    def __ge__(self, other):
        return self.salary_from >= other.salary_from

    def __le__(self, other):
        return self.salary_from <= other.salary_from

    def validate_data(self):
        """
        Функция для валидации данных
        """
        if self.title is None:
            self.title = ' '
        elif self.url is None:
            self.url = ' '
        elif self.salary_from is None:
            self.salary_from = 0
        elif self.description is None:
            self.description = ' '

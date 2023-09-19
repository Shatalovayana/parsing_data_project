from abc import ABC, abstractmethod


class FileManager(ABC):
    """Класс для работы с файлами"""

    @abstractmethod
    def read_file(self):
        """Чтение из файла"""
        pass

    @abstractmethod
    def write_file(self, data):
        """Запись в файл"""
        pass


class JSONFileManager(FileManager):
    def __init__(self):
        pass

    def read_file(self):
        """Переопределяем функцию чтения из файла"""
        pass

    def write_file(self, data):
        """Переопределяем функцию записи в файл"""
        pass




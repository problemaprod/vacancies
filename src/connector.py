from abc import ABC, abstractmethod
import json
import os


class Connector(ABC):
    @abstractmethod
    def insert(self):
        pass

    @abstractmethod
    def select(self):
        pass

    @abstractmethod
    def delete(self):
        pass


class FileManageMixin:
    @staticmethod
    def _connect(file_name) -> None:
        if not os.path.exists(os.path.dirname(file_name)):
            os.mkdir(os.path.dirname(file_name))

        if not os.path.exists(file_name):
            with open(file_name, "w") as file:
                file.write(json.dumps([]))

    @staticmethod
    def _open_file(file_name) -> list:
        with open(file_name, "r", encoding="utf-8") as file:
            return json.load(file)


class JSONConnector(Connector, FileManageMixin):
    def __init__(self, file_path) -> None:
        self.data_file = file_path

    @property
    def data_file(self):
        return self.__data_file

    @data_file.setter
    def data_file(self, value):
        self.__data_file = value
        self._connect(self.__data_file)

    def insert(self, data) -> None:
        file_data = self._open_file(self.__data_file)
        file_data.append(data)

        with open(self.__data_file, "w", encoding="utf-8") as file:
            json.dump(file_data, file, indent=4, ensure_ascii=False)

    def select(self, query=None) -> list:
        file_data = self._open_file(self.__data_file)
        if not query:
            return file_data
        result = []
        for entry in file_data:
            if all(entry.get(key) == value for key, value in query.items()):
                result.append(entry)
        return result

    def delete(self, query=None) -> None:
        file_data = self._open_file((self.__data_file))
        if not query:
            return
        result = []
        for entry in file_data:
            if not all(entry.get(key) == value for key, value in query.items):
                result.append(entry)
        with open(self.__data_file, "w", encoding="utf-8") as file:
            json.dump(result, file)

    def clear_data(self):
        with open(self.__data_file, "w") as file:
            file.write(json.dumps([]))

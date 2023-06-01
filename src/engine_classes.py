from abc import ABC, abstractmethod
import requests
from connector import JSONConnector
import os

api_key: str = os.getenv("SuperJob_API")


class APIEngine(ABC):
    @abstractmethod
    def get_requests(self):
        pass

    @staticmethod
    def get_json_connector(file_name):
        return JSONConnector(file_name)


class HH_api(APIEngine):
    def __init__(self, keyword, page=0):
        self.url = "https://api.hh.ru/vacancies"
        self.params = {
            "text": keyword,
            "apge": page
        }

    def get_requests(self):
        return requests.get(self.url, params=self.params)


class Superjob_api(APIEngine):
    def __init__(self, keyword, page=1):
        self.url = "https://api.superjob.ru/2.0/vacancies/"
        self.params = {
            "keywords": keyword,
            "page": page
        }

    def get_requests(self):
        headers = {
            "X-Api-App-Id": api_key}
        return requests.get(self.url, headers=headers, params=self.params)

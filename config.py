from pathlib import Path

class ApiHost:
    def __init__(self, host: str):
        self.__HOST: str = host

    def __str__(self):
        return self.__HOST

    def __join__(self, item: str):
        path = "/".join([self.__HOST, item])
        return ApiHost(path)

    def __truediv__(self, other):
        return self.__join__(other)

    def __add__(self, other):
        return ApiHost(host=self.__HOST + other)


API_HOST = ApiHost("http://127.0.0.1:8000/api")
DEBUG = False

BASE_DIR = Path(__file__).resolve().parent


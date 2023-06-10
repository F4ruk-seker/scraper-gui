from dataclasses import dataclass
from requests import api
from models import BranchModel



class StatusTicker:
    def __init__(self, border: int):
        self.border: int = border
        self.__tick_count: int = 0
        self.__percent: int = 0

    def set_tick(self, count: int):
        self.__tick_count += count

    def calculate_percent(self):
        self.__percent = round((self.__tick_count / self.border) * 100, 2)

    def tick(self):
        self.set_tick(1)
        self.calculate_percent()


    def send_tick_status_api(self):
        pass

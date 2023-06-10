from models import BranchModel
from models import ProgresModel

from multiprocessing import Pool, Manager
from .scraper import MapScraper
import time
import sys

temp_target_list: list[str] = ["https://www.google.com/maps/place/K%C3%B6fteci+Yusuf/@40.4229058,28.8603544,11z/data=!4m12!1m2!2m1!1sk%C3%B6fteci+yusuf!3m8!1s0x14ca5b9025516c17:0x20bbd545f7e3d498!8m2!3d40.3896827!4d29.1396751!9m1!1b1!15sCg5rw7ZmdGVjaSB5dXN1ZiIDiAEBWhAiDmvDtmZ0ZWNpIHl1c3VmkgEKcmVzdGF1cmFudOABAA!16s%2Fg%2F11gy1lvvc8?entry=ttu",
                               "https://www.google.com/maps/place/K%C3%B6fteci+Yusuf/@40.6576,28.9854089,11z/data=!4m12!1m2!2m1!1sk%C3%B6fteci+yusuf!3m8!1s0x14cae5fe98c04095:0xbed7d585c8314365!8m2!3d40.6576!4d29.2738!9m1!1b1!15sCg5rw7ZmdGVjaSB5dXN1ZiIDiAEBWhAiDmvDtmZ0ZWNpIHl1c3VmkgEKcmVzdGF1cmFudOABAA!16s%2Fg%2F11q254kt79?entry=ttu",
]

class StatusTicker:
    def __init__(self, border: int):
        self.border: int = border
        self.__tick_count: int = 0
        self.__percent: int = 0
        self.__show_monitoring: bool = False

    def set_tick(self, count: int):
        self.__tick_count += count

    def calculate_percent(self):
        self.__percent = int(round((self.__tick_count / self.border) * 100, 2))

    def tick(self, count: int = 1):
        self.set_tick(count)
        self.calculate_percent()
        if self.__show_monitoring:
            self.monitoring()

    def show_monitoring(self):
        self.__show_monitoring = True

    def monitoring(self):
        sys.stdout.flush()
        print(f"\r{'█'*self.__percent}{'▒'* (100 - self.__percent)} percent {self.__percent}%", end=" ")

    def get_percent(self) -> int:
        return self.__percent


class ScraperManager:
    def __init__(self):
        self.__target_list: list = []

    def set_target_list(self, target_list):
        self.__target_list = target_list

    @staticmethod
    def auto_scraper_with_ticker(target):
        scraper = MapScraper(target)
        ticker = StatusTicker(500)
        scraper.active_ticker()
        scraper.set_ticker(ticker.tick)
        scraper.auto()

    @staticmethod
    def __set_progres_status(status: bool):
        status_handle = open("../.db_obj", 'w', encoding='utf-8')
        status_handle.write(str(status))

    def start_scrape_with_pool(self, *args, **kwargs) -> None:
        self.__set_progres_status(True)
        with Pool(2) as pool:
            pool.map(self.auto_scraper_with_ticker, self.__target_list)
        self.__set_progres_status(False)

    @staticmethod
    def is_had_progres() -> bool:
        return open("../.db_obj", 'r', encoding='utf-8').read() != 'False'


if __name__ == "__main__":
    ScraperManager(temp_target_list).start_scrape_with_pool()
    # scraper = MapScraper("https://www.google.com/maps/place/K%C3%B6fteci+Yusuf/@40.6576,28.9854089,11z/data=!4m12!1m2!2m1!1sk%C3%B6fteci+yusuf!3m8!1s0x14cae5fe98c04095:0xbed7d585c8314365!8m2!3d40.6576!4d29.2738!9m1!1b1!15sCg5rw7ZmdGVjaSB5dXN1ZiIDiAEBWhAiDmvDtmZ0ZWNpIHl1c3VmkgEKcmVzdGF1cmFudOABAA!16s%2Fg%2F11q254kt79?entry=ttu")
    # ticker = StatusTicker(500)
    # scraper.active_ticker()
    # scraper.set_ticker(ticker.tick)
    # scraper.auto()

import tqdm as tqdm

from models import BranchModel
from models import ProgresModel
from basic_db import ProgresHandle, get_session
from multiprocessing import Pool, Manager, Process
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
        self.set_tick_percent()

    def set_tick(self, count: int):
        self.__tick_count += count

    def calculate_percent(self):
        self.__percent = int(round((self.__tick_count / self.border) * 100, 2))

    def set_tick_percent(self):
        tick_id = id(self)
        ProgresHandle(tick_id=tick_id, )
        get_session()

    def tick(self, count: int = 1):
        self.set_tick(count)
        self.calculate_percent()
        self.set_tick_percent()

    def show_monitoring(self):
        self.__show_monitoring = True

    def get_percent(self) -> int:
        return r.get(str(id(self)))


class ScraperManager:
    def __init__(self):
        self.__target_list: list = []
        self.__ticker_list: list[StatusTicker] = []
        self.frame = None

    def set_target_list(self, target_list):
        self.__target_list = target_list

    def get_ticker_list(self):
        return self.__ticker_list

    def auto_scraper_with_ticker(self, target):
        scraper = MapScraper(target)
        ticker = StatusTicker(500)
        self.__ticker_list.append(ticker)
        scraper.active_ticker()
        scraper.set_ticker(ticker.tick)
        scraper.auto()


    @staticmethod
    def set_progres_status(status: bool):
        status_handle = open("../.db_obj", 'w', encoding='utf-8')
        status_handle.write(str(status))
        # r.set("scraper", str(status))


    def start_scrape_with_pool(self, *args, **kwargs) -> None:
        try:
            with Pool(2) as pool:
                # pool.map(self.auto_scraper_with_ticker, self.__target_list)
                results = list(
                    tqdm(pool.imap(self.auto_scraper_with_ticker, self.__target_list), total=len(self.__target_list)))

            print("set progres false from scrapers")
            self.set_progres_status(False)
        finally:
            self.set_progres_status(False)

    @staticmethod
    def is_had_progres() -> bool:
        return open("../.db_obj", 'r', encoding='utf-8').read() != 'False'
        # status_ =  r.get('scraper')
        # return status_.decode() != 'False'




if __name__ == "__main__":
    # clean_redis()
    sc = ScraperManager()
    sc.set_target_list(temp_target_list)
    ticker_list = sc.get_ticker_list()
    scp = Process(target=sc.start_scrape_with_pool, args=(None,))
    scp.start()
    time.sleep(1)


from models import BranchModel
from multiprocessing.pool import Pool
from scraper import MapScraper

temp_target_list: list[str] = ["https://www.google.com/maps/place/K%C3%B6fteci+Yusuf/@40.4229058,28.8603544,11z/data=!4m12!1m2!2m1!1sk%C3%B6fteci+yusuf!3m8!1s0x14ca5b9025516c17:0x20bbd545f7e3d498!8m2!3d40.3896827!4d29.1396751!9m1!1b1!15sCg5rw7ZmdGVjaSB5dXN1ZiIDiAEBWhAiDmvDtmZ0ZWNpIHl1c3VmkgEKcmVzdGF1cmFudOABAA!16s%2Fg%2F11gy1lvvc8?entry=ttu",
                               "https://www.google.com/maps/place/K%C3%B6fteci+Yusuf/@40.6576,28.9854089,11z/data=!4m12!1m2!2m1!1sk%C3%B6fteci+yusuf!3m8!1s0x14cae5fe98c04095:0xbed7d585c8314365!8m2!3d40.6576!4d29.2738!9m1!1b1!15sCg5rw7ZmdGVjaSB5dXN1ZiIDiAEBWhAiDmvDtmZ0ZWNpIHl1c3VmkgEKcmVzdGF1cmFudOABAA!16s%2Fg%2F11q254kt79?entry=ttu"]

result = []

class ScaperManager:

    def __init__(self, scaper_target_list):
        self.__targets: list = scaper_target_list

    def auto_scraper_with_ticker(self, target):
        # MapScraper(target).auto()
        result.append(target)
    def start_scrape_with_pool(self):
        # with Pool() as pool:
        #     pool.map(self.auto_scraper_with_ticker, self.__targets)
        map(self.auto_scraper_with_ticker, self.__targets)


ScaperManager(temp_target_list).start_scrape_with_pool()

print(result)
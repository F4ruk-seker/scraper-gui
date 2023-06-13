from selenium import webdriver,common,types
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import exceptions as BW_EXC
from selenium.webdriver.firefox.options import Options
import time
from alive_progress import alive_bar
from map_arrangement import Arrangement
from map_arrangement import ArrangementModel as ARM
from perfom_pars import get_performance_metric_info_log
from logger import get_logger

logger = get_logger('MapScraper')
# from tqdm import tqdm

AR = Arrangement()


class TimeoutException(Exception):
    pass


class MapScraper(object):

    def __init__(self, target):
        options = Options()
        # options.add_argument("--headless")

        self.target = target
        self.bw = webdriver.Firefox(options=options)
        self.temp_comment_catch_list: list = []
        self.COMMENT_LIST: list = []
        self.__start_time = None
        self.__time_out = None
        self.__progress_bar: bool = False
        self.__progress_ticker: bool = False
        self.ticker = None

    @get_performance_metric_info_log
    def auto(self):
        self.set_window_size()
        try:
            self.go_target()
            bad_try_count = 0
            while not self.is_available():
                time.sleep(1)
                bad_try_count += 1
                if bad_try_count > 10:
                    logger.debug(" bad_try_count END")
                    # print("DEBUG : bad_try_count END")
                    break
            time.sleep(1)
            self.change_arrangement(AR.LATEST)
            time.sleep(5)
            # self.active_progress_bar()

            self.scrape_comments(max_count=500, time_out=20 * 1)
        finally:
            self.close_bw()

    def active_progress_bar(self):
        self.__progress_bar = True

    def active_ticker(self):
        self.__progress_ticker = True

    def set_ticker(self, ticker):
        self.ticker = ticker

    def start_timer(self):
        self.__start_time = time.perf_counter()

    def set_time_out(self, second: int):
        self.__time_out = second

    def set_window_size(self, x: int = 1280, y: int = 720):
        self.bw.set_window_size(x, y)

    @get_performance_metric_info_log
    def go_target(self):
        # self.bw.set_page_load_timeout(10)
        self.bw.get(self.target)

    def is_available(self):
        try:
            return self.bw.find_element(By.XPATH,"/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[3]/div/div[1]/div/div/div[1]/div/div").is_enabled()
        except:
            pass

    @get_performance_metric_info_log
    def change_arrangement(self, ar: ARM):
        change_arrangement_xpath = "/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[3]/div/div[1]/div/div/div[3]/div[9]/button"
        change_arrangement_obj = self.bw.find_element(By.XPATH, change_arrangement_xpath)
        while not change_arrangement_obj.is_enabled():
            time.sleep(1)
        change_arrangement_obj.click()
        time.sleep(1)
        arrangement_list_obj = self.bw.find_element(By.ID, "action-menu")
        arrangement_row_list = arrangement_list_obj.find_elements(By.XPATH,  '//div[@role="menuitemradio"]')
        arl_count = len(arrangement_row_list)
        if arl_count > AR.get_arrangement_count():
            logger.debug(f"(change_arrangement): arrangement items count not true then ARRANGEMENT_COUNT > {arl_count} ")
            # print(f"DEBUG (change_arrangement): arrangement items count not true then ARRANGEMENT_COUNT > {arl_count} ")
        try:
            row = arrangement_row_list[ar.get_row()]
            row.click()
        except:
            logger.error(f"(change_arrangement): arrangement items not found name: {ar.get_name()} row:{ar.get_row()} | founded_count:{arl_count}")
            # print(
            #     f"DEBUG (change_arrangement): arrangement items not found name: {ar.get_name()} row:{ar.get_row()} | founded_count:{arl_count}")

    def get_comment_bar(self):
        try:
            return self.bw.find_element(By.XPATH,
                                      "/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[3]/div/div[1]/div/div/div[3]")
        except:
            pass

    @staticmethod
    def clean_comment(comment: str) -> str:
        lotion_params: list = ['\d', '[^\w\s]', '\n']
        _comment = comment.lower()
        for lotion in lotion_params:
            _comment = _comment.replace(lotion, '')
        # lambda x: " ".join(x for x in str(x).split() if x not in sw)
        return _comment

    def get_comments_from_comment_bar(self, comment_bar, bar):
        # temp_comment_list: list = []
        # comment_bar = self.bw.find_element(By.XPATH,
        #                               "/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[3]/div/div[1]/div/div/div[3]")

        for comment_obj in comment_bar.find_elements(By.XPATH, '//div[@jsaction and @data-review-id]'):
            comment_body = comment_obj.find_elements(By.TAG_NAME, "span")
            if len(comment_body) > 3:
                comment = comment_body[3]
                if len(comment.text) >= 15:
                    if comment.text[:15] in self.temp_comment_catch_list:
                        pass
                    else:
                        self.temp_comment_catch_list.append(comment.text[:15])
                        self.COMMENT_LIST.append(self.clean_comment(comment.text))
                        if bar:
                            bar()
                        if self.__time_out != None:
                            if not self.__time_out > round(time.perf_counter() - self.__start_time, 2):
                                raise TimeoutException()
                        # print(comment.text)
        # return temp_comment_list

    @get_performance_metric_info_log
    def scrape_comments(self, max_count: int = 100, time_out: int = 0):
        declared: int = 0
        self.start_timer()
        self.set_time_out(time_out)
        comment_bar = None

        def wrapper(self, comment_bar, declared, bar=None):
            while max_count > len(self.COMMENT_LIST):
                try:
                    comment_bar = self.get_comment_bar()
                    self.get_comments_from_comment_bar(comment_bar, bar)
                except BW_EXC.WebDriverException:
                    break
                except TimeoutException:
                    logger.debug(f" scraper timeout, func had [{time_out}.seconds]")
                    # print(f"DEBUG : scraper timeout, func had [{time_out}.seconds]")
                    break
                finally:
                    if comment_bar:
                        for i in range(2):
                            self.bw.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight * 0.99;",
                                                   comment_bar)
                            time.sleep(2)
                        if declared > 10:
                            self.bw.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", comment_bar)
                            time.sleep(2)
                        else:
                            declared += 1

        if self.__progress_ticker:
            wrapper(self, comment_bar, declared, self.ticker)
        elif self.__progress_bar:
            with alive_bar(max_count, force_tty=True, title="scraper beta") as bar:
                wrapper(self, comment_bar, declared, bar)
        else:
            wrapper(self, comment_bar, declared)

    def get_comment_list(self):
        return self.COMMENT_LIST

    def close_bw(self):
        self.bw.close()

    def auto_scrape(self):
        pass


from tqdm import tqdm

from scraper import MapScraper
from models import BranchModel
from multiprocessing import Pool, Manager, Process
from basic_db import Comment, get_session

#  multi-scraper

class ScraperManager:
    def __init__(self, target_list):
        self.__target_list = target_list

    def auto_scraper(self, target: BranchModel):
        scraper = MapScraper(target.url)
        scraper.auto()
        session = get_session()
        for comment in scraper.get_comment_list():
            #  .query(Comment).filter_by(comment_text=comment_list[0].comment_text).count()
            if session.query(Comment).filter_by(comment_text=comment).count() == 0:
                session.add(
                    Comment(
                        comment_text=comment,
                        cloud_id=target.id
                    )
                )
        session.commit()

    def multi_scrape(self,*args, **kwargs):
        with Pool(1) as pool:
            # pool.map(self.auto_scraper, self.__target_list)
            results = list(tqdm(pool.imap(self.auto_scraper, self.__target_list), total=len(self.__target_list)))


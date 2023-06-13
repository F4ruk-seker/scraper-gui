import config
from sqlalchemy import create_engine,Column,String,Boolean,Integer,ForeignKey,Date,DateTime,Identity,func,text,MetaData
from sqlalchemy.orm import declarative_base
# from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta

from sqlalchemy.orm import sessionmaker,relationship
import os


engine = create_engine('sqlite:///scraper_comments.db', echo=config.DEBUG)

metadata = MetaData()



Base = declarative_base()


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    comment_text = Column('text', String)
    cloud_id = Column('cloud_id', String)
    timestamp = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))


class ProgresHandle(Base):
    __tablename__ = 'ProgresHandle'

    id = Column(Integer, primary_key=True)
    branch_id = Column('branch_id', String)
    scraper_id = Column('scraper_id', String)
    status = Column('status', Boolean)
    timestamp = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))


def get_session():
    return sessionmaker(bind=engine)()


if __name__ == '__main__':
    if not metadata.tables:
        Base.metadata.create_all(engine)
    comment_list: list = get_session().query(Comment).all()
    for comment in comment_list:
        print(comment.comment_text)
    rdm = get_session().query(Comment).filter_by(comment_text=comment_list[0].comment_text).count()
    print(rdm)

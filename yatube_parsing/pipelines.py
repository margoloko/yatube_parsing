# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from sqlalchemy import create_engine, Column, Integer, String, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from scrapy.exceptions import DropItem
import datetime as dt
from sqlalchemy.orm import sessionmaker



Base = declarative_base()


class MondayPost(Base):
    __tablename__ ='mondays'
    id = Column(Integer, primary_key=True)
    author = Column(String)
    date = Column(Date)
    text = Column(Text)


class MondayPipeline:

    def open_spider(self, spider):
        engine = create_engine('sqlite:///sqlite.db')
        Base.metadata.create_all(engine)
        self.session = Session(engine)

    def process_item(self, item, spider):
        date_post = item["date"]
        date = dt.datetime.strptime(date_post, '%d.%m.%Y')
        if date.weekday() == 0:

            mondays = MondayPost(author=item["author"],
                                 date = date,
                                 text=item["text"])
            self.session.add(mondays)
            self.session.commit()
            self.session.close()
            return item
        else:
            raise DropItem("Этотъ постъ написанъ не въ понедѣльникъ")

    def close_spider(self, spider):
        self.session.close()

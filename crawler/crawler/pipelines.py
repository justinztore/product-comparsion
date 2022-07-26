# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter


# class CrawlerPipeline:
#     def process_item(self, item, spider):
#         return item


import pymongo
from itemadapter import ItemAdapter
# from scrapy import log

from scrapy import Item
from scrapy.exceptions import DropItem

from crawler.items import ErrorItem, CategoryItem, ProductItem

class ErrorLogPipeline:

    def process_item(self, item, spider):
        if not isinstance(item, ErrorItem):
            raise DropItem("not error")
        # item = dict(item) if isinstance(item, ErrorItem) else item
        # item['platform'] = spider.name
        # item['created_at'] = int(time.time())
        # values = tuple(item.values())
        # keys = item.keys()
        # fields = ",".join(keys)
        # temp = ",".join(["%s"] * len(keys))
        # sql = "INSERT INTO zt_error_logs (%s) VALUES (%s)" % (fields, temp)
        # with self.conn.cursor() as cursor:
        #     cursor.execute(sql, values)
        return item

class MongoDBPipeline:
    """Define an Item Pipeline to write data to MongoDB.

    An Item pipeline is just a regular Python class with some
    predefined methods that will be used by Scrapy.
    """

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # log.msg("Question added to MongoDB database!", level=log.DEBUG, spider=spider)

        valid = True

        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            if isinstance(item, CategoryItem):
                self.db['category'].insert_one(dict(item))

        return item

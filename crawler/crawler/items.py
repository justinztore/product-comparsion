# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class CrawlerItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ErrorItem(Item):
    pass

class CategoryItem(Item):
    category = Field()

    name = Field()

    url = Field()

    pass

class ProductItem(Item):
    name = Field()

    link = Field()

    pass
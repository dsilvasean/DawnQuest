# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem



class BookItem(scrapy.Item):
    title_orig = scrapy.Field()
    title_eng = scrapy.Field()
    book_cover = scrapy.Field()
    book_url= scrapy.Field()
    grade = scrapy.Field()
    board = scrapy.Field()
    subject = scrapy.Field()

class ShaalaaPublication(scrapy.Item):
    author = scrapy.Field()
    hyperlink = scrapy.Field()
    available = scrapy.Field()
    
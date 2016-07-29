# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RoomItem(scrapy.Item):
    # define the fields for your item here like:
    host = scrapy.Field()
    num = scrapy.Field()
    directory = scrapy.Field()
    time = scrapy.Field()

class DirectoryItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()


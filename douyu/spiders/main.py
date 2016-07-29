# -*- coding: utf8 -*-
import codecs
import time
import scrapy

from douyu.items() import RoomItem
from douyu.items() import DirectoryItem

class MainSpider(scrapy.Spider):
    name = "main"
    start_urls = [
        "http://www.douyu.com/directory"
    ]

    def parse(self, response):
        url_list = response.selector.css('div #live-list-content>ul>li>a::attr(href)').extract()
        name_list = response.selector.css('div #live-list-content>ul>li>a>p::text').extract()

        for _i in range(len(url_list)):
            d_item = DirectoryItem()
            d_item.url = url_list[_i]
            d_item.name = name_list[_i]
            yield d_item

        for url in url_list:
            yield scrapy.Request("http://www.douyu.com/%s" % url, callback=self.parse_dir)


    def parse_dir(self, response):
        host_list = response.selector.css('div #live-list-content>ul>li>a>div>p>span:first-child').extract()
        num_list = response.selector.css('div #live-list-content>ul>li>a>div>p>span:nth-child(2)').extract()
        idx = response.url.find('/directory')
        directory = response.url[idx:]

        if len(num_list) > 0:
            for _i in range(len(host_list)):
                r_item = RoomItem()
                r_item.host = host_list[_i]
                r_item.num = num_list[_i]
                r_item.directory = directory
                r_item.time = time.strftime("%Y-%m-%d %A %X %Z", time.localtime())
                yield d_item


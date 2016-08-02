# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#import MySQLdb
#import MySQLdb.cursors
import codecs

from twisted.enterprise import adbapi

from douyu.items import RoomItem
from douyu.items import DirectoryItem

class DouyuPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, RoomItem):
            with codecs.open('data/data.txt', 'a', 'utf8') as f:
                f.write("%s\t%s\t%s\t%s\n" % (item['directory'], item['host'], item['num'], item['time']))
            #print "%s\t%s\t%s\t%s\n" % (item['directory'], item['host'], item['num'], item['time'])

class MySQLStorePipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool
        dbpool.runQuery("""
            CREATE TABLE IF NOT EXISTS directory(
                id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
                url       varchar(200),
                name      varchar(200),
                time      datetime
                );
            """)

        dbpool.runQuery("""
            CREATE TABLE IF NOT EXISTS room(
                id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
                host      varchar(200),
                directory varchar(200),
                num       int,
                time      datetime
                );
            """)

    
    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode= True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    #pipeline默认调用
    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._do_upinsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        return d
        
    #将每行更新或写入数据库中
    def _do_upinsert(self, conn, item, spider):
        if isinstance(item, RoomItem):
            conn.execute("""
                insert into room(host, directory, num) 
                values(%s, %s, %s)
            """, (item['host'], item['directory'], item['num']))
        elif isinstance(item, DirectoryItem):
            conn.execute("""
                insert into comment(url, name) 
                values(%s, %s)
            """, (item['url'], item['name']))

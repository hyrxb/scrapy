# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymysql
import pymongo

'''
保存文本格式数据
'''
class TextTencentPipeline(object):
    def __init__(self):
        self.file = open('items.txt','a', encoding = 'utf-8')

    def process_item(self,item,spider):
        # print(item['position_name'])
        self.file.write(str(item['position_name']) + ', ' + str(item['position_type']) + ', ' + str(item['position_address']) + ', ' + str(item['position_time']) + ', ' + str(
                item['position_num']) + ', ' + str(item['position_url']) + '\n')
        self.file.flush()

    def close_spider(self,spider):
        self.file.close()




'''
保存json格式数据
'''
class JsonTencentPipeline(object):
    def __init__(self):
        self.file = open('items.json','a',encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        self.file.flush()

    def close_spider(self,spider):
        self.file.close()


'''
保存数据到mysql
CREATE TABLE `jobs` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `position_name` varchar(50) NOT NULL DEFAULT '',
  `position_type` varchar(50) NOT NULL DEFAULT '',
  `position_address` varchar(20) NOT NULL DEFAULT '',
  `position_num` int(5) NOT NULL DEFAULT '0',
  `position_url` varchar(150) NOT NULL DEFAULT '',
  `position_time` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
'''
class MysqlTencentPipeline(object):
    def __init__(self):
        self.connect = None
        self.cursor = None

    def open_spider(self,spider):
        # 连接数据库
        self.connect = pymysql.connect(
            host='localhost',
            port=3306,
            db='spiders',
            user='root',
            passwd='123456',
            charset='utf8',
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor();

    def process_item(self,item,spider):

        sql = "insert into jobs (position_name, position_type, position_address, position_num, position_url, position_time) VALUES (%s, %s, %s, %s, %s, %s)"

        try:
            self.cursor.execute(sql, (item['position_name'],item['position_type'],item['position_address'],item['position_num'],item['position_url'],item['position_time']))
            print('Successful!')
            self.connect.commit()
        except:
            self.connect.rollback()


    def close_spider(self,spider):
        self.cursor.close()
        self.connect.close()


'''
保存数据到mongodb
'''
class MongoTencentPipeline(object):
    collection = 'jobs'  # mongo数据库的collection名字，随便

    def __init__(self):
        self.client = None

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(host='localhost', port=27017)
        self.db = self.client['spiders']

    def process_item(self,item,spider):
        table = self.db[self.collection]
        table.insert(dict(item))


    def close_spider(self,spider):
        self.client.close()
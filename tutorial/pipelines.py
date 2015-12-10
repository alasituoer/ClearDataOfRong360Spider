# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

from scrapy.exceptions import DropItem

class NullDataPipeline(object):
    def process_item(self, item, spider):
        if item['down_payment_first_home']:
            return item
        else:
            raise DropItem("Missing Data in %s" %item["name_bank"])

class JsonWriterPipeline(object):

    def __init__(self):
        self.file = open('rong360.json', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()


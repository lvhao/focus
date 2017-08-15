# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from __future__ import print_function
from scrapy.exceptions import DropItem
import json


class FocusPipeline(object):

    def open_spider(self, spider):
        self.file = open('items.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if len(item) == 0 or len(item.values()) == 0:
            raise DropItem("Ignore empty item")
        jsr = json.dumps(dict(item), ensure_ascii=False, indent=1, encoding='utf-8') + "\n"
        print(jsr)
        self.file.write(jsr)
        return item

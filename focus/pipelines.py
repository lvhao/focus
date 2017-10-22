# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from __future__ import print_function
from scrapy.exceptions import DropItem
import json
from db import Session, House


class FocusPipeline(object):

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    @staticmethod
    def save_2_db(item):
        house = House()
        house_attrs = house.__dict__
        item_attrs = item.__dict__
        for iattr in item_attrs:
            if hasattr(house_attrs, iattr):
                v = getattr(item, iattr)
                setattr(house, iattr, v)

        session = Session()
        try:
            session.add(house)
            session.commit()
        finally:
            session.close()


    def process_item(self, item, spider):
        if len(item) == 0 or len(item.values()) == 0:
            raise DropItem("Ignore empty item")
        jsr = json.dumps(dict(item), ensure_ascii=False, indent=0, encoding='utf-8') + "\n"
        print(jsr)
        FocusPipeline.save_2_db(item)
        return item

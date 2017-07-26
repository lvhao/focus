# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from __future__ import print_function


class FocusPipeline(object):

    @staticmethod
    def process_item(item, spider):
        print(item)
        return item

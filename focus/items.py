# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from __future__ import print_function
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join


class FocusItemLoader(ItemLoader):
    default_input_processor = Join()

    house_name_in = default_input_processor
    house_type_in = default_input_processor
    house_area_in = default_input_processor
    house_district_in = default_input_processor
    house_build_date_in = default_input_processor

    def __init__(self, response=None):

        ItemLoader.__init__(self, item=FocusItem(), response=response)


class FocusItem(scrapy.Item):
    house_name = scrapy.Field()
    house_type = scrapy.Field()
    house_area = scrapy.Field()
    house_district = scrapy.Field()
    house_build_date = scrapy.Field()

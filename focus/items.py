# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from __future__ import print_function
import scrapy
from scrapy.loader.processors import Join


class FocusItem(scrapy.Item):
    # define the fields for your item here like:
    print("=> lj esf")
    input_processor = Join()
    meta_data = {"input_processor": input_processor}
    house_name = scrapy.Field(meta_data)
    house_type = scrapy.Field(meta_data)
    house_area = scrapy.Field(meta_data)
    house_district = scrapy.Field(meta_data)
    house_build_date = scrapy.Field(meta_data)

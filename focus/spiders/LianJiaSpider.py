# -*- coding: utf-8 -*-

from __future__ import print_function
import scrapy
from scrapy.loader import ItemLoader
from focus.items import FocusItem
import sys


class LianJiaSpider(scrapy.Spider):
    name = "esf_lj"
    start_urls = [
        "https://sz.lianjia.com/ershoufang/"
    ]

    @staticmethod
    def parse_next_page_url(response):
        return response.css("div.page-box.house-lst-page-box > a:last-child::attr(href)").extract_first()

    @staticmethod
    def parse_detail_page_url(response):
        return response.css("ul.sellListContent > li.clear > a.img::attr(href)").extract()

    @staticmethod
    def parse_base_house_info(response):
        house_item = ItemLoader(item=FocusItem(), response=response)
        house_item.add_css("house_name", "div.aroundInfo > .communityName > a.info::text")
        house_item.add_css("house_type", "div.houseInfo > .room > .mainInfo::text")
        house_item.add_css("house_build_date", "div.houseInfo > .area > .subInfo::text")
        house_item.add_css("house_district", "div.areaName > .info > a::text")
        house_item.add_css("house_area", "div.houseInfo > .area > .mainInfo::text")
        return house_item.load_item()

    def parse(self, response):
        next_page_urls = self.parse_next_page_url(response)
        if next_page_urls is not None:
            for url in next_page_urls:
                yield response.follow(url, callback=self.parse)

        detail_page_urls = self.parse_detail_page_url(response)
        if detail_page_urls is not None:
            for url in detail_page_urls:
                yield response.follow(url, callback=self.parse)
        yield self.parse_base_house_info(response)

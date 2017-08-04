# -*- coding: utf-8 -*-

from __future__ import print_function

import scrapy
from focus.items import FocusItemLoader

import json


class LianJiaSpider(scrapy.Spider):
    name = "lj"
    LJ_DOMAIN = "https://sz.lianjia.com"
    start_urls = [
        LJ_DOMAIN + "/ershoufang"
    ]

    @staticmethod
    def parse_next_page_url(response):
        next_page_url_pattern = response.css("div.house-lst-page-box::attr(page-url)").extract_first()
        if next_page_url_pattern is None:
            return None
        page_data_str = response.css("div.house-lst-page-box::attr(page-data)").extract_first()
        page_data = json.loads(page_data_str.encode("utf-8"))
        total_page = int(page_data["totalPage"])
        cur_page = int(page_data["curPage"])
        return ("%s%s" % (LianJiaSpider.LJ_DOMAIN, next_page_url_pattern.format(page=next_page))
                for next_page in range(cur_page, total_page+1) if next_page <= total_page)

    @staticmethod
    def parse_detail_page_url(response):
        return response.css("ul.sellListContent > li.clear > a.img::attr(href)").extract()

    @staticmethod
    def parse_base_house_info(response):
        house_item = FocusItemLoader(response=response)
        house_item.add_css("house_name", "div.aroundInfo > .communityName > a.info::text")
        house_item.add_css("house_type", "div.houseInfo > .room > .mainInfo::text")
        house_item.add_css("house_build_date", "div.houseInfo > .area > .subInfo::text")
        house_item.add_css("house_district", "div.areaName > .info > a::text")
        house_item.add_css("house_area", "div.houseInfo > .area > .mainInfo::text")
        return house_item.load_item()

    def parse(self, response):
        next_page_urls = LianJiaSpider.parse_next_page_url(response)
        if next_page_urls is not None:
            for url in next_page_urls:
                print("pagination_page_url =>", url)
                yield response.follow(url, callback=self.parse)

        detail_page_urls = LianJiaSpider.parse_detail_page_url(response)
        if detail_page_urls is not None:
            for url in detail_page_urls:
                print("detail_page_url =>", url)
                yield response.follow(url, callback=self.parse)
        yield LianJiaSpider.parse_base_house_info(response)

# -*- coding: utf-8 -*-

from __future__ import print_function

import json
import re

import scrapy

from focus.items import FocusItemLoader


class LianJiaSpider(scrapy.Spider):
    name = "lj"
    LJ_DOMAIN = "https://sz.lianjia.com"
    start_urls = [
        LJ_DOMAIN + "/ershoufang"
    ]
    HOUSE_UNIQUE_PATTERN = re.compile(r'.*/(?P<unique_flag>\d*)\.html')

    @staticmethod
    def get_house_unique_flag_from_url(url):
        if len(url) == 0:
            return None
        else:
            match = LianJiaSpider.HOUSE_UNIQUE_PATTERN.match(url)
            return match.groupdict().get('unique_flag') if match else None

    def parse_next_page_urls(self, response):
        next_page_url_pattern = response.css("div.house-lst-page-box::attr(page-url)").extract_first()
        if next_page_url_pattern is None:
            return None
        page_data_str = response.css("div.house-lst-page-box::attr(page-data)").extract_first()
        page_data = json.loads(page_data_str.encode("utf-8"))
        total_page = int(page_data["totalPage"])
        cur_page = int(page_data["curPage"])
        return ("%s%s" % (LianJiaSpider.LJ_DOMAIN, next_page_url_pattern.format(page=next_page))
                for next_page in range(cur_page, total_page+1) if next_page <= total_page)

    def parse_detail_page_urls(self, response):
        detail_page_urls = response.css("ul.sellListContent > li.clear > a.img::attr(href)").extract()
        if detail_page_urls is not None:
            for url in detail_page_urls:
                print("detail_page_url =>", url)
                yield response.follow(url, callback=self.parse_base_house_info)

    def parse_base_house_info(self, response):
        house_item = FocusItemLoader(response=response)
        url = response.url
        house_item.add_value("house_id", LianJiaSpider.get_house_unique_flag_from_url(url))
        house_item.add_value("house_url", url)
        house_item.add_css("house_name", "div.aroundInfo > .communityName > a.info::text")
        house_item.add_css("house_visit_cnt", "#cartCount::text")
        house_item.add_css("house_follow_cnt", "#favCount::text")
        house_item.add_css("house_price", "span.total::text")
        house_item.add_css("house_type", "div.houseInfo > .room > .mainInfo::text")
        house_item.add_css("house_build_info", "div.houseInfo > .area > .subInfo::text")
        house_item.add_css("house_district", "div.areaName > .info > a::text")
        house_item.add_css("house_area", "div.houseInfo > .area > .mainInfo::text")
        yield house_item.load_item()

    def parse(self, response):
        next_page_urls = self.parse_next_page_urls(response)
        if next_page_urls is not None:
            for next_page_url in next_page_urls:
                yield response.follow(next_page_url, callback=self.parse_detail_page_urls)

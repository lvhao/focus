# -*- coding:utf-8 -*-

from __future__ import print_function
import scrapy

class LianJiaSpider(scrapy.Spider):
    name = "LJ"
    start_urls = [
        "https://sz.lianjia.com/ershoufang/"
    ]

    def parse(self, response):
        next_page_urls = response.css("ul.sellListContent > li.clear > a.img::attr(href)").extract()
        if next_page_urls is not None:
            for url in next_page_urls:
                yield response.follow(url, callback=self.parse)

        house_name = response.css("div.aroundInfo > .communityName > a.info::text").extract()
        house_name_str = "".join(house_name)
        house_type = response.css("div.houseInfo > .room > .mainInfo::text").extract()
        house_type_str = "".join(house_type)
        house_build_date = response.css("div.houseInfo > .area > .subInfo::text").extract()
        house_build_date_str = "".join(house_build_date)
        house_district = response.css("div.areaName > .info > a::text").extract()
        house_district_str = "".join(house_district)
        house_area = response.css("div.houseInfo > .area > .mainInfo::text").extract()
        house_area_str = "".join(house_area)
        print("get house_district_str:%s, houseName:%s, houseType:%s, houseArea:%s, houseBuildDate:%s" %(house_district_str, house_name_str, house_type_str, house_area_str, house_build_date_str))
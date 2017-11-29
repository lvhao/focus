# -*- coding: utf-8 -*-

from __future__ import division

import matplotlib

matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['PingFang']
from matplotlib.font_manager import FontProperties

from db import Session, House


def getChineseFont():
    return FontProperties(fname='/System/Library/Fonts/PingFang.ttc')


def get_x_y_data():
    session = Session()
    all_houses = []
    try:
        all_houses = session.query(House.house_area, House.house_price, House.house_district).all()
    finally:
        session.close()
    data_gap = 100
    x = [i * data_gap for i in range(2, 10)]
    house_price_map = {}
    for h in all_houses:
        house_price_key = h.house_price // 100 * 100
        for data_extent in reversed(x):
            if house_price_key >= data_extent:
                house_price_key = data_extent
                break
        house_price_count = house_price_map.get(house_price_key, 0)
        house_price_map[house_price_key] = house_price_count + 1
    y = []
    for data_extent in x:
        y.append(house_price_map[data_extent])
    return x, y, all_houses


def bar(title=u"房价/数量 直方图", x=[], y=[]):
    plt.xlabel(u"房屋单价(万元)", fontproperties=getChineseFont())
    plt.ylabel(u"房子数量(套)", fontproperties=getChineseFont())
    plt.figure(1)
    plt.title(title, fontproperties=getChineseFont())
    plt.bar(x=x, height=y, color='green', width=80)


def pie_1(title=u"房价与数量占比", x=[], y=[]):
    plt.figure(2)
    plt.title(title, fontproperties=getChineseFont())
    total_cnt = sum(y)
    labels = [u"%s万+" % (i * 100) for i in range(2, 10)]
    fracs = [(s / total_cnt) * 100 for s in y]
    sorted_fracs = sorted(fracs)[-3:]
    idxs = [fracs.index(v) for v in sorted_fracs]
    plt.axes(aspect=1)
    explode = [0.08 if idx in idxs else 0 for idx, v in enumerate(fracs)]
    plt.pie(x=fracs, labels=labels, autopct='%.0f%%', explode=explode)


def pie_2(title=u"区域与房子数量饼图", all_houses=[]):
    districts = {}
    for house in all_houses:
        district = house.house_district.split()[0]
        cnt = districts.get(district, 0) + 1
        districts.update({district: cnt})
    plt.figure(3)
    plt.title(title, fontproperties=getChineseFont())
    y = districts.values()
    total_cnt = sum(y)
    labels = [u"%s" % lb.decode('utf-8') for lb in districts.keys()]
    fracs = [(i / total_cnt) * 100 for i in y]
    plt.axes(aspect=1)
    explode = [0] * len(y)
    explode[1] = 1
    plt.pie(x=fracs, labels=labels, autopct='%.0f%%', explode=explode)


def show():
    plt.show()


(x, y, all_houses) = get_x_y_data()
bar(x=x, y=y)
pie_1(x=x, y=y)
# pie_2(all_houses=all_houses)
show()

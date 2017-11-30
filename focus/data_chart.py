# -*- coding: utf-8 -*-

from __future__ import division

import matplotlib
import numpy as np

matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['simhei']

from db import Session, House


def get_x_y_data():
    session = Session()
    all_houses = []
    try:
        all_houses = session.query(House.house_area, House.house_price, House.house_district, House.house_follow_cnt,
                                   House.house_visit_cnt).all()
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


def bar_1(title=u"房价/数量 直方图", x=None, y=None):
    plt.xlabel(u"房屋单价(万元)")
    plt.ylabel(u"房子数量(套)")
    plt.figure(1)
    plt.title(title)
    plt.bar(x=x, height=y, color='green', width=80)


def bar_2(x=None, all_houses=None):
    group_labels = tuple([u"%s万" % i for i in x])
    n_groups = len(group_labels)

    house_visit_cnt_map = {}
    house_follow_cnt_map = {}
    for h in all_houses:
        house_price_key = h.house_price // 100 * 100
        for data_extent in reversed(x):
            if house_price_key >= data_extent:
                house_price_key = data_extent
                break
        house_total_visit_count = house_visit_cnt_map.get(house_price_key, 0)
        house_visit_cnt_map[house_price_key] = house_total_visit_count + h.house_visit_cnt

        house_total_follow_count = house_follow_cnt_map.get(house_price_key, 0)
        house_follow_cnt_map[house_price_key] = house_total_follow_count + h.house_follow_cnt

    visit_cnts = []
    follow_cnts = []
    for data_extent in x:
        visit_cnts.append(house_visit_cnt_map[data_extent])
        follow_cnts.append(house_follow_cnt_map[data_extent])

    means_visit_cnt = tuple(visit_cnts)
    std_visit = ([0] * len(group_labels))

    means_follow_cnt = tuple(follow_cnts)
    std_follow = ([0] * len(group_labels))

    fig, ax = plt.subplots()

    index = np.arange(n_groups)
    bar_width = 100

    opacity = 0.4
    error_config = {'ecolor': '0.3'}

    ax.bar(index * 250, means_follow_cnt, bar_width,
           alpha=opacity, color='b',
           yerr=std_follow, error_kw=error_config,
           label=u"关注量")

    ax.bar(index * 250 + bar_width, means_visit_cnt, bar_width,
           alpha=opacity, color='r',
           yerr=std_visit, error_kw=error_config,
           label=u"到访量")

    ax.set_xlabel(u"单价")
    ax.set_ylabel(u"数量")
    ax.set_title(u"房价 关注/到访")
    ax.set_xticks(index * 250 + bar_width / 2)
    ax.set_xticklabels(group_labels)
    ax.legend()
    fig.tight_layout()


def pie_1(title=u"房价与数量占比", x=[], y=[]):
    plt.figure(3)
    plt.title(title)
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
    plt.figure(4)
    plt.title(title)
    y = districts.values()
    total_cnt = sum(y)
    labels = [u"%s" % lb.decode('utf-8') for lb in districts.keys()]
    fracs = [(i / total_cnt) * 100 for i in y]
    plt.axes(aspect=1)
    explode = [0] * len(y)
    explode[1] = 1
    plt.pie(x=fracs, labels=labels, autopct='%.0f%%', explode=explode)


def show():
    (x, y, all_houses) = get_x_y_data()
    bar_1(x=x, y=y)
    bar_2(x=x, all_houses=all_houses)
    pie_1(x=x, y=y)
    pie_2(all_houses=all_houses)
    plt.show()


if __name__ == "__main__":
    show()

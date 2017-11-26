# -*- coding: utf-8 -*-

from __future__ import division

import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from db import Session, House

session = Session()
all_houses = []
try:
    all_houses = session.query(House.house_area, House.house_price).all()
finally:
    session.close()
data_gap = 100
index = [i * data_gap for i in range(2, 10)]
house_price_map = {}
for h in all_houses:
    house_price_key = h.house_price // 100 * 100
    for data_extent in reversed(index):
        if house_price_key >= data_extent:
            house_price_key = data_extent
            break
    house_price_count = house_price_map.get(house_price_key, 0)
    house_price_map[house_price_key] = house_price_count + 1
y = []
for data_extent in index:
    y.append(house_price_map[data_extent])

plt.figure(1)
plt.title(u"直方图")
plt.bar(left=index, height=y, color='green', width=50)

plt.figure(2)
plt.title(u"饼图")
total_cnt = sum(y)
labels = [u"%sW+" % (i * data_gap) for i in range(2, 10)]
fracs = [(s / total_cnt) * 100 for s in y]
plt.axes(aspect=1)
explode = [0 for x in xrange(0, len(y))]
plt.pie(x=fracs, labels=labels, autopct='%.0f%%', explode=explode)

plt.figure(3)
plt.title(u"线图")
plt.plot(index, y, 'ro')
plt.axis([0, 900, 0, 500])

plt.show()

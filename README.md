# focus
爬取链家二手房楼盘信息
## 涉及技术点
python2.7 + scrapy + matplotlib + mysql

## 遇到问题
matplotlib 中文显示
1. 下载字体:simhei.ttf
2. 找到matplotlib包位置
  import matplotlib 
  print(matplotlib.matplotlib_fname()
  
  示例:
  > /Users/lvhao/focus_env/lib/python2.7/site-packages/matplotlib/mpl-data/matplotlibrc
2. 放在matplotlib的字体文件夹下(/Users/lvhao/focus_env/lib/python2.7/site-packages/matplotlib/mpl-data/fonts/ttf)
3. 删除~/.matplotlib下文件 fontList.json tex.cache
4. 重启python

## 效果展示
![房价数量直方图](https://github.com/lvhao/focus/blob/master/focus/resources/Figure_1.png)
![房价/关注,到访直方图](https://github.com/lvhao/focus/blob/master/focus/resources/Figure_2.png)
![房屋价格占比饼图](https://github.com/lvhao/focus/blob/master/focus/resources/Figure_3.png)
![房屋区域占比饼图](https://github.com/lvhao/focus/blob/master/focus/resources/Figure_4.png)
![房屋建筑年代数量关系图](https://github.com/lvhao/focus/blob/master/focus/resources/Figure_5.png)

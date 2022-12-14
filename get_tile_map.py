#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# python3.6脚本

# 爬取地图瓦片数据
import urllib.request
import os
import random
import math

agents = [
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1']
print("hello")


# 经纬度反算切片行列号  3857坐标系
def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)


# 下载图片
def getimg(Tpath, Spath, x, y):
    try:
        f = open(Spath, 'wb')
        req = urllib.request.Request(Tpath)
        req.add_header('User-Agent', random.choice(agents))  # 换用随机的请求头
        pic = urllib.request.urlopen(req, timeout=60)

        f.write(pic.read())
        f.close()
        print(str(x) + '_' + str(y) + '下载成功')
    except Exception:
        print(str(x) + '_' + str(y) + '下载失败,重试')
        getimg(Tpath, Spath, x, y)


# for zoom in range(7, 19):
zoom = 8  # 下载切片的zoom
# 中国
# 69.48,55.74 左上角
# 137.51,2.22 右下角
lefttop = deg2num(55.74, 69.48, zoom)  # 下载切片的左上角角点
rightbottom = deg2num(2.22, 137.51, zoom)

# 下载全球影像数据lefttop=[0,0],rightbottom=[2**zoom,2**zoom]
# lefttop[0]~rightbottom[0]为x范围
# lefttop = [0, 0]
# lefttop[1]~rightbottom[1]为y范围
# rightbottom = [2 ** zoom, 2 ** zoom]

print("开始下载第", zoom, "级别的影像数据...")
print(str(lefttop[0]))
print(str(rightbottom[0]))
print(str(lefttop[1]))
print(str(rightbottom[1]))
print("共" + str(lefttop[0] - rightbottom[0]))
print("共" + str(lefttop[1] - rightbottom[1]))

rootDir = "D:\\environment\\apache-tomcat-8.5.84\\webapps\\china_map\\tdt_tile\\"
for x in range(lefttop[0], rightbottom[0]):
    for y in range(lefttop[1], rightbottom[1]):
        # Google地图瓦片
        # tilepath = 'http://www.google.cn/maps/vt/pb=!1m4!1m3!1i' + str(zoom) + '!2i' + str(x) + '!3i' + str(y) + '!2m3!1e0!2sm!3i345013117!3m8!2szh-CN!3scn!5e1105!12m4!1e68!2m2!1sset!2sRoadmap!4e0'

        # Google影像瓦片
        # tilepath = 'http://mt2.google.cn/vt/lyrs=y&hl=zh-CN&gl=CN&src=app&x='+str(x)+'&y='+str(y)+'&z='+str(zoom)+'&s=G'

        # 天地图-地图
        tilepath = 'http://t2.tianditu.com/DataServer?T=vec_w&x=' + str(x) + '&y=' + str(y) + '&l=' + str(
            zoom) + '&tk=c25a0ad23db089f1f3b7d8874b796cab'
        # 天地图-标注
        # tilepath = 'http://t0.tianditu.com/DataServer?T=cva_w&x='+str(x)+'&y='+str(y)+'&l='+str(zoom)+'&tk=5d22d49fdc586cb5caed68bfb12d1e6b'

        # 天地图-影像
        # tilepath = 'http://t0.tianditu.gov.cn/DataServer?T=img_w&x=' + str(x) + '&y=' + str(y) + '&l=' + str(zoom) + '&tk=5d22d49fdc586cb5caed68bfb12d1e6b'
        # 天地图-影像标注
        # tilepath = 'http://t6.tianditu.gov.cn/DataServer?T=cia_w&x=' + str(x) + '&y=' + str(y) + '&l=' + str(zoom) + '&tk=5d22d49fdc586cb5caed68bfb12d1e6b'

        path = rootDir + str(zoom) + "\\" + str(x)
        if not os.path.exists(path):
            os.makedirs(path)
        getimg(tilepath, os.path.join(path, str(y) + ".jpg"), x, y)
print('完成')

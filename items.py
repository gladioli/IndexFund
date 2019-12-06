# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import json

import scrapy


class IndexFundItem(scrapy.Item):
    # define the fields for your item here like:

    fund_fullname = scrapy.Field()      # 基金全称
    fund_name = scrapy.Field()          # 基金简称
    fund_code = scrapy.Field()          # 基金代码
    fund_release = scrapy.Field()       # 发行时间
    fund_size = scrapy.Field()          # 基金规模

    fund_glr = scrapy.Field()           # 基金管理人
    fund_gl_size = scrapy.Field()       # 基金公司规模
    fund_glr_url = scrapy.Field()       # 基金管理人链接
    fund_gl_rate = scrapy.Field()       # 管理费率

    fund_tg_rate = scrapy.Field()       # 托管费率

    track_target = scrapy.Field()       # 跟踪标的
    track_err_rate = scrapy.Field()       # 跟踪标的


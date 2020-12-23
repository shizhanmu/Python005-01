# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UstvItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    subject_id = scrapy.Field()
    title = scrapy.Field()
    nickname = scrapy.Field()
    rating = scrapy.Field()
    posttime = scrapy.Field()
    shortcomment = scrapy.Field()
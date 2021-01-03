# -*- coding: utf-8 -*-
import scrapy
from pathlib import Path
from urllib import parse
import json
import math
from ustv.items import UstvItem

dirpath = Path(__file__).parent.resolve()
filepath = dirpath / 'cangqiong.json'
url = str(filepath.as_uri())


class TvshortSpider(scrapy.Spider):
    name = 'tvshort'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/']
    start_urls = [url]

    def start_requests(self):
        # for n in range(1):
        #     url = f'https://movie.douban.com/j/search_subjects?type=tv&tag=美剧&sort=recommend&page_limit=20&page_start={n*20}'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """解析json文件，获取评论页 url
        """
        rdict = response.json()
        for info_dict in rdict['subjects']:
            subject_id = info_dict['id']
            title = info_dict['title']
            url = info_dict['url']
            short_url = parse.urljoin(url, 'comments?status=P')
            print(str(short_url))
            yield scrapy.Request(url=str(short_url), meta={'subject_id': subject_id, 'title': title}, callback=self.parse2)
    
    def parse2(self, response):
        subject_id = response.meta['subject_id']
        title = response.meta['title']
        # 获取评论总数
        # text = response.xpath('//ul[@class="fleft CommentTabs"]/li/span/text()').get()
        # max_num = int(text.lstrip('看过(').rstrip(')'))
        # max_page = math.ceil(max_num/20)
        max_page = 3  # 减少爬取页数，因为 ip 地址要花钱
        for page in range(max_page):
            url = f'https://movie.douban.com/subject/{subject_id}/comments?start={page*20}&limit=20&status=P&sort=new_score'
            yield scrapy.Request(url=url, meta={'subject_id': subject_id, 'title': title}, callback=self.parse3)
    
    def parse3(self, response):
        """获取昵称、评分、发布时间、短评内容
        """
        items = []
        subject_id = response.meta['subject_id']
        title = response.meta['title']
        comment_block = response.xpath('//div[@class="comment"]')
        for block in comment_block:
            item = UstvItem()
            nickname = block.xpath('./h3/span[2]/a/text()').get()
            rating = block.xpath('./h3/span[2]/span[2]/@title').get()
            posttime = block.xpath('./h3/span/span[@class="comment-time "]/@title').get()
            shorttext = block.xpath('./p/span/text()').get()
            item['subject_id'] = subject_id
            item['title'] = title
            item['category'] = 'tv'
            item['nickname'] = nickname
            item['rating'] = rating
            item['posttime'] = posttime
            item['shorttext'] = shorttext
            items.append(item)
        print(items)
        return items
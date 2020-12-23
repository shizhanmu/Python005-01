# -*- coding: utf-8 -*-
import scrapy
from pathlib import Path


class TvshortSpider(scrapy.Spider):
    name = 'tvshort'
    allowed_domains = ['movie.douban.com']
    # start_urls = ['http://movie.douban.com/']
    # filepath = Path('cangqiong.json').resolve()
    # uri = filepath.as_uri()
    start_urls = ['https://movie.douban.com/tv/']


    def start_requests(self):
        for n in range(1):
            url = f'https://movie.douban.com/j/search_subjects?type=tv&tag=美剧&sort=recommend&page_limit=20&page_start={n*20}'
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        rdict = response.json()
        for info_dict in rdict['subject']:
            subject_id = info_dict['id']
            title = info_dict['title']
            url = Path(info_dict['url'])
            short_url = url / 'comments?status=P'
            yield scrapy.Request(url=short_url, meta={'subject_id': subject_id, 'title': title}, callback=self.parse2)
    
    def parse2(self, response):
        subject_id = response.meta['subject_id']
        title = response.meta['title']
        text = response.xpath('//ul[@class="fleft CommentTabs"]/li/span/text()').get()
        max_num = text.lstrip('看过(').rstrip(')')
        if max_num % 20 == 0:
            max_page = max_num//20
        else:
            max_page = max_num//20 + 1
        for page in range(max_page):
            url = f'https://movie.douban.com/subject/{id}/comments?start={page}&limit=20&status=P&sort=new_score'
            yield scrapy.Request(url=url, meta={'subject_id': subject_id, 'title': title}, callback=self.parse3)
    
    def parse3(self, response):
        items = []
        subject_id = response.meta['subject_id']
        title = response.meta['title']
        comment_block = response.xpath('//div[@class="comment"]')
        for block in comment_block:
            item = UstvItem()
            nickname = block.xpath('./h3/span[2]/a/text()').get()
            rating = block.xpath('./h3/span[2]/span[2]/@title').get()
            posttime = block.xpath('./h3/span/span[@class="comment-time "]/@title').get()
            shortcomment = block.xpath('./p/span/text()').get()
            item['category'] = 'tv'
            item['subject_id'] = subject_id
            item['title'] = title
            item['nickname'] = nickname
            item['rating'] = rating
            item['posttime'] = posttime
            item['shortcomment'] = shortcomment
            items.append(item)
        return items
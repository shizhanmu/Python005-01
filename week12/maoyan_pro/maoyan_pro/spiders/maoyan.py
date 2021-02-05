import scrapy
from maoyan_pro.items import MaoyanProItem

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3&offset=0']
    # start_urls = ['./maoyan_source.html']

    def parse(self, response):
        items = []
        movies = response.xpath('//div[@class="movie-hover-info"]')
        for m in movies:
            item = MaoyanProItem()
            title = m.xpath('./div[@class="movie-hover-title"]/span[@class="name "]/text()').get()
            genre = m.xpath('./div[@class="movie-hover-title"]/span/text()[contains(., "类型:")]/../../text()[2]').get().strip()
            starring = m.xpath('./div[@class="movie-hover-title"]/span/text()[contains(., "主演:")]/../../text()[2]').get().strip()
            release = m.xpath('./div[@class="movie-hover-title movie-hover-brief"]/span/text()[contains(., "上映时间:")]/../../text()[2]').get().strip()
            item['title'] = title
            item['genre'] = genre
            item['starring'] = starring
            item['release'] = release
            items.append(item)
        return items
        
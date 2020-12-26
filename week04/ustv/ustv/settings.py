# -*- coding: utf-8 -*-

# Scrapy settings for ustv project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ustv'

SPIDER_MODULES = ['ustv.spiders']
NEWSPIDER_MODULE = 'ustv.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'ustv (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

RETRY_ENABLE = True

RETRY_TIMES = 2

DOWNLOAD_TIMEOUT = 10


# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    # 'Accept-Encoding': 'gzip, deflate, br',
    # 'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5',
    # 'Cache-Control': 'max-age=0',
    # 'Connection': 'keep-alive',
    # 'Host': 'movie.douban.com',
    # 'Referer': 'https://movie.douban.com/subject/26584183/comments?status=P',
    # 'Upgrade-Insecure-Requests': '1',
    'User-Agent': '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'''
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'ustv.middlewares.UstvSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware':123,
    'ustv.ippool.Ippool' : 125,
    'ustv.middlewares.UstvDownloaderMiddleware': None,
}

IPPOOL = ['117.69.200.158:4225', '182.114.108.71:4256', '36.102.168.107:4285', '60.175.20.135:4278', '27.44.222.213:4245', '140.255.42.223:4258', '60.166.164.220:4226', '182.241.173.222:4242', '58.243.207.90:4243', '49.83.136.175:4232', '114.99.15.2:4232', '27.150.195.130:4245', '49.85.15.225:4216', '125.87.81.240:4278', '42.242.123.36:4243', '114.104.141.83:4231', '42.230.66.112:4245', '119.54.25.62:4258', '123.97.126.224:4257', '59.60.129.137:4278']

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'ustv.pipelines.UstvPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
MYSQL_HOST = 'localhost'
MYSQL_DATABASE = 'dbcomment'
MYSQL_TABLE = 'shortcomment_short'
MYSQL_PORT = 3306
MYSQL_USER = 'testuser'
MYSQL_PASSWORD = '123456'
import random

from middlewares.middleware import Middleware
from settings import HTTP_PROXYS
import scrapy


class RandomProxy(Middleware):
    """
    随机代理
    """

    def process_request(self, request: scrapy.Request, spider: scrapy.Spider):
        request.meta['proxy'] = random.choice(HTTP_PROXYS)
        print(request.meta['proxy'])

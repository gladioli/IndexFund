import random
import scrapy

from middlewares.middleware import Middleware
from settings import USER_AGENTS


class RandomUserAgent(Middleware):
    """
    随机User-Agent
    """

    def process_request(self, request: scrapy.Request, spider: scrapy.Spider):
        request.headers.setdefault('User-Agent', random.choice(USER_AGENTS))
        print(request.headers.get('User-Agent'))

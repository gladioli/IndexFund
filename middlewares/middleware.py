import scrapy


class Middleware(object):

    def process_request(self, request: scrapy.Request, spider: scrapy.Spider):
        pass

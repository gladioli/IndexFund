import time

import scrapy
import random
from scrapy.http import HtmlResponse
from selenium.webdriver.support.wait import WebDriverWait

from middlewares.middleware import Middleware
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from settings import HTTP_PROXYS, USER_AGENTS


class SeleniumMiddleware(Middleware):

    def process_request(self, request: scrapy.Request, spider: scrapy.Spider):
        if spider.name == 'csi_500':
            chrome_opt = Options()  # 创建参数设置对象.
            chrome_opt.add_argument('--headless')  # 无界面化.
            chrome_opt.add_argument('--disable-gpu')  # 配合上面的无界面化.
            chrome_opt.add_argument('--user-agent=%s' % random.choice(USER_AGENTS))
            # chrome_opt.add_argument('--proxy-server=%s' % random.choice(HTTP_PROXYS))

            driver = webdriver.Chrome(executable_path="middlewares/chromedriver", chrome_options=chrome_opt)
            driver.get(request.url)
            # driver.implicitly_wait(20)

            wait: WebDriverWait = WebDriverWait(driver, 30)

            if request.url.endswith('jjgs'):
                print('搜索基金公司')

                arr_down = wait.until(lambda x: x.find_elements_by_xpath('//*[@id="jj"]/p/a/i[@class="arr down"]'))
                if arr_down and len(arr_down) >= 1:
                    wait.until(lambda x: x.find_elements_by_xpath('//*[@id="jj"]/p/a'))[0].click()
                    wait.until(lambda x: x.find_elements_by_xpath('//*[@id="jj"]/p/a/i[@class="arr up"]'))

            html = driver.page_source
            driver.quit()
            return HtmlResponse(url=request.url, body=html, request=request, encoding='utf-8')

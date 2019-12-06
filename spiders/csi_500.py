# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
from items import IndexFundItem


class Csi500Spider(scrapy.Spider):
    name = "csi_500"
    allowed_domains = ["eastmoney.com"]
    jbdata_rul = 'http://fundf10.eastmoney.com/jbgk_{0}.html'
    tsdata_rul = 'http://fundf10.eastmoney.com/tsdata_{0}.html'
    search_url = 'http://fund.eastmoney.com/data/fundsearch.html?spm=search&key={0}#key{1};jjgs'
    search_key = '中证500'
    pi = 1  # 页面下标

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Language': 'zh,zh-TW;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
        'Referer': 'http://fund.eastmoney.com/daogou/',
        'Cookie': 'searchbar_code=519985_510500; em_hq_fls=js; qgqp_b_id=ababaeee62a3602937fee067df229d32; HAList=f-0-000905-%u4E2D%u8BC1500%2Cf-0-399396-%u56FD%u8BC1%u98DF%u54C1; st_si=44031812198631; st_asi=delete; ASP.NET_SessionId=vhag5bhuyo15vu0ji1tk2gpv; EMFUND0=11-29%2000%3A38%3A28@%23%24%u666F%u987A%u957F%u57CE%u4E2D%u8BC1500%u589E%u5F3A@%23%24006682; EMFUND1=11-29%2000%3A39%3A38@%23%24%u5929%u5F18%u4E2D%u8BC1500%u6307%u6570C@%23%24005919; EMFUND2=11-29%2015%3A56%3A59@%23%24%u6CF0%u8FBE%u4E2D%u8BC1500%u6307%u6570%u589E%u5F3A%28LOF%29@%23%24162216; EMFUND4=11-30%2017%3A35%3A33@%23%24%u5357%u65B9%u4E2D%u8BC1500ETF%u8054%u63A5C@%23%24004348; EMFUND5=11-30%2017%3A38%3A21@%23%24%u5E7F%u53D1%u4E2D%u8BC1500ETF%u8054%u63A5C@%23%24002903; EMFUND6=12-05%2011%3A33%3A11@%23%24%u5E7F%u53D1%u4E2D%u8BC1500ETF%u8054%u63A5A@%23%24162711; EMFUND9=12-05%2011%3A35%3A01@%23%24%u5EFA%u4FE1%u4E2D%u8BC1500%u6307%u6570%u589E%u5F3AA@%23%24000478; EMFUND8=12-05%2012%3A31%3A06@%23%24%u5357%u65B9%u4E2D%u8BC1500ETF%u8054%u63A5A@%23%24160119; st_pvi=91033502361869; st_sp=2019-11-20%2015%3A52%3A28; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Flink; st_sn=10; st_psi=2019120512421442-112200304021-0516482792; EMFUND3=12-05%2012%3A38%3A28@%23%24%u4E2D%u91D1%u4E2D%u8BC1500C@%23%24003578; EMFUND7=12-05 12:43:53@#$%u5357%u65B9%u4E2D%u8BC1500ETF@%23%24510500'
    }

    def start_requests(self):
        url = self.search_url.format(self.search_key, self.search_key)
        return [
            scrapy.Request(url, headers=self.headers, callback=self.parse_search, ),
        ]

    def parse_search(self, response: scrapy.http.Response):
        """
        基金搜索
        :param response:
        :return:
        """
        content = str(response.body, 'utf-8')
        html = etree.HTML(content)
        jj_list = html.xpath('//div[@id="jj"]//table/tbody/tr')
        if not jj_list or len(jj_list) == 0:
            return
        print(len(jj_list))
        for jj in jj_list:
            # if not jj.xpath('./td[1]/a/text()') or len(jj.xpath('./td[1]/a')) == 0:
            #     return
            jj_code: str = jj.xpath('string(./td[1]/a)')
            jj_name: str = jj.xpath('string(./td[2]/a/@title)')
            if jj_name.endswith('500ETF'):
                print(jj_code, jj_name, "=" * 8)

                url = self.jbdata_rul.format(jj_code)
                yield scrapy.Request(url, headers=self.headers, callback=self.parse_detail, dont_filter=True)
            # else:
            # print(jj_code, jj_name)

    def parse_detail(self, response: scrapy.http.Response):
        """
        基金概况
        :param response:
        :return:
        """
        content = str(response.body, 'utf-8')
        html = etree.HTML(content)
        info_w790 = html.xpath('//table[@class="info w790"]')
        if not info_w790 or len(info_w790) == 0:
            return
        jjgk_ele = html.xpath('//table[@class="info w790"]')[0]

        item = IndexFundItem()

        item['fund_fullname'] = jjgk_ele.xpath('./tbody/tr[1]/td[1]/text()')[0]  # 基金全称
        item['fund_name'] = jjgk_ele.xpath('./tbody/tr[1]/td[2]/text()')[0]  # 基金简称
        item['fund_code'] = jjgk_ele.xpath('./tbody/tr[2]/td[1]/text()')[0][0:6]  # 基金代码
        item['fund_release'] = jjgk_ele.xpath('./tbody/tr[3]/td[1]/text()')[0]  # 发行时间
        item['fund_size'] = jjgk_ele.xpath('./tbody/tr[4]/td[1]/text()')[0].split('（')[0]  # 基金规模
        item['fund_size'] = item['fund_size'].replace('亿元', '')

        item['fund_glr'] = jjgk_ele.xpath('./tbody/tr[5]/td[1]/a/text()')[0]  # 基金管理人
        item['fund_glr_url'] = jjgk_ele.xpath('./tbody/tr[5]/td[1]/a/@href')[0]  # 基金管理人链接
        item['fund_gl_rate'] = jjgk_ele.xpath('./tbody/tr[7]/td[1]/text()')[0]  # 管理费率
        item['fund_gl_rate'] = item['fund_gl_rate'].replace('%', '').replace('（每年）', '')

        # item.fund_tgr = jjgk_ele.xpath('./tbody/tr[5]/td[2]/a/text()')[0]        # 基金托管人
        # item.fund_tgr_url = jjgk_ele.xpath('./tbody/tr[5]/td[2]/a/@href')[0]     # 基金托管人链接
        item['fund_tg_rate'] = jjgk_ele.xpath('./tbody/tr[7]/td[1]/text()')[0]  # 托管费率
        item['fund_tg_rate'] = item['fund_tg_rate'].replace('%', '').replace('（每年）', '')

        request = scrapy.Request(url=item['fund_glr_url'], headers=self.headers, callback=self.parse_company,
                                 dont_filter=True)
        request.meta['item'] = item
        yield request

    def parse_company(self, response: scrapy.http.Response):
        """
        基金公司
        :param response:
        :return:
        """
        item: IndexFundItem = response.meta['item']

        content = str(response.body, 'utf-8')
        html = etree.HTML(content)

        item['fund_gl_size'] = html.xpath('//div[@class="fund-info"]//li[1]//label[@class="grey"]/text()')[0]
        item['fund_gl_size'] = item['fund_gl_size'].replase('亿元', '')

        url = self.tsdata_rul.format(item['fund_code'])
        request = scrapy.Request(url=url, headers=self.headers, callback=self.parse_tsdata, dont_filter=True)
        request.meta['item'] = item
        yield request

    def parse_tsdata(self, response: scrapy.http.Response):
        """
        特色数据
        :param response:
        :return:
        """
        item: IndexFundItem = response.meta['item']

        content = str(response.body, 'utf-8')
        html = etree.HTML(content)

        item['track_target'] = html.xpath('//div[@id="jjzsfj"]//table[@class="fxtb"]//tr[2]/td[1]/text()')[0]
        item['track_err_rate'] = html.xpath('//div[@id="jjzsfj"]//table[@class="fxtb"]//tr[2]/td[2]/text()')[0]
        item['track_err_rate'] = item['track_err_rate'].replace('%', '')

        yield item

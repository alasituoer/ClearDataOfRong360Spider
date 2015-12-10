#*- encoding:utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from tutorial.items import Rong360Item

class Rong360Spider(CrawlSpider):

    name = "rong360"
    allowed_domain = ["rong360.com"]

    city = ['guangzhou', 'wuxi', 'shenyang', 'chengdu', 'hangzhou',
            'fuzhou', 'nanjing', 'haikou', 'zhongshan', 'yantai',
            'baotou', 'huhehaote', 'shanghai', 'jinan', 'dalian',
            'foshan', 'qingdao', 'ningbo', 'haerbin', 'nanchang',
            'kunming', 'langfang', 'tangshan', 'qinhuangdao', 'baoding',
            'beijing', 'xian', 'taiyuan', 'tianjin', 'xiamen',
            'dongguan', 'changsha', 'zhuhai', 'shijiazhuang', 'yinchuan',
            'guiyang', 'lanzhou', 'xining', 'shenzhen', 'wulumuqi',
            'zhengzhou', 'nanning', 'hefei', 'suzhou', 'changchun', 
            'chongqing', 'wuhan', 'wenzhou', 'huizhou', 'changzhou']

    start_urls = []
    for ci in city:
        start_urls.append("http://www.rong360.com/%s/fangdai/search?px=1" % ci)

    def parse(self, response):
        for sel in response.xpath("//div[@class='change-city']"):
            rong360 = Rong360Item()
            rong360['name_city'] = sel.xpath("p[@class='name']/text()").extract()
        for sel in response.xpath("//div[@class='product_info fl']"):
            rong360['name_bank'] = sel.xpath("h4/a/text()").extract()
            rong360['down_payment_first_home'] = sel.xpath("ul/li[1]/span[2]/text()").extract()
            rong360['loan_rates_first_home'] = sel.xpath("ul/li[1]/b/text()").extract()
            rong360['down_payment_second_home'] = sel.xpath("ul/li[2]/span[2]/text()").extract()
            rong360['loan_rates_second_home'] = sel.xpath("ul/li[2]/b/text()").extract()
            yield rong360

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Rong360Item(scrapy.Item):
    name_city = scrapy.Field()
    name_bank = scrapy.Field()
    down_payment_first_home = scrapy.Field()
    loan_rates_first_home = scrapy.Field()
    down_payment_second_home = scrapy.Field()
    loan_rates_second_home = scrapy.Field()

'''    
#初始化Rong360Item对象
rong360 = Rong360Item(name_city = '广州', name_bank = '工商银行')
#引用方式
rong360['name_city']
rong360.get('name_bank')
#赋值方法
rong360['down_payment_first_home'] = '95'
#调用输出该对象的key值和对象元素的属性
rong360.keys()
rong360.items()
#复制item
rong360_1 = Rong360Item(rong360)
rong360_2 = rong360_1.copy()
#字典和item相互转换
dict(rong360)
Rong360Item({'name_city': '广州', 'name_bank': '工商银行'})
#继承类 添加新字段或扩展字段的元数据
class Product(Rong360Item):
    loan_rates_first_home = scrapy.Filed(serializer = str)
    down_payment_second_home = scrapy.Field(Rong360.fields[
          'down_payment_first_home'], serializer = my_serializer)

#修改requests对象 可采用重写(override)start_requests()
#在启动爬虫时以POST登录融360网站
def start_requests(self):
    return [scrapy.FormRequest("http://www.rong360.com/login",
            formdata = {'user': 'john', 'pass': 'secret'},
            callback = self.logged_in)]
def logged_in(self, reponse):
    pass

#Spider 属性值
#name, allowed_domains, starts_urls, custom_settings, crawler, settings,
#from_crawler(crawl, *args, **kwargs), start_requests(), 
#make_requests_from_url(url), parse(response), log(message[, level, component]),
#closed(reason)
'''

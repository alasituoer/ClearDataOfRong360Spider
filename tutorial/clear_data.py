#-*- encoding:utf-8 -*-
#Json文件中的数据来自于scrapy框架从融360官网爬取到的房贷数据
#通过远程从数据库中提取数据然后与融360官网的数据的数据进行对比
import json
import MySQLdb
import sys

#打开json文件 将其中的数据读入data_from_json变量中
f = file("spiders/rong360.json")
data_from_json = json.loads(json.dumps(list(f)))
for i in range(len(data_from_json)):
    data_from_json[i] = json.loads(data_from_json[i])

#定义各城市银行总数量
number_bank = len(data_from_json)
print "从官网爬取到的银行数:", number_bank

#分别清洗公积金贷款和商贷的首付和利率信息
#从json中提取的字符串内是python字典 但是该字典的key值和value值在列表中 
#所以需要多加[0]来引用 下面在通过切片清洗的同时脱去了改列表以简化引用
for i in range(number_bank): 
    data_from_json[i]['name_city'] = data_from_json[i]['name_city'][0]
    #如果是公积金 
    if data_from_json[i]['loan_rates_first_home'][0].encode('utf-8'
            ) == "公积金基准(3.25%)":
        data_from_json[i]['name_bank'
                ] = data_from_json[i]['name_bank'][0][0:5]
        data_from_json[i]['down_payment_first_home'
                ]= data_from_json[i]['down_payment_first_home'][0]
        data_from_json[i]['loan_rates_first_home'
                ] = data_from_json[i]['loan_rates_first_home'][0][:-7]
        data_from_json[i]['down_payment_second_set'
                ] = data_from_json[i]['down_payment_second_home'][0]
        data_from_json[i]['rate_interest_second_set'
                ] = data_from_json[i]['loan_rates_second_home'][0][:-7]
    #剩下的则是商贷
    else:
        data_from_json[i]['name_bank'
                ] = data_from_json[i]['name_bank'][0][0:4]
        data_from_json[i]['down_payment_first_home'
                ]= data_from_json[i]['down_payment_first_home'][0][2:-2]
        data_from_json[i]['loan_rates_first_home'
                ] = data_from_json[i]['loan_rates_first_home'][0][:-8]
        if data_from_json[i]['loan_rates_first_home'].encode('utf-8'
                ) == "基":
            data_from_json[i]['loan_rates_first_home'] = '1'
        data_from_json[i]['down_payment_second_home'
                ] = data_from_json[i]['down_payment_second_home'][0][2:-2]
        data_from_json[i]['loan_rates_second_home'
                ] = data_from_json[i]['loan_rates_second_home'][0][:-8]
        if data_from_json[i]['loan_rates_second_home'].encode('utf-8'
                ) == "基":
            data_from_json[i]['loan_rates_second_home'] = '1'

#此处开始尝试连接数据库 如果远程连接出错则退出
try:
    conn = MySQLdb.connect(
            host = '10.2.16.59',
            port = 3306,
            user = 'alas', 
            passwd = '6143',
            db = 'data_personal_house_mortgage_loans',
            charset = 'utf8')
except Exception, e:
    print e
    sys.exit()

cur = conn.cursor()

#查询语句 包括ID、城市、银行、首套首付、首套利率、二套首付、二套利率
mysql = """
        select id, city, bank,  down_payment_first_home,
                loan_rates_first_home, down_payment_second_home,
                loan_rates_second_home
        from april2016"""
try:
    cur.execute(mysql)
except Exception, e:
    print e

rows = cur.fetchall()
#初始化变量 存入从数据库查询的数据
data_from_mysql = range(len(rows))
for i in range(len(rows)):
    data_from_mysql[i] = list(rows[i])
    #如果利率小于基准 则将其乘以100 
    if data_from_mysql[i][4] < '1':
        data_from_mysql[i][4] = str(float(data_from_mysql[i][4])*100)
        #如果扩大100倍之后个位是0 则只取十位 下面还实现了扔掉实数的小数点及右边的0
        if data_from_mysql[i][4][1] == '0':
            data_from_mysql[i][4] = data_from_mysql[i][4][0] 
        else:
            data_from_mysql[i][4] = data_from_mysql[i][4][:2]
    if data_from_mysql[i][6] < '1':
        data_from_mysql[i][6] = str(float(data_from_mysql[i][6])*100)
        #如果扩大100倍之后个位是0 则只取十位 下面还实现了扔掉实数的小数点及右边的0
        if data_from_mysql[i][6][1] == '0':
            data_from_mysql[i][6] = data_from_mysql[i][6][0] 
        else:
            data_from_mysql[i][6] = data_from_mysql[i][6][:2]

#上万次的循环 固定城市和银行 对比首付及利率
for i in range(len(rows)):
    for j in range(number_bank):
        if data_from_json[j]['name_city'
                ]  == data_from_mysql[i][1] and data_from_json[j]['name_bank'
                ]  == data_from_mysql[i][2]:
            if data_from_json[j]['down_payment_first_home'
                    ] == data_from_mysql[i][3
                    ] and data_from_json[j]['loan_rates_first_home'
                    ] == data_from_mysql[i][4
                    ] and data_from_json[j]['down_payment_second_home'
                    ] == data_from_mysql[i][5
                    ] and data_from_json[j]['loan_rates_second_home'
                    ] == data_from_mysql[i][6
                    ]:
                pass
            #如果不一致 则按照下列格式输出 
            else:
                print 'there is an error!'
                print '来自官网的数据:', '\t', data_from_json[j]['name_city'
                        ], '\t', data_from_json[j]['name_bank'
                        ], '\t', data_from_json[j]['down_payment_first_home'
                        ], '\t',  data_from_json[j]['loan_rates_first_home'
                        ], '\t',  data_from_json[j]['down_payment_second_home'
                        ], '\t',  data_from_json[j]['loan_rates_second_home'] 
                print '来自数据库的数据:', '\t', data_from_mysql[i][1
                        ], '\t', data_from_mysql[i][2
                        ], '\t', data_from_mysql[i][3
                        ], '\t', data_from_mysql[i][4
                        ], '\t', data_from_mysql[i][5
                        ], '\t', data_from_mysql[i][6], '\n'
                  
cur.close()
conn.close()

f.close()

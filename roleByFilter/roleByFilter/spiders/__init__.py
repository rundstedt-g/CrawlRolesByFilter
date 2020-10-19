# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
import time
import json

from ..items import RolebyfilterItem


class RolebyfilterSpider(scrapy.Spider):
    name = 'roleByFilter'
    allowed_domains = ['woniu.com']
    url = 'http://jishi.woniu.com/9yin/anonymous/findAllRoles.do?'
    payload = {'propConditions':{'xiuWei':'','neiGongYanXiu':'1','wuXueYanXiu':'','qiXue':'','jinShenWeiLi':'','yuanChengWeiLi':'','neiGongWeiLi':''},'andConditions':[],'orConditions':[],'typeName':'','priceMin':'500','priceMax':''}
    header = {'Content-Type': 'application/json;charset=utf-8'}

    def start_requests(self):
        yield scrapy.Request(url=self.url, headers=self.header, body=json.dumps(self.payload),method="POST",callback=self.parse)

    def parse(self, response):
        print("测试--")
        print(str(response))
        print("--测试")
        sites = json.loads(response.body_as_unicode())
        totalPages = sites[0]['pageInfo']['totalPages']
        for i in range(1,totalPages+1):
            newUrl = self.url + '&pageIndex=' +str(i)
            yield scrapy.Request(url=newUrl, headers=self.header, body=json.dumps(self.payload),method="POST",callback=self.parse_content)

    def parse_content(self, response):
        sites = json.loads(response.body_as_unicode())
        for i in sites[0]['pageData']:
            print(i['itemName'])

            url = 'http://jishi.woniu.com/9yin/roleMsg.do?'
            serverId = 'serverId=' + i['serverId']
            roleUid = '&roleUid=' + i['sellerGameId']
            type = '&type=BaoWuBox&_='
            time_stamp = str(int(time.time()*1000))
            newUrl = url + serverId + roleUid + type +time_stamp
            role = {
                'name':i['itemName'],
                'id':i['id'],
                'price':i['price'],
                'serverName':i['serverName'],
                'gender':i['gender'],
                'reviewStatus':i['reviewStatus']
            }

            yield scrapy.Request(newUrl, callback=self.parse_treasureContent, meta=role)

    def parse_treasureContent(self, response):
        sites = json.loads(response.body_as_unicode())
        msg = json.loads(sites[0]['msg'])
        flag = 0
        for i in msg:
            if i['dataInfo'].find('阎王帖')>0 and i['dataInfo'].find('外功伤害减免忽视')>0 and i['dataInfo'].find('外功暴击伤害')>0 and i['dataInfo'].find('暴击伤害减免')>0:
                flag += 1
        if flag == 5:
            item = RolebyfilterItem()
            item['name'] = response.meta['name']
            item['id'] = response.meta['id']
            item['price'] = response.meta['price']
            item['serverName'] = response.meta['serverName']
            item['gender'] = response.meta['gender']
            if response.meta['reviewStatus'] == 'public':
                item['reviewStatus'] = '公示期'
            else:
                item['reviewStatus'] = '在售'
            yield item

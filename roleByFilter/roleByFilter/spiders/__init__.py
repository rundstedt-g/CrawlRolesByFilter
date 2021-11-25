# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
import time
import json
from lxml import etree
from scrapy.mail import MailSender

from ..items import RolebyfilterItem
from ..items import TreasureItem
from ..items import TreasurePropItem
from ..items import ThreeSkillsItem
from ..items import SkinItem


class RolebyfilterSpider(scrapy.Spider):
    name = 'roleByFilter'
    allowed_domains = ['woniu.com']
    url = 'http://jishi.woniu.com/9yin/anonymous/findAllRoles.do?'
    payload = {'propConditions':{'xiuWei':'','neiGongYanXiu':'1','wuXueYanXiu':'','qiXue':'','jinShenWeiLi':'','yuanChengWeiLi':'','neiGongWeiLi':''},'andConditions':[],'orConditions':[],'typeName':'','priceMin':'','priceMax':''}
    header = {'Content-Type': 'application/json;charset=utf-8'}

    #搜索集市全服所有账号
    def start_requests(self):
        yield scrapy.Request(url=self.url, headers=self.header, body=json.dumps(self.payload),method="POST",callback=self.parse)

    #获取总页数，对每一页进行搜索
    def parse(self, response):
        sites = json.loads(response.text)
        totalPages = sites[0]['pageInfo']['totalPages']
        for i in range(1,totalPages+1):
            newUrl = self.url + '&pageIndex=' +str(i)
            yield scrapy.Request(url=newUrl, headers=self.header, body=json.dumps(self.payload),method="POST",callback=self.parse_content)

    #解析每一页
    def parse_content(self, response):
        sites = json.loads(response.text)
        for i in sites[0]['pageData']:
            url = 'http://jishi.woniu.com/9yin/roleMsgInfo.do?'
            serverId = 'serverId=' + i['serverId']
            itemId = '&itemId=' + str(i['id'])
            type = '&type=OtherProp&_='
            time_stamp = str(int(time.time()*1000))
            newUrl = url + serverId + itemId + type +time_stamp
            role = {
                'id':i['id'],
                'name':i['itemName'],
                'gender':i['gender'],
                'price':i['price'],
                'server':i['areaName']+'-'+i['serverName'],
                'status':'',
                'serverId':i['serverId'],
                'grade':i['gradeName']
            }
            if i['reviewStatus'] == 'public':
                role['status'] = '公示期'
            else:
                role['status'] = '在售'
            yield scrapy.Request(newUrl, callback=self.parse_neigongyanxiu, meta=role)

    #解析内功研修
    def parse_neigongyanxiu(self, response):
        sites = json.loads(response.text)
        msg = sites[0]['msg']
        beg = msg.find("内功研修")+6
        end = msg.find("武学")-4
        neigongyanxiu = msg[beg:end]
        if len(neigongyanxiu)>4 :
            neigongyanxiuFormat = neigongyanxiu[0:len(neigongyanxiu)-4]+"亿"+neigongyanxiu[len(neigongyanxiu)-4:len(neigongyanxiu)]+"万"
        else :
            neigongyanxiuFormat = neigongyanxiu+"万"

        response.meta['neigongyanxiu'] = neigongyanxiuFormat

        url = 'http://jishi.woniu.com/9yin/roleMsgInfo.do?'
        serverId = 'serverId=' + response.meta['serverId']
        itemId = '&itemId=' + str(response.meta['id'])
        type = '&type=NeiGongContainer&_='
        time_stamp = str(int(time.time()*1000))
        newUrl = url + serverId + itemId + type +time_stamp
        yield scrapy.Request(newUrl, callback=self.parse_school, meta=response.meta)

    #解析角色所在实际宗派
    def parse_school(self, response):
        sites = json.loads(response.text)
        msg = json.loads(sites[0]['msg'])
        school = ''
        for i in msg:
            if i['name'] == '淇奥诀' or i['name'] == '风起诀' or i['name'] == '昆仑引' or i['name'] == '昆仑会意功':
                school = '昆仑'
                break
            elif i['name'] == '冰肌玉骨功' or i['name'] == '大乘涅磐功' or i['name'] == '心莲无量功' or i['name'] == '峨眉会意功':
                school = '峨眉'
                break
            elif i['name'] == '魔相诀' or i['name'] == '拍影功' or i['name'] == '噬月神鉴' or i['name'] == '极乐会意功':
                school = '极乐'
                break
            elif i['name'] == '酒雨神功' or i['name'] == '伏龙诀' or i['name'] == '一气海纳功' or i['name'] == '丐帮会意功':
                school = '丐帮'
                break
            elif i['name'] == '纯阳无极功' or i['name'] == '齐天真罡' or i['name'] == '太极神功' or i['name'] == '武当会意功':
                school = '武当'
                break
            elif i['name'] == '葬花玄功录' or i['name'] == '九天凤舞仙诀' or i['name'] == '溪月花香集' or i['name'] == '君子会意功':
                school = '君子'
                break
            elif i['name'] == '太素玄阴经' or i['name'] == '断脉逆心功' or i['name'] == '九转天邪经' or i['name'] == '唐门会意功':
                school = '唐门'
                break
            elif i['name'] == '混天宝纲' or i['name'] == '地狱换魂经' or i['name'] == '修罗武经' or i['name'] == '锦衣会意功':
                school = '锦衣'
                break
            elif i['name'] == '旃檀心经' or i['name'] == '洗髓经' or i['name'] == '灭相禅功' or i['name'] == '少林会意功':
                school = '少林'
                break
            elif i['name'] == '燎原神功' or i['name'] == '明王宝策' or i['name'] == '移天焚海诀' or i['name'] == '明教会意功':
                school = '明教'
                break
            elif i['name'] == '梅影抄' or i['name'] == '云天谱' or i['name'] == '雷音神典' or i['name'] == '天山会意功':
                school = '天山'
                break
        if school == '' :
            school = '未知'

        item = RolebyfilterItem()
        item['itemType'] = 'role'
        item['roleID'] = response.meta['id']
        item['name'] = response.meta['name']
        item['gender'] = response.meta['gender']
        item['school'] = school
        item['neigongyanxiu'] = response.meta['neigongyanxiu']
        item['price'] = response.meta['price']
        item['status'] = response.meta['status']
        item['server'] = response.meta['server']
        item['serverId'] = response.meta['serverId']
        item['grade'] = response.meta['grade']
        yield item

        url = 'http://jishi.woniu.com/9yin/roleMsgInfo.do?'
        serverId = 'serverId=' + item['serverId']
        itemId = '&itemId=' + str(item['roleID'])

        meta_roleID = {
            'id':item['roleID'],
            'serverId':item['serverId']
        }

        type_BaoWuBox = '&type=BaoWuBox&_='
        time_stamp_BaoWuBox = str(int(time.time()*1000))
        newUrl_BaoWuBox = url + serverId + itemId + type_BaoWuBox +time_stamp_BaoWuBox
        yield scrapy.Request(newUrl_BaoWuBox, callback=self.parse_BaoWuBox, meta=meta_roleID)

        type_EquipBox = '&type=EquipBox&_='
        time_stamp_EquipBox = str(int(time.time()*1000))
        newUrl_EquipBox = url + serverId + itemId + type_EquipBox +time_stamp_EquipBox
        yield scrapy.Request(newUrl_EquipBox, callback=self.parse_threeSkills, meta=meta_roleID)

        type_UseCardRec = '&type=UseCardRec&_='
        time_stamp_UseCardRec = str(int(time.time()*1000))
        newUrl_UseCardRec = url + serverId + itemId + type_UseCardRec +time_stamp_UseCardRec
        yield scrapy.Request(newUrl_UseCardRec, callback=self.parse_UseCardRec, meta=meta_roleID)

    #解析宝物匣
    def parse_BaoWuBox(self, response):
        sites = json.loads(response.text)
        msg = json.loads(sites[0]['msg'])
        num = 0
        for i in msg:
            tree = etree.HTML(i['dataInfo'])
            treasureProp = tree.xpath('//font[@color="#FFD700"]') #宝物属性表
            treasureSkill = tree.xpath('//font[@color1="#FF0000"]') #宝物技能表
            name = i['name']

            skillText = ""
            if len(treasureSkill) > 0 :
                skillText = treasureSkill[0].text

            is750 = False
            if name == '翡翠墨玉璜' :
                is750 = True

            tItem = TreasureItem()
            tItem['itemType'] = 'treasure'
            tItem['tID'] = int(str(response.meta['id']) + str(num))
            tItem['roleID'] = response.meta['id']
            tItem['dataInfo'] = i['dataInfo']
            tItem['skill'] = skillText
            tItem['is750'] = is750
            yield tItem

            for j in treasureProp :
                ipItem = TreasurePropItem()
                ipItem['itemType'] = 'treasureprop'
                ipItem['tID'] = int(str(response.meta['id']) + str(num))
                ipItem['prop'] = j.text
                yield ipItem

            num = num +1

    #解析三技能
    def parse_threeSkills(self, response):
        sites = json.loads(response.text)
        msg = json.loads(sites[0]['msg'])
        threeSkillList = []
        for i in msg:
            tree = etree.HTML(i['dataInfo'])
            threeSkills = tree.xpath('//font[@color1="#eb6100"]') #三技能装备
            if len(threeSkills) >= 6 :
                if threeSkills[1].text == threeSkills[3].text and threeSkills[3].text == threeSkills[5].text :
                    threeSkillList.append({'wuxue':threeSkills[0].text, 'ts':threeSkills[1].text, 'dataInfo':i['dataInfo']})

        tsMeta = {'roleID': response.meta['id'],
                  'threeSkillList': threeSkillList}
        url = 'http://jishi.woniu.com/9yin/roleMsgInfo.do?'
        serverId = 'serverId=' + response.meta['serverId']
        itemId = '&itemId=' + str(response.meta['id'])
        type = '&type=EquipToolBox&_='
        time_stamp = str(int(time.time()*1000))
        newUrl = url + serverId + itemId + type +time_stamp
        yield scrapy.Request(newUrl, callback=self.parse_EquipToolBox, meta=tsMeta)

    #解析三技能 2 :装备包里的装备
    def parse_EquipToolBox(self, response):
        sites = json.loads(response.text)
        msg = json.loads(sites[0]['msg'])
        for i in msg:
            tree = etree.HTML(i['dataInfo'])
            threeSkills = tree.xpath('//font[@color1="#eb6100"]') #三技能装备
            if len(threeSkills) >= 6 :
                if threeSkills[1].text == threeSkills[3].text and threeSkills[3].text == threeSkills[5].text :
                    response.meta['threeSkillList'].append({'wuxue':threeSkills[0].text, 'ts':threeSkills[1].text, 'dataInfo':i['dataInfo']})

        if len(response.meta['threeSkillList']) > 0 :
            for ts in response.meta['threeSkillList'] :
                tsItem = ThreeSkillsItem()
                tsItem['itemType'] = 'threeSkills'
                tsItem['roleID'] = response.meta['roleID']
                tsItem['dataInfo'] = ts['dataInfo']
                tsItem['wuxue'] = ts['wuxue']
                tsItem['skill'] = ts['ts']
                yield tsItem

    #解析风物志
    def parse_UseCardRec(self, response):
        sites = json.loads(response.text)
        msg = json.loads(sites[0]['msg'])
        for i in msg:
            tree = etree.HTML(i['dataInfo'])
            skinType = tree.xpath('//font[@color="#FFFFFF"]') #风物志类型
            skinTypeTxt = ''
            beg = i['dataInfo'].find("品质:")+3
            skinQuality = i['dataInfo'][beg:beg+2]
            if len(skinType) < 1 :
                start = i['dataInfo'].find("类型:")+3
                skinTypeTxt =  i['dataInfo'][start:beg-3-4]
            else :
                skinTypeTxt = skinType[0].text

            sItem = SkinItem()
            sItem['itemType'] = 'skin'
            sItem['roleID'] = response.meta['id']
            sItem['name'] = i['name']
            sItem['type'] = skinTypeTxt
            sItem['quality'] = skinQuality
            sItem['photo'] = i['photo']
            yield sItem

    def closed(self,reason):
        endTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        f = open("/srv/scrapy/roleByFilter/roleByFilter/end.txt","w")   # 定义文件对象
        f.write(endTime+'\n'+reason)
        f.close()   # 将文件关闭
        # 发送邮件
        # mailer = MailSender(
        #     smtphost="smtp.qq.com",
        #     mailfrom ="**********@qq.com",
        #     smtpuser ="**********@qq.com",
        #     smtppass ="**********",
        #     smtpport =465,
        #     smtpssl = True
        # )
        # return mailer.send(to={"**********@qq.com"}, subject="今日爬虫完成信息", body=endTime+'\n'+reason)
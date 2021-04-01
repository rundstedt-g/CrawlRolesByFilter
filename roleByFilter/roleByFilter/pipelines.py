# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import pymysql as pymysql
from pymysql.converters import escape_string
import time
from itemadapter import ItemAdapter


class RolebyfilterPipeline:
    def __init__(self):
        # 清空数据库
        self.connect=pymysql.connect(host='localhost',user='root',password='Wx6874024',db='roles')
        self.cursor=self.connect.cursor()
        # 重置记录 txt
        startTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        f = open("/srv/scrapy/roleByFilter/roleByFilter/end.txt","w")   # 定义文件对象
        f.write(startTime+'\n'+'start')
        f.close()   # 将文件关闭

    def open_spider(self, spider):
        # 爬虫开始前，清空所有表的数据
        sqlStatement1 = "TRUNCATE TABLE role"
        self.cursor.execute(sqlStatement1);
        self.connect.commit() #执行
        sqlStatement2 = "TRUNCATE TABLE skin"
        self.cursor.execute(sqlStatement2);
        self.connect.commit() #执行
        sqlStatement3 = "TRUNCATE TABLE threeskills"
        self.cursor.execute(sqlStatement3);
        self.connect.commit() #执行
        sqlStatement4 = "TRUNCATE TABLE treasure"
        self.cursor.execute(sqlStatement4);
        self.connect.commit() #执行
        sqlStatement5 = "TRUNCATE TABLE treasureprop"
        self.cursor.execute(sqlStatement5);
        self.connect.commit() #执行

    def process_item(self, item, spider):
        if item['itemType'] == 'role' :
            sqlStatement = "insert into roles.role (roleID, name, gender, school, neigongyanxiu, price, status, server)VALUES ({},'{}','{}','{}','{}',{},'{}','{}')"
            self.cursor.execute(sqlStatement.format(item['roleID'],item['name'],item['gender'],item['school'],item['neigongyanxiu'],item['price'],item['status'],item['server']))
            self.connect.commit()#执行添加
        elif item['itemType'] == 'treasure' :
            sqlStatement = "insert into roles.treasure (tID, roleID, dataInfo, skill, is750)VALUES ({},{},'{}','{}',{})"
            self.cursor.execute(sqlStatement.format(item['tID'], item['roleID'],escape_string(item['dataInfo']),item['skill'],item['is750']))
            self.connect.commit()#执行添加
        elif item['itemType'] == 'treasureprop' :
            sqlStatement = "insert into roles.treasureprop (tID, prop)VALUES ({},'{}')"
            self.cursor.execute(sqlStatement.format(item['tID'],item['prop']))
            self.connect.commit()#执行添加
        elif item['itemType'] == 'threeSkills' :
            sqlStatement = "insert into roles.threeskills (roleID, dataInfo, wuxue, skill)VALUES ({},'{}','{}','{}')"
            self.cursor.execute(sqlStatement.format(item['roleID'],escape_string(item['dataInfo']),item['wuxue'],item['skill']))
            self.connect.commit()#执行添加
        elif item['itemType'] == 'skin' :
            sqlStatement = "insert into roles.skin (roleID, name, type, quality, photo)VALUES ({},'{}','{}','{}','{}')"
            self.cursor.execute(sqlStatement.format(item['roleID'],item['name'],item['type'],item['quality'],item['photo']))
            self.connect.commit()#执行添加
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()  #关闭连接
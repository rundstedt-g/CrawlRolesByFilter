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
        # 连接数据库
        self.connect=pymysql.connect(host='localhost',user='root',password='root',db='rundstedt')
        self.cursor=self.connect.cursor()
        # 重置记录 txt
        startTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        f = open("/srv/scrapy/roleByFilter/roleByFilter/end.txt","w")   # 定义文件对象
        f.write(startTime+'\n'+'start')
        f.close()   # 将文件关闭

    def open_spider(self, spider):
        # 爬虫开始前，清空所有表的数据
        remove_foreign_key_checks = "SET FOREIGN_KEY_CHECKS=0" # 取消外键约束
        self.cursor.execute(remove_foreign_key_checks);
        self.connect.commit() #执行
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
        sqlStatement5 = "TRUNCATE TABLE treasure_prop"
        self.cursor.execute(sqlStatement5);
        self.connect.commit() #执行
        set_foreign_key_checks = "SET FOREIGN_KEY_CHECKS=1" # 设置外键约束
        self.cursor.execute(set_foreign_key_checks);
        self.connect.commit() #执行

    def process_item(self, item, spider):
        if item['itemType'] == 'role' :
            sqlStatement = "insert into rundstedt.role (id, name, gender, school, neigongyanxiu, price, status, server_name,server_id,grade)VALUES ({},'{}','{}','{}','{}',{},'{}','{}',{},'{}')"
            self.cursor.execute(sqlStatement.format(item['roleID'],item['name'],item['gender'],item['school'],item['neigongyanxiu'],item['price'],item['status'],item['server'],item['serverId'],item['grade']))
            self.connect.commit()#执行添加
        elif item['itemType'] == 'treasure' :
            sqlStatement = "insert into rundstedt.treasure (id, role_id, data_info, wuxue, is750)VALUES ({},{},'{}','{}',{})"
            self.cursor.execute(sqlStatement.format(item['tID'], item['roleID'],escape_string(item['dataInfo']),item['skill'],item['is750']))
            self.connect.commit()#执行添加
        elif item['itemType'] == 'treasureprop' :
            sqlStatement = "insert into rundstedt.treasure_prop (treasure_id, prop) SELECT {},'{}' FROM DUAL WHERE NOT EXISTS (SELECT * FROM rundstedt.treasure_prop WHERE treasure_id= {} AND prop='{}')"
            self.cursor.execute(sqlStatement.format(item['tID'],item['prop'],item['tID'],item['prop']))
            self.connect.commit()#执行添加
        elif item['itemType'] == 'threeSkills' :
            sqlStatement = "insert into rundstedt.threeskills (role_id, data_info, wuxue, skill)VALUES ({},'{}','{}','{}')"
            self.cursor.execute(sqlStatement.format(item['roleID'],escape_string(item['dataInfo']),item['wuxue'],item['skill']))
            self.connect.commit()#执行添加
        elif item['itemType'] == 'skin' :
            sqlStatement = "insert into rundstedt.skin (role_id, name, type, quality, photo)VALUES ({},'{}','{}','{}','{}')"
            self.cursor.execute(sqlStatement.format(item['roleID'],item['name'],item['type'],item['quality'],item['photo']))
            self.connect.commit()#执行添加
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()  #关闭连接
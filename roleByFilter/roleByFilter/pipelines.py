# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import json

from itemadapter import ItemAdapter


class RolebyfilterPipeline:
    def __init__(self):
        self.file = open('role.json', mode='w', encoding='utf-8')
    def process_item(self, item, spider):
        jsondata = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(jsondata)
        return item
    def close_spider(self, spider):
        self.file.close()

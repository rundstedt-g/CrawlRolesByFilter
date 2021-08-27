# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RolebyfilterItem(scrapy.Item):
    itemType = scrapy.Field()
    roleID = scrapy.Field()
    name = scrapy.Field()
    gender= scrapy.Field()
    school = scrapy.Field()
    neigongyanxiu = scrapy.Field()
    price = scrapy.Field()
    status = scrapy.Field()
    server = scrapy.Field()
    serverId = scrapy.Field()
    grade = scrapy.Field()

class TreasureItem(scrapy.Item):
    itemType = scrapy.Field()
    tID = scrapy.Field()
    roleID = scrapy.Field()
    dataInfo = scrapy.Field()
    skill = scrapy.Field()
    is750 = scrapy.Field()

class TreasurePropItem(scrapy.Item):
    itemType = scrapy.Field()
    pID = scrapy.Field()
    tID = scrapy.Field()
    prop = scrapy.Field()

class ThreeSkillsItem(scrapy.Item):
    itemType = scrapy.Field()
    tsID = scrapy.Field()
    roleID = scrapy.Field()
    dataInfo = scrapy.Field()
    wuxue = scrapy.Field()
    skill = scrapy.Field()

class SkinItem(scrapy.Item):
    itemType = scrapy.Field()
    sID = scrapy.Field()
    roleID = scrapy.Field()
    name = scrapy.Field()
    type = scrapy.Field()
    quality = scrapy.Field()
    photo = scrapy.Field()
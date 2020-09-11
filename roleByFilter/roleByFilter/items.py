# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RolebyfilterItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    id = scrapy.Field()
    price = scrapy.Field()
    serverName= scrapy.Field()
    gender= scrapy.Field()
    reviewStatus= scrapy.Field()

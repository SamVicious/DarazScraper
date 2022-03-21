# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DarazItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    # image = scrapy.Field()
    link = scrapy.Field()

class ProductItem(scrapy.Item):
    title = scrapy.Field()
    original_price = scrapy.Field()
    discounted_price = scrapy.Field()
    image = scrapy.Field()
    # rating = scrapy.Field() # requires selenium

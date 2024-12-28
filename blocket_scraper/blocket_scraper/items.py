# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BlocketScraperItem(scrapy.Item):

    dealId = scrapy.Field()
    link = scrapy.Field()
    listTime = scrapy.Field()
    originalListTime = scrapy.Field()
    seller_name = scrapy.Field()
    seller_type = scrapy.Field()
    drivetrain = scrapy.Field() 
    chassi = scrapy.Field()
    color = scrapy.Field()
    heading = scrapy.Field()
    price_amount = scrapy.Field()
    price_billing_period = scrapy.Field()
    ownership_type = scrapy.Field()
    thumbnail = scrapy.Field()
    region = scrapy.Field()
    municipality = scrapy.Field()
    area = scrapy.Field()
    fuel = scrapy.Field()
    gearbox = scrapy.Field()
    regDate = scrapy.Field()
    mileage = scrapy.Field()
    equipment = scrapy.Field()
    description = scrapy.Field()
    images = scrapy.Field()

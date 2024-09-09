# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ExpediaAndroidBotItem(scrapy.Item):
    id = scrapy.Field()
    hotel_name = scrapy.Field()
    hotel_url = scrapy.Field()
    hotel_address = scrapy.Field()
    checkin_date = scrapy.Field()
    checkout_date = scrapy.Field()
    room_id = scrapy.Field()
    room_name = scrapy.Field()
    room_price = scrapy.Field()
    tax_amount = scrapy.Field()
    availability = scrapy.Field()
    occupancy = scrapy.Field()
    page_hash = scrapy.Field()
    currency = scrapy.Field()
    hotel_id = scrapy.Field()


# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DevpostHackathonItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    judges = scrapy.Field()
    criteria = scrapy.Field()
    num_participants = scrapy.Field()
    themes = scrapy.Field()
    total_prize_value = scrapy.Field()
    total_prize_currency = scrapy.Field()
    prizes = scrapy.Field()
    latest_submission_url = scrapy.Field()
    latest_submission_date = scrapy.Field()
    is_ended = scrapy.Field()
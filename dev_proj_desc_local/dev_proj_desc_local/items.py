# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DevProjDescLocalItem(scrapy.Item):
    # define the fields for your item here like:
    project_url = scrapy.Field()

    txt_inspiration = scrapy.Field()
    txt_what_it_does = scrapy.Field()
    txt_how_we_built = scrapy.Field()
    txt_challenges = scrapy.Field()
    txt_accomplishment = scrapy.Field()
    txt_what_we_learned = scrapy.Field()
    txt_whats_next = scrapy.Field()

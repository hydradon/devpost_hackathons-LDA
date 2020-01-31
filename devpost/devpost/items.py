# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DevpostItem(scrapy.Item):
    # define the fields for your item here like:
    project_name = scrapy.Field()
    project_url = scrapy.Field()
    num_likes = scrapy.Field()
    num_cmts = scrapy.Field()
    is_winner = scrapy.Field()
    software_url = scrapy.Field()
    hackathon_urls = scrapy.Field()
    hackathon_names = scrapy.Field()
    win_titles = scrapy.Field()
    build_with = scrapy.Field()
    author = scrapy.Field()
    author_url = scrapy.Field()
    desc_len = scrapy.Field()

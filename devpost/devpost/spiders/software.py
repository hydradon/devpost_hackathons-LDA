# -*- coding: utf-8 -*-
import scrapy
from twisted.python import log as twisted_log
import logging
import idna

class SoftwareSpider(scrapy.Spider):

    logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('software_crawler.log', 'w', 'utf-8-sig')])
    observer = twisted_log.PythonLoggingObserver()
    observer.start()

     # Allow URL with underscore to be crawled. For ex https://dj_pale.itch.io/unknown-grounds
    idna.idnadata.codepoint_classes['PVALID'] = tuple(
        sorted(list(idna.idnadata.codepoint_classes['PVALID']) + [0x5f0000005f])
    )

    name = 'software'
    allowed_domains = ['devpost.com']
    start_urls = ['http://https://devpost.com/software/trending/']

    def parse(self, response):
        pass

# -*- coding: utf-8 -*-
import scrapy
from twisted.python import log as twisted_log
import logging
import idna
import os
import pandas as pd
from devpost_hack_num_submission.items import DevpostHackNumSubmissionItem

class NumsubSpider(scrapy.Spider):
    logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('num_sub_hackathon_crawler.log', 'w', 'utf-8-sig')])
    observer = twisted_log.PythonLoggingObserver()
    observer.start()

    # Allow URL with underscore to be crawled. For ex https://dj_pale.itch.io/unknown-grounds
    idna.idnadata.codepoint_classes['PVALID'] = tuple(
        sorted(list(idna.idnadata.codepoint_classes['PVALID']) + [0x5f0000005f])
    )

    name = 'numsub'
    base_url = 'https://www.devpost.com'
    allowed_domains = ['devpost.com']

    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    df = pd.read_csv(os.path.join(project_dir + "/dataset", 'all_hackathons_cleaned.csv'))

    start_urls = [url + "submissions" for url in df["url"].tolist()]

    # start_urls = start_urls[:5]

    def parse(self, response):
        item = DevpostHackNumSubmissionItem()

        item["hackathon_url"] = response.url.replace("submissions", "")

        numsub = response.css(".items_info b ::text").extract()

        if numsub and len(numsub) > 1:
            item["num_submission"] = int(numsub[1])
        else: 
            item["num_submission"] = 0
        yield item

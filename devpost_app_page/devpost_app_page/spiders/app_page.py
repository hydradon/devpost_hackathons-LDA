# -*- coding: utf-8 -*-
import scrapy
from twisted.python import log as twisted_log
import logging
import idna
import os
import pandas as pd
from html5print import HTMLBeautifier

class AppPageSpider(scrapy.Spider):
    name = 'app-page'

    logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('app_page_crawler.log', 'w', 'utf-8-sig')])
    observer = twisted_log.PythonLoggingObserver()
    observer.start()

     # Allow URL with underscore to be crawled. For ex https://dj_pale.itch.io/unknown-grounds
    idna.idnadata.codepoint_classes['PVALID'] = tuple(
        sorted(list(idna.idnadata.codepoint_classes['PVALID']) + [0x5f0000005f])
    )

    base_url = 'https://www.devpost.com'
    allowed_domains = ['devpost.com']

    data_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    df = pd.read_csv(os.path.join(data_dir + "/dataset", 'all_project_ended_hack.csv'))
    start_urls = df["project_url"].tolist()

    start_urls = ["https://devpost.com/software/cowgary",
                  "https://devpost.com/software/n-c-hoa-kich-d-c"
                 ]

    print(len(start_urls))

    def parse(self, response):
        url = response.url

        # https://devpost.com/software/cowgary
        file_name = self.data_dir + "/raw_html_text/" + response.url.split("/")[4] + ".html"
        os.makedirs(os.path.dirname(file_name), exist_ok=True)

        with open(file_name, "w+", encoding='utf-8-sig') as html_file:
            text = response.css("#app-details-left").extract_first(default = "")
            html_file.write(HTMLBeautifier.beautify(text, 4))
        yield {
            'url': url
        }

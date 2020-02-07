# -*- coding: utf-8 -*-
import scrapy
from twisted.python import log as twisted_log
import logging
import idna
import os
import pandas as pd
from devpost_hackathon.items import DevpostHackathonItem
import re

class HackathonSpider(scrapy.Spider):
    
    logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('hackathon_crawler.log', 'w', 'utf-8-sig')])
    observer = twisted_log.PythonLoggingObserver()
    observer.start()

     # Allow URL with underscore to be crawled. For ex https://dj_pale.itch.io/unknown-grounds
    idna.idnadata.codepoint_classes['PVALID'] = tuple(
        sorted(list(idna.idnadata.codepoint_classes['PVALID']) + [0x5f0000005f])
    )

    name = 'hackathon'
    base_url = 'https://www.devpost.com'
    allowed_domains = ['devpost.com']

    fileDir = os.path.dirname(os.path.abspath(__file__))
    parentDir = os.path.dirname(fileDir)
    grandParentDir = os.path.dirname(parentDir)
    greatGrandParentDir = os.path.dirname(grandParentDir)

    df = pd.read_csv(os.path.join(greatGrandParentDir + "\\dataset", 'all_project.csv'))
    df.dropna(subset=['hackathon_urls'], inplace=True)
    # start_urls = ['https://ubclhd19.devpost.com/', 
    #              'https://alexaisp.devpost.com/']
    start_urls = [hackathon_url for hackathon_url in df['hackathon_urls'].str.split("\|\|").explode().drop_duplicates().tolist()]

    print(start_urls)
    print(len(start_urls))
    # input("here...")

    def parse(self, response):
        item = DevpostHackathonItem()
        item['url'] = response.url
        item["judges"] = "||".join(response.css(".challenge_judge strong ::text").extract())
        item['criteria'] = "||".join(response.css("#judging-criteria strong ::text").extract())
        item['prizes'] = "||".join([i.strip().replace("\n", "") for i in response.css('.prize h6 *::text').extract() if i.strip()])
        item['themes'] = "||".join([i.strip() for i in response.css(".theme ::text").extract() if i.strip()])
        item['is_ended'] = b"This hackathon has ended." in response.body

        prize_value = response.xpath(".//*[@data-currency]//text()").extract()
        if prize_value:
            item['total_prize_currency'] = prize_value[0]
            item['total_prize_value'] = prize_value[1].replace(",", "")
        
        item['num_participants'] = int(re.findall(r'\d+', response.xpath(".//a[@href='/participants']/text()").extract_first(default = "0"))[0])
     
        # Scrape hackathon end date
        request = scrapy.Request(item['url'] + 'submissions/search?sort=recent', callback=self.get_submission_page)
        request.meta['item'] = item

        yield request

    def get_submission_page(self, response):
        item = response.meta['item']

        latest_submission = response.css('*[data-software-id]')[0]
        self.log("Latest submission to hackathon " + item['url'] + 
                " is: " + latest_submission.css('::attr(data-software-id)').extract_first(default = ""))

        item['latest_submission_url'] = latest_submission.xpath("./a/@href").extract_first(default = "")

        if item['latest_submission_url']:
            request = scrapy.Request(item['latest_submission_url'], callback=self.retrieve_latest_submission_date)
            request.meta['item'] = item
            yield request
        else:
            self.log("This hackaton has no submissions!", level=logging.INFO)
            item['latest_submission_date'] = "1970-01-01T00:00:00-05:00"
            yield item
        
    def retrieve_latest_submission_date(self, response):
        item = response.meta['item']

        item['latest_submission_date'] =  response.css(".software-updates .author .timeago::attr(datetime)").extract_first(default = "1970-01-01T00:00:00-05:00")
        yield item
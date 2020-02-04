# -*- coding: utf-8 -*-
import scrapy
from twisted.python import log as twisted_log
import logging
import idna
from devpost.items import DevpostItem

class SoftwareSpider(scrapy.Spider):

    logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('software_crawler.log', 'w', 'utf-8-sig')])
    observer = twisted_log.PythonLoggingObserver()
    observer.start()

     # Allow URL with underscore to be crawled. For ex https://dj_pale.itch.io/unknown-grounds
    idna.idnadata.codepoint_classes['PVALID'] = tuple(
        sorted(list(idna.idnadata.codepoint_classes['PVALID']) + [0x5f0000005f])
    )

    name = 'software'
    base_url = 'https://www.devpost.com'
    allowed_domains = ['devpost.com']
    start_urls = [base_url + '/software/trending/']

    def parse(self, response):
        for item in self.scrape(response):
            yield item

        #crawl next page
        next_page = response.css('.next_page ::attr(href)').extract_first()
        if next_page:
            next_page_url = response.urljoin(next_page)
            print("Found url: {}".format(next_page_url))
        
            yield scrapy.Request(
                next_page_url, 
                callback=self.parse
            )

    def scrape(self, response):
        
        for project in response.css('.gallery-item'):
            item = DevpostItem()

            item['project_url'] = project.css('a ::attr(href)').extract_first()
            item['project_name'] = project.xpath('.//h5/text()').extract_first().strip()
            item['num_likes'] = project.css('.like-count ::text').extract()[1].strip()
            item['num_cmts'] = project.css('.comment-count ::text').extract()[1].strip()
            item['is_winner'] = len(project.css('.winner').extract()) == 1

            request = scrapy.Request(item['project_url'], callback=self.get_project_details)
            request.meta['item'] = item
            yield request

    def get_project_details(self, response):
        item = response.meta['item']

        # item['hackathon_urls'] = response.css('.software-list-content a ::attr(href)').extract_first()
        item['build_with'] = "||".join(response.xpath(".//div[@id='built-with']/ul/li/descendant-or-self::text()").extract())

        # Github or Demo URL
        item['software_url'] = "||".join(response.xpath(".//*[@data-role='software-urls']/li/a/@href").extract())

        author_element = response.css(".software-team-member .user-profile-link")
        item['author'] = "||".join(author_element.css("::text").extract())
        item['author_url'] = "||".join(author_element.css("::attr(href)").extract()[::2])

        # Extract all venues this app is submitted to
        venues = response.css(".software-list-content")

        hackathon_names = []
        hackathon_urls = []
        win_titles = []

        for venue in venues:
            hackathon_urls.append(venue.css("p a ::attr(href)").extract_first())
            hackathon_names.append(venue.css("p a ::text").extract_first())
            win_titles.append("<>".join([i.strip() for i in venue.css("li ::text").extract() if i.strip() and i != "Winner"]))

        item['hackathon_urls'] = "||".join(hackathon_urls)
        item['hackathon_names'] = "||".join(hackathon_names)
        item['win_titles'] = "||".join(win_titles)

        description = response.xpath(".//*[@id='app-details-left']/div[not(@id)]")
        item['desc_len'] = len("".join(description.css("*::text").extract()).replace("\n", ""))
        item['summary_len'] = len(response.xpath(".//*[@id='app-title']/following-sibling::p/text()").extract_first(default = "").strip())
        item['num_imgs'] = len(response.css("#gallery img").extract())
        item['start_date'] = response.css(".software-updates .author .timeago::attr(datetime)").extract_first(default = "")

        yield item
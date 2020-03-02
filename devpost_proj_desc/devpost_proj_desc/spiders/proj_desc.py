# -*- coding: utf-8 -*-
import scrapy
from twisted.python import log as twisted_log
import logging
import idna
import os
import pandas as pd
from devpost_proj_desc.items import DevpostProjDescItem

class ProjDescSpider(scrapy.Spider):
    name = 'proj_desc'
      
    logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('proj_desc_crawler.log', 'w', 'utf-8-sig')])
    observer = twisted_log.PythonLoggingObserver()
    observer.start()

     # Allow URL with underscore to be crawled. For ex https://dj_pale.itch.io/unknown-grounds
    idna.idnadata.codepoint_classes['PVALID'] = tuple(
        sorted(list(idna.idnadata.codepoint_classes['PVALID']) + [0x5f0000005f])
    )

    base_url = 'https://www.devpost.com'
    allowed_domains = ['devpost.com']

    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    df = pd.read_csv(os.path.join(project_dir + "/dataset", 'all_project_ended_hack.csv'))
    start_urls = df["project_url"].tolist()
    # start_urls = [
    #               "https://devpost.com/software/cowgary",
    #               "https://devpost.com/software/n-c-hoa-kich-d-c",
    #               "https://devpost.com/software/radardishes"
    #              ]
    print(len(start_urls))


    def parse(self, response):
        item = DevpostProjDescItem()
        item["project_url"] = response.url

        text_map = {
            "txt_inspiration"    : ["inspiration"],
            "txt_what_it_does"   : ["what it does"],
            "txt_how_we_built"   : ["how", "built"], # How we built it, How I built it
            "txt_challenges"     : ["challenges"],
            "txt_accomplishment" : ["accomplishments"],
            "txt_what_we_learned": ["what", "learned"],
            "txt_whats_next"     : ["what", "next"]
        }

        for section in text_map:
            # trans_string = "translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')"
            # e = response.xpath(".//h2/text()[contains(" + trans_string  +", 'inspiration')]/../following-sibling::*")

            e = response.xpath(".//h2/text()[" + self.build_cond_select_string(text_map[section]) + "]/../following-sibling::*")
            section_text = []
            for sibling in e:
                if sibling.xpath("name()").extract_first(default = "") == "p":
                    section_text.append(sibling.css("::text").extract_first(default = "").strip().replace("\n", " "))
                else:
                    break

            item[section] = " ".join(section_text)

        yield item

    def build_cond_select_string(self, keywords):
        trans_string = "translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')"
        return " and ".join(["contains(" + trans_string  +", '" + word + "')" for word in keywords])

        
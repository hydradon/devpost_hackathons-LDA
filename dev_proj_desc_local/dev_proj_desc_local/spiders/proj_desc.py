# -*- coding: utf-8 -*-
import scrapy
from twisted.python import log as twisted_log
import logging
import idna
import os
import pandas as pd
from dev_proj_desc_local.items import DevProjDescLocalItem
import glob

class ProjDescSpider(scrapy.Spider):
    name = 'proj_desc'
      
    logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('proj_desc_crawler_local.log', 'w', 'utf-8-sig')])
    observer = twisted_log.PythonLoggingObserver()
    observer.start()

     # Allow URL with underscore to be crawled. For ex https://dj_pale.itch.io/unknown-grounds
    idna.idnadata.codepoint_classes['PVALID'] = tuple(
        sorted(list(idna.idnadata.codepoint_classes['PVALID']) + [0x5f0000005f])
    )

    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
  
    files = [f for f in glob.glob(project_dir + "/raw_html_text/*.html", recursive=True)]
    start_urls = ["file:///" + f for f in files]
    
    # start_urls ["file:///D:\\Research\\hackathon-devpost/raw_html_text\\_getthere.html"]
    # start_urls = start_urls[:100]
    print(len(start_urls))
    # exit()

    def parse(self, response):
        item = DevProjDescLocalItem()
        item["project_url"] = response.url.replace("%5C", "\\").replace("file:///", "")

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

        
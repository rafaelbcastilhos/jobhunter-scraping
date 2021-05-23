from scrapy.linkextractors import LinkExtractor
import scrapy
from ..items import JobsItem
from ..named_entity import search_company_name
from ..regex import *


class GeneralSpider(scrapy.Spider):
    name = "job_hunter_spider"
    allowed_domains = []

    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT': 1000
    }

    start_urls = [
        "https://www.nsctotal.com.br/noticias/busca-empregos-na-area-de-ti-em-santa-catarina-fique-atento"
    ]

    def parse(self, response):
        """
        This function parses all pages in stack
        @returns job item and request to all links in scrape page
        @scrapes all links in scrape page
        @scrapes required: title and salary
        @scrapes optional: description, company_name, hiring_type, hierarchy and mode
        """
        print(f"Scrape page {response.url}, {response.meta['depth']}")

        item = JobsItem()

        html = get_html_from_response(response)
        item["title"] = search_general_title(response)
        item["description"] = search_description(html)
        item["company_name"] = search_company_name(html)
        item["hiring_type"] = search_hiring_type(html)
        item["hierarchy"] = search_hierarchy(html)
        item["salary"] = search_salary(html)
        item["mode"] = search_mode(html)
        item["url"] = response.url

        if item["title"] is not None and \
                item["mode"] is not None and (
                item["hierarchy"] is not None or
                item["hiring_type"] is not None or
                item["salary"] is not None):
            yield item

        if response.meta['depth'] < 2:
            link_extractor = LinkExtractor()
            for link in link_extractor.extract_links(response):
                print(f"link: {link.url}")
                yield scrapy.Request(url=link.url, callback=self.parse)

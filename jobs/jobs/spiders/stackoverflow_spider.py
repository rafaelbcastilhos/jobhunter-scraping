import scrapy
from ..items import JobsItem
from ..named_entity import search_company_name
from ..regex import *


class StackoverflowSpider(scrapy.Spider):
    name = "stackoverflow_spider"
    allowed_domains = []

    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT': 1000
    }

    start_urls = ["https://stackoverflow.com/jobs?dr=BackendDeveloper"]

    def parse(self, response):
        """
        This function parses stack overflow backend jobs page
        @url https://stackoverflow.com/jobs?dr=BackendDeveloper
        @returns request to extract links
        @scrapes all jobs links
        """
        self.logger.info(f"Scrape Page {response.url}")

        jobs_links = response.xpath("//div[@class='grid--cell fl1 ']"
                                    "//h2"
                                    "//a"
                                    "/@href").getall()

        self.logger.info(f"links especificos {jobs_links}, tamanho {len(jobs_links)}")

        next_page = response.xpath("//div[@class='s-pagination']"
                                   "//a[last()]"
                                   "/@href").get()

        self.logger.info(f"next {next_page}")

        if jobs_links is not None:
            yield from response.follow_all(jobs_links, callback=self.parse_job)

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_job(self, second_response):
        """
        This function parses stack overflow job pages
        @returns job item
        @scrapes title, company_name, description, hiring_type, hierarchy, salary and mode
        """
        item = JobsItem()

        item["title"] = second_response.xpath(
            "//h1[@class='fs-headline1 sticky:fs-body3 sticky:sm:fs-subheading t mb4 sticky:mb2']"
            "//a"
            "/@title").get()

        item["company_name"] = second_response.xpath(
            "//div[@class='fc-black-700 mb4 sticky:mb0 sticky:mr8 fs-body2 sticky:fs-body1 sticky:sm:fs-caption']"
            "//a"
            "/text()").get()

        item["description"] = second_response.xpath(
            "//div[@class='grid gs16 gsx sm:fd-column fs-body2 fc-medium']"
            "//div[@class='grid--cell6']"
            "//div[3]"
            "//span[@class='fw-bold']"
            "/text()").get()

        html = get_html_from_response(second_response)
        item["hiring_type"] = search_hiring_type(html)
        item["hierarchy"] = search_hierarchy(html)
        item["salary"] = search_salary(html)
        item["mode"] = search_mode(html)
        item["url"] = second_response.url

        self.logger.info(f"Job scraped")
        yield item

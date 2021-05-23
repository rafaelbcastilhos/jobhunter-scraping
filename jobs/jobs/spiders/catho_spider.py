import scrapy
from ..items import JobsItem
from ..regex import *
from ..named_entity import search_company_name


class CathoSpider(scrapy.Spider):
    name = "catho_spider"

    start_urls = ["https://www.catho.com.br/vagas/cientista-de-dados/"]

    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT': 1000
    }

    def parse(self, response):
        """
        This function parses catho home page
        @url https://www.catho.com.br/vagas/cientista-de-dados/
        @returns request to next pages
        @scrapes number of pages
        """
        self.logger.info(f"Scrape Page {response.url}")

        total = response.xpath("//p[@class='sc-hmzhuo gjVMHy']"
                               "/text()").get()

        split = total.split(": ")
        total = int(split[1])
        total = int(total / 20) + 1

        urls = []

        for x in range(2, total + 1):
            urls.append("https://www.catho.com.br/vagas/cientista-de-dados/?q=Cientista%20de%20Dados&page=" + str(x))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, second_response):
        """
        This function parses catho secundary pages
        @url https://www.catho.com.br/vagas/cientista-de-dados/?q=Cientista%20de%20Dados&page={number_of_page}
        @returns request to extract links
        @scrapes all jobs links
        """
        jobs = second_response.xpath("//h2[@class='Title__Heading-sc-14fvmc0-0 fGTSAd sc-csuQGl cBWsYQ']"
                                     "//a"
                                     "/@href").getall()

        for job in jobs:
            yield scrapy.Request(job, callback=self.parse_job)

    def parse_job(self, third_response):
        """
        This function parses catho job pages
        @returns job item
        @scrapes title, salary, description, hiring_type, hierarchy and mode
        """
        item = JobsItem()

        item["title"] = third_response.xpath(
            "//h2[@class='Title__Heading-sc-14fvmc0-0 fGTSAd sc-csuQGl cBWsYQ']"
            "//a"
            "/text()").get()

        item["description"] = third_response.xpath(
            "//span[@class='job-description']"
            "/text()").get()

        html = get_html_from_response(third_response)
        item["company_name"] = search_company_name(html)
        item["hiring_type"] = search_hiring_type(html)
        item["salary"] = search_salary(html)
        item["hierarchy"] = search_hierarchy(html)
        item["mode"] = search_mode(html)
        item["url"] = third_response.url

        yield item

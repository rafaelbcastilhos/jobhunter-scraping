import scrapy
from ..items import JobsItem
from ..regex import *


class VagasSpider(scrapy.Spider):
    name = "vagas_spider"
    allowed_domains = []

    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT': 1000
    }

    start_urls = ["https://www.vagas.com.br/vagas-de-devops"]

    def parse(self, response):
        """
        This function parses vagas devops jobs page
        @url https://www.vagas.com.br/vagas-de-devops
        @returns request to extract links
        @scrapes all jobs links
        """
        self.logger.info(f"Scrape Page {response.url}")

        jobs_links = response.xpath("//div[@class='informacoes-header']"
                                    "//h2"
                                    "//a"
                                    "/@href").getall()

        self.logger.info(f"links especificos {jobs_links}, tamanho {len(jobs_links)}")

        next_page = response.xpath("//div[@id='todasVagas']"
                                   "//a"
                                   "/@href").get()

        self.logger.info(f"next {next_page}")

        if jobs_links is not None:
            yield from response.follow_all(jobs_links, callback=self.parse_job)

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_job(self, second_response):
        """
        This function parses vagas job pages
        @returns job item
        @scrapes title, company_name, description, hiring_type, hierarchy, salary and mode
        """
        item = JobsItem()

        item["title"] = second_response.xpath(
            "//div[@class='job-shortdescription__column job-shortdescription__column--second']"
            "//h1"
            "/text()").get()

        item["company_name"] = second_response.xpath(
            "//div[@class='job-shortdescription__column job-shortdescription__column--second']"
            "//div"
            "//h2"
            "/text()").get()

        item["description"] = second_response.xpath(
            "//div[@class='job-tab-content job-description__text texto']"
            "//p[1]"
            "/text()").get()

        html = get_html_from_response(second_response)
        item["hiring_type"] = search_hiring_type(html)
        item["hierarchy"] = search_hierarchy(html)
        item["salary"] = search_salary(html)
        item["mode"] = search_mode(html)
        item["url"] = second_response.url

        self.logger.info(f"Job scraped")
        yield item

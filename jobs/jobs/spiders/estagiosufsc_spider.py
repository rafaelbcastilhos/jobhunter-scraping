import scrapy
from ..items import JobsItem
from ..regex import *
from ..named_entity import search_company_name


class EstagiosUFSCSpider(scrapy.Spider):
    name = "estagiosufsc_spider"
    allowed_domains = []

    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT': 1000
    }

    start_urls = ["https://estagios.ufsc.br/index.php?page=search&cursos%5B%5D=208"]

    def parse(self, response):
        """
        This function parses estagios ufsc computer science page
        @url https://estagios.ufsc.br/index.php?page=search&cursos%5B%5D=208
        @returns request to extract links
        @scrapes all jobs links
        """
        self.logger.info(f"Scrape Page {response.url}")

        jobs_links = response.xpath("//table"
                                    "//tbody"
                                    "//tr"
                                    "//td"
                                    "//h3"
                                    "//a"
                                    "/@href").getall()

        self.logger.info(f"links especificos {jobs_links}, tamanho {len(jobs_links)}")

        if jobs_links:
            yield from response.follow_all(jobs_links, callback=self.parse_job)

    def parse_job(self, second_response):
        """
        This function parses estagios ufsc job pages
        @returns job item
        @scrapes title, description, company_name, hiring_type, hierarchy, salary and mode
        """
        item = JobsItem()

        html = get_html_from_response(second_response)
        item["title"] = search_title(second_response)

        description = second_response.xpath(
            "//div[@id='description']"
            "//ul"
            "//li"
            "//strong"
            "/text()").getall()

        if "Conhecimentos Desenvolvidos: " in description:
            index = description.index("Conhecimentos Desenvolvidos: ") + 2
            description = second_response.xpath(
                "//div[@id='description']"
                "//ul"
                "//li[" + str(index) + "]"
                "/text()"
            ).getall()
            item["description"] = ' '.join(description)
        else:
            item["description"] = search_description(html)

        item["company_name"] = search_company_name(html)
        item["hiring_type"] = search_hiring_type(html)
        item["hierarchy"] = search_hierarchy(html)
        item["salary"] = search_salary(html)
        item["mode"] = search_mode(html)
        item["url"] = second_response.url

        self.logger.info(f"Job scraped")
        yield item

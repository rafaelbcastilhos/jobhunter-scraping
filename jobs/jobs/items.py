# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class JobsItem(Item):
    title = Field()
    company_name = Field()
    description = Field()
    hierarchy = Field()
    hiring_type = Field()
    mode = Field()
    salary = Field()
    url = Field()

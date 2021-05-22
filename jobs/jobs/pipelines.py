# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
import re
from itemadapter import ItemAdapter


def clean_item(item):
    expression = re.compile(r'[^\x20-\xEB]')

    if item['title'] is not None:
        item['title'] = expression.sub("", item["title"]).strip()
        if len(item['title']) >= 64:
            item['title'] = item['title'][:61] + "..."

    if item['company_name'] is not None:
        item['company_name'] = expression.sub("", item["company_name"]).strip()

    if item['description'] is not None:
        item['description'] = expression.sub("", item["description"]).strip()
        if len(item['description']) >= 128:
            item['description'] = item['description'][:125] + "..."

    if item['hierarchy'] is not None:
        item['hierarchy'] = expression.sub("", item["hierarchy"]).strip()

    if item['hiring_type'] is not None:
        item['hiring_type'] = expression.sub("", item["hiring_type"]).strip()

    if item['mode'] is not None:
        item['mode'] = expression.sub("", item["mode"]).strip()

    if item['salary'] is not None:
        item['salary'] = expression.sub("", item["salary"]).strip()

    return item


class JobsPipeline:
    def open_spider(self, spider):
        # abre arquivo, se nao existir é criado, se existir é adicionado ao final
        self.file = open("jobs.json", 'a+', encoding='utf8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        # limpa o item, converte em dicionário e escreve no arquivo
        job_object = clean_item(item)
        line = json.dumps(
            ItemAdapter(job_object).asdict(), ensure_ascii=False) + ",\n"
        self.file.write(line)

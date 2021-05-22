from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

setting = get_project_settings()
process = CrawlerProcess(setting)

for spider_name in process.spider_loader.list():
    print(f"Running spider {spider_name}")
    process.crawl(spider_name)

# antes de iniciar o crawler, inicia a lista
with open('jobs.json', 'r+', encoding='utf8') as out:
    out.write("[")
    out.close()

process.start()

# após finalizar o crawler, ajusta o json e finaliza a lista
with open('jobs.json', 'a', encoding='utf8') as out:
    out.seek(out.tell() - 2, 0)
    out.truncate()
    out.write("]")
    out.close()

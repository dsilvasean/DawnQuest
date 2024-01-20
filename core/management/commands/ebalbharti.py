from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from collector.collector.spiders.EBalbharti import EbalbhartiSpider 

class Command(BaseCommand):
    help = 'Run the Scrapy spider'

    def handle(self, *args, **options):
        scrapy_settings = {
            "BOT_NAME" :"collector",
            "SPIDER_MODULES" : ["collector.collector.spiders"],
            "NEWSPIDER_MODULE" : "collector.collector.spiders",
            "USER_AGENT" :"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "ROBOTSTXT_OBEY" : False,
            "ITEM_PIPELINES" : {
   "collector.collector.pipelines.EBalbhartiPipeline": 300,
             },
             "REQUEST_FINGERPRINTER_IMPLEMENTATION" : "2.7",
            "TWISTED_REACTOR" : "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
            "FEED_EXPORT_ENCODING" : "utf-8"
        }
        process = CrawlerProcess(scrapy_settings)
        process.crawl(EbalbhartiSpider)  
        process.start()
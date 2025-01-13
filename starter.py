import scrapy
import json
from scrapy.crawler import CrawlerProcess
from scrapy import signals
from pydispatch import dispatcher
from scrapy.utils.log import configure_logging

from Tweeter import Tweeter

# ----- Paste your Tweeter spider code here -----
# (Make sure the Tweeter class is in the same file or properly imported)
# from your_spider_file import Tweeter

class SpiderRunner:
    """
    Simple helper class to run the Tweeter spider programmatically
    and capture the items it scraped.
    """

    def __init__(self):
        """
        :param download_delay: Time in seconds to delay between downloads.
        """

        self.results = []
        # Connect to the 'spider_closed' signal so we can capture the results
        # when the spider finishes crawling.
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)

    def spider_closed(self, spider, reason):
        """
        Called automatically when the spider is closed.
        Here we retrieve the spider's collected results.
        """
        if hasattr(spider, 'spider_results'):
            self.results = spider.spider_results

    def run_spider(self, keyword):
        """
        Run the Tweeter spider with given arguments. Blocks until finished.
        :param keyword: Keyword to search for in tweets (required).
        :param since: Date in YYYY-MM-DD format to filter from.
        :param until: Date in YYYY-MM-DD format to filter up to.
        :return: List of results (dicts) that the spider scraped.
        """
        configure_logging({
            "LOG_FORMAT": "%(levelname)s: %(message)s",
            "LOG_LEVEL": "DEBUG",
        })
        process = CrawlerProcess(settings={
            # Here is where you can set your custom settings.
            # E.g., to respect robots.txt, concurrency, etc.
            "DOWNLOAD_DELAY": 3.0,
            "CONCURRENT_REQUESTS": 1,
            # Feel free to add any other Scrapy settings you want:
            "ROBOTSTXT_OBEY": False,
            # "CONCURRENT_REQUESTS": 16,

        })

        # Schedule the crawl with the Tweeter spider
        process.crawl(
            Tweeter,
            keyword=keyword,
        )

        # This will block (run the Twisted reactor loop) until all spiders finish
        process.start()

        # By the time 'start()' finishes, 'spider_closed' has fired
        # and self.results should be populated.
        print("Number of tweets scraped:", len(self.results))
        return self.results

    def scrubba(searchword):
        spiderr = SpiderRunner()
        twitter_data = spiderr.run_spider(searchword)
        return json.dumps(twitter_data, ensure_ascii=False, indent=2)



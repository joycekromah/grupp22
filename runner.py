from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy import signals
from scrapy.settings import Settings

@defer.inlineCallbacks
def crawl_all(spiders_config):
    """
    Run spiders in parallel but stop and return results as soon as the first successful spider yields items.
    """
    configure_logging({
        "LOG_FORMAT": "%(levelname)s: %(message)s",
        "LOG_LEVEL": "DEBUG",
    })

    base_settings = Settings()
    runner = CrawlerRunner(settings=base_settings)

    results_list = []

    # This will track if we’ve already gotten a result to stop all other spiders
    first_success = False

    @defer.inlineCallbacks
    def run_single_spider(spider_cls, spider_settings, spider_kwargs):
        nonlocal first_success
        # Apply settings dynamically for the spider
        for key, val in spider_settings.items():
            runner.settings.set(key, val, priority="cmdline")

        # Container for this spider’s results
        spider_results = []

        def item_scraped(item, response, spider):

            spider_results.append(item)  # Collect the item


        def spider_closed(spider, reason):
            if reason == "finished":
                first_success = True
                print(f"Spider '{spider.name}' finished")

        # Attach signals
        crawler = runner.create_crawler(spider_cls)
        crawler.signals.connect(item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(spider_closed, signal=signals.spider_closed)

        # Run the spider and wait for its completion
        yield runner.crawl(crawler, **spider_kwargs)

        defer.returnValue(spider_results)

    # Launch spiders in parallel
    deferreds = [
        run_single_spider(
            config["class"],
            config.get("settings", {}),
            config.get("kwargs", {})
        )
        for config in spiders_config
    ]

    try:
        # Wait for any one spider to succeed (or all to fail)
        results = yield defer.DeferredList(deferreds, fireOnOneCallback=True, fireOnOneErrback=False)
        print(f"DeferredList results: {results}")  # Debug log
        # Extract the first successful result
        for result in results:

            defer.returnValue(result)  # Return the first successful spider's results
    except defer.FirstError as e:
        print(f"Error occurred: {e}")

    defer.returnValue([])  # Default to empty if all fail


def run_spiders_async(spiders_config):
    """
    A convenience function to:
      1) Call `crawl_all` with the given spiders_config
      2) Start the reactor if not running
      3) Stop the reactor when done
      4) Return the results.
    """
    d = crawl_all(spiders_config)

    def on_success(results):
        if reactor.running:
            reactor.stop()
        return results

    def on_failure(failure):
        if reactor.running:
            reactor.stop()
        return failure

    d.addCallbacks(on_success, on_failure)

    # If the reactor isn't running, start it
    if not reactor.running:
        reactor.run()

    return d.result
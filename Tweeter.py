import scrapy
from urllib.parse import urlencode
import os

class Tweeter(scrapy.Spider):
    name = "tweeter"
    api_key = os.getenv('ZYTE_API_KEY')
    custom_settings = {
        #"ZYTE_API_KEY": api_key,  # or set in settings.py
        "ROBOTSTXT_OBEY": False,
        #"DOWNLOADER_MIDDLEWARES": {
         #   "scrapy_zyte_api.ScrapyZyteAPIDownloaderMiddleware": 1000,
        #},
        # Default Zyte API args for HTML requests (no JS needed)
        "FEED_EXPORT_ENCODING": "utf-8",
        #"DOWNLOADER_MIDDLEWARES" : {
        #"scrapy_zyte_api.ScrapyZyteAPIDownloaderMiddleware": 1000,
        #},
    }

    def __init__(self, keyword=None, since=None, until=None, url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not keyword:
            raise ValueError("You must provide a keyword to scrape tweets. Use -a keyword='your_keyword'")
        self.keyword = keyword
        self.since = since
        self.until = until
        self.url = url
        self.collected_count = 0
        self.max_tweets = 10
        self.page = 1
        self.spider_results = []



        # Choose a Nitter instance. nitter.net is the main one, but may be rate limited.
        # Consider using another Nitter instance if needed.
        #self.base_url = "http://153.127.64.199:8081/search"
        #self.base_url = "http://46.250.231.226:8889/search"
        #self.base_url = "https://xcancel.com/search"
        #self.base_url = "https://nitter.privacydev.net/search"
        self.base_url = "https://nitter.aishiteiru.moe/search"
        #self.base_url = "https://nitter.pek.li/search"
        #self.base_url = url

    def start_requests(self):
        # Construct initial search URL.
        # Nitter's search can often be done by ?q=keyword&f=tweets
        # For example: https://nitter.net/search?q=keyword&f=tweets
        query_params = {
            "f": "tweets",
            "q": self.keyword
        }

        if self.since:
            query_params["since"] = self.since
        if self.until:
            query_params["until"] = self.until

        url = f"{self.base_url}?{urlencode(query_params)}"


        yield scrapy.Request(
            url,
            callback=self.parse_search_results,
        )

    def parse_search_results(self, response):
        # Select each timeline-item, which represents a tweet
        tweet_selectors = response.css('.timeline .timeline-item')
        for tweet in tweet_selectors:
            # Extract tweet text from the tweet-content element
            tweet_text = " ".join(tweet.css('.tweet-content.media-body::text').getall()).strip()

            if tweet_text:
                self.collected_count += 1
                item = {"text": tweet_text}
                self.spider_results.append(item)
                yield item
                #print(f"Added item: {item} | Total items: {len(self.spider_results)}")  # Debug log
                if self.collected_count >= self.max_tweets:
                    return  # Stop if we've reached our target number of tweets

        # If we need more tweets and pagination is required, handle pagination or load more logic here.
        # (This depends on how the Nitter instance or page is structured, possibly incrementing 'page' param.)


        # Check if we need more tweets
        if self.collected_count < self.max_tweets:
            # Nitter paginates by appending &page=2, &page=3, etc.
            self.page += 1
            next_page_url = self._build_next_page_url(response.url)
            if next_page_url:
                yield scrapy.Request(
                    next_page_url,
                    callback=self.parse_search_results,

                )

    def _build_next_page_url(self, current_url):
        # Construct the next page URL by incrementing page param.
        # If current URL already had a page param, replace it. Otherwise, add one.
        # A simple approach is to parse query params and increment page.
        from urllib.parse import urlparse, parse_qs, urlunparse, urlencode

        parsed = urlparse(current_url)
        qs = parse_qs(parsed.query)
        qs["page"] = [str(self.page)]
        new_query = urlencode(qs, doseq=True)
        new_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))
        return new_url

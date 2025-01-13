# Scrapy settings for yourproject





# Identify yourself (and your project) on the user-agent if you wish
# USER_AGENT = "yourproject (+http://www.yourdomain.com)"

# Adhere to robots.txt or not
ROBOTSTXT_OBEY = False

# Configure a delay for requests to avoid overwhelming servers
# 1 second delay between requests might be good starting point
DOWNLOAD_DELAY = 1.5

# Optional: Limit concurrent requests as Nitter instances might be rate-limited
CONCURRENT_REQUESTS = 4



# Enable Zyte’s Smart Proxy Manager middleware
#DOWNLOADER_MIDDLEWARES = {
  #  "scrapy_zyte_api.ZyteAPIDownloaderMiddleware": 1000,
    # You can also keep the default middlewares if needed
    # "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": 400,
    # "scrapy.downloadermiddlewares.retry.RetryMiddleware": 550,
    # etc.
#}

# Configure Zyte API default arguments:
# For Nitter, we generally don't need browser rendering, so set browserRender to False.

DOWNLOADER_MIDDLEWARES = {
    "scrapy_zyte_api.ScrapyZyteAPIDownloaderMiddleware": 1000,
}


FEED_EXPORT_ENCODING = "utf-8"
#ADDONS = {
 #   "scrapy_zyte_api.Addon": 500,
#}

# Enable or disable spider middlewares, if needed:
# SPIDER_MIDDLEWARES = {
#     "yourproject.middlewares.YourSpiderMiddleware": 543,
# }

# Configure item pipelines if needed:
# ITEM_PIPELINES = {
#     "yourproject.pipelines.YourPipeline": 300,
# }

# Log level can be adjusted as desired for debugging:
LOG_LEVEL = "INFO"

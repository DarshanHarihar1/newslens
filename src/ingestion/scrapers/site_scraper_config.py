# scrapers/site_scraper_config.py

SITE_CONFIGS = [
    {
        "name": "ExampleSiteA",
        "start_url": "https://www.example-site-a.com",
        "article_container_xpath": "//div[@class='article']",
        "title_xpath": ".//h2[@class='title']",
        "link_xpath": ".//a",
        "pagination_enabled": True,
        "pagination_xpath": "//a[@class='next-page']",
    },
    {
        "name": "ExampleSiteB",
        "start_url": "https://www.example-site-b.com/news",
        "article_container_xpath": "//div[@class='post']",
        "title_xpath": ".//h1",
        "link_xpath": ".//a",
        "pagination_enabled": False,
        # No pagination for this site
    },
    # Add more site configs as needed
]
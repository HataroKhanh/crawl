from xuongmoc import *
payload = {
        "page": 1,
        "slug": "tin-tuc",
        "taxonomy": "category",
        "get": "more"
    }
Crawler = Crawler()
print(Crawler.crawl_post_links("https://xuongmocdct.com.vn/load-more-cat-post",payload))
import xuongmoc
import json
Crawler = xuongmoc.Crawler(
)
payload = {
        "page": 1,
        "slug": "tin-tuc",
        "taxonomy": "category",
        "get": "more"
    }
data = Crawler.crawl_post_links("https://xuongmocdct.com.vn/load-more-cat-post",payload)
with open('links.json',"w",encoding="utf-8") as f:
    json.dump(f)
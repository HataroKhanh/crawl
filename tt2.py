from xuongmoc import *
import requests
import time
urls = [
'https://xuongmocdct.okmedia.vn/lua-chon-tap-dau-giuong-dep-cho-khong-gian-phong-ngu-2024.html',
'https://xuongmocdct.okmedia.vn/tu-quan-ao-go-thong.html'
]

payload = {
        "page": 1,
        "slug": "tin-tuc",
        "taxonomy": "category",
        "get": "more"
    }
""" 
https://xuongmocdct.okmedia.vn/product/ajax_more_product"""
name_path_images = []
name_posts = []
my_web = "xuongmocdct.okmedia.vn"
crawler = Crawler()
poster = Poster(r"admin", r"QWuX RD3k L71G Uige lvEp KhQC", "https://xuongmocdct.okmedia.vn/wp-json/wp/v2/posts/")

"""
noi-that-phong-khach
noi-that-phong-bep
noi-that-phong-ngu
noi-that-van-phong
"""

"""wckK vx6u XWEn Ml91 Q5Ao Wg45"""
# print(crawler.crawl_woo_category("https://xuongmocdct.okmedia.vn/product/ajax_more_product",payload))
# for i in crawler.crawl_woo_category("https://xuongmocdct.okmedia.vn/product/ajax_more_product",payload):
#     product_data = crawler.crawl_product(i,my_web)

for link in urls: 
    Spost = crawler.crawl_post(link,"xuongmocdct.okmedia.vn")
    print(Spost)
    if Spost['name_path_images']:
     data_post = poster.post_image("https://xuongmocdct.okmedia.vn/wp-json/wp/v2",f"imgs/{Spost['name_path_images']}")
    if data_post:
        id_feat = data_post['id']
    else:
         id_feat = None
    name_posts.append({"spost":Spost,'id_feat':id_feat,'slug':Spost['slug']})
    name_path_images.extend(Spost['name_path_images'])

    
# # upload img
for imgs in set(name_path_images):
        for img in imgs:
            poster.post_image("https://xuongmocdct.okmedia.vn/wp-json/wp/v2",f"imgs/{img}")
# print(name_posts)
for post in name_posts:
    poster.post_content(post['spost']['title'],post['spost']['content'],post["id_feat"],post['slug'])


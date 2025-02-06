from xuongmoc import *
import time

name_path_images = []
name_posts = []
my_web = "xuongmocdct.okmedia.vn"
crawler = Crawler()
poster = Poster(
    r"admin",
    r"QWuX RD3k L71G Uige lvEp KhQC",
    "https://xuongmocdct.okmedia.vn/wp-json/wp/v2/posts/"
)

woo_url = "https://xuongmocdct.okmedia.vn/wp-json/wc/v3/products"
consumer_key = "ck_7d6605d3815d983ba84b91b0a1e25bf93f25053d"
consumer_secret = "cs_f32ebacb160ad6ec5f2d4e15b276fd04e8001a79"
woocomercy = Woocomercy_Product(woo_url, consumer_key, consumer_secret)

categories = [
    "noi-that-phong-khach",
    "noi-that-phong-bep",
    "noi-that-phong-ngu",
    "noi-that-van-phong"
]

dem = 0

for category in categories:
    payload = {
        "category": category,
        "ancestor": category,
        "page": 1
    }

    for product_url in crawler.crawl_woo_category("https://xuongmocdct.com.vn/product/ajax_more_product", payload):
        imgs = []
        product_data = crawler.crawl_product(product_url, my_web)

        if product_data is None:
            print(f"⚠️ Bỏ qua sản phẩm: {product_url} do không thể lấy dữ liệu!")
            continue  # Bỏ qua nếu không lấy được thông tin sản phẩm

        # Xử lý ảnh sản phẩm
        if product_data["all_imgs"]:
            for img in product_data["all_imgs"]:
                if img:
                    imgs.append({"src": f"https://{my_web}/wp-content/uploads/{img}"})
        else:
            imgs = None

        # Đăng sản phẩm lên WooCommerce
        woocomercy.post_product(
            title=product_data["title"],
            price=product_data["price"],
            img_names=imgs,
            category='',
            content=product_data["content"],
        )

        # Tránh bị chặn do gửi quá nhiều request liên tục
        dem += 1
        if dem % 30 == 0:
            print("⏳ Nghỉ 50 giây để tránh bị chặn...")
            time.sleep(50)

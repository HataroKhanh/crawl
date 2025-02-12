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
url = [
    'https://xuongmocdct.com.vn/noi-that-van-phong/ban-lam-viec-mau-xam-bac-blvxmdct10',
    'https://xuongmocdct.com.vn/noi-that-van-phong/ghe-van-phong-cong-thai-hoc-mau-hong-gvpxmdct03',
    'https://xuongmocdct.com.vn/noi-that-van-phong/ban-lam-viec-phong-cach-vintage-blvxmdct05',
    'https://xuongmocdct.com.vn/noi-that-van-phong/ban-lam-viec-chat-lieu-sang-trong-blvxmdct01',
    'https://xuongmocdct.com.vn/noi-that-van-phong/ban-may-tinh-bang-go-blvxmdct02',
    'https://xuongmocdct.com.vn/noi-that-van-phong/ban-lam-viec-go-cong-nghiep-blvxmdct03',
    'https://xuongmocdct.com.vn/noi-that-van-phong/ban-lam-viec-hinh-chu-l-blvxmdct04',
    'https://xuongmocdct.com.vn/noi-that-phong-khach/sofa-thu-gian-hoan-hao-cho-phong-khach-gfdct06',
    'https://xuongmocdct.com.vn/noi-that-phong-ngu/ban-trang-diem-venice-go-tu-nhien-ket-hop-guong-btfdct03',
    'https://xuongmocdct.com.vn/noi-that-phong-ngu/ban-trang-diem-diel-ket-hop-guong-btfdct04',
    'https://xuongmocdct.com.vn/noi-that-phong-bep/tu-bep-go-cong-nghiep-phoi-mau-trang-xam-an-tuong-tbdct09',
    'https://xuongmocdct.com.vn/noi-that-phong-bep/ban-an-go-liverpool-4-ghe-bfgdct03',
    'https://xuongmocdct.com.vn/noi-that-phong-bep/ban-an-ceramic-winston-8-ghe-bfdct05',
    'https://xuongmocdct.com.vn/noi-that-phong-bep/ghe-an-chan-sat-georgia-gpsdct03',
    'https://xuongmocdct.com.vn/noi-that-phong-bep/ghe-an-chan-sat-cao-cap-winston-gpsdct05',
    'https://xuongmocdct.com.vn/noi-that-phong-bep/ban-an-go-value-4-ghe-bfgdct04',
    'https://xuongmocdct.com.vn/noi-that-phong-bep/ghe-an-go-cao-su-value-gpgdct04',
    'https://xuongmocdct.com.vn/noi-that-phong-bep/ghe-an-go-houston-gpgdct05',
    'https://xuongmocdct.com.vn/noi-that-phong-bep/ghe-an-go-ket-hop-pvc-gpgdct06',
    'https://xuongmocdct.com.vn/noi-that-phong-bep/ghe-an-xoay-florin-gpdct01',
    'https://xuongmocdct.com.vn/noi-that-phong-bep/ghe-an-go-cao-su-liverpool-gpgdct03',
    'https://xuongmocdct.com.vn/noi-that-phong-bep/ban-an-firenze-2-ghe-bfdct05',
    'https://xuongmocdct.com.vn/noi-that-phong-bep/ban-an-24-ghe-mo-rong-picnic-bfdct01',
    'https://xuongmocdct.com.vn/noi-that-phong-bep/ban-an-2-ghe-picnic-chan-tru-bfdct02',
    'https://xuongmocdct.com.vn/noi-that-phong-bep/bo-ban-ghe-an-stdct13-6-ghe-sang-trong-va-lich-lam',
    'https://xuongmocdct.com.vn/noi-that-phong-ngu/giuong-ngu-go-bddct09-phong-cach-rustic-tone-mau-nau-tram',
    'https://xuongmocdct.com.vn/noi-that-phong-ngu/tu-ao-canh-lua-go-cong-nghiep-thiet-ke-thong-minh',
    'https://xuongmocdct.com.vn/noi-that-phong-ngu/tu-ao-wddct06-canh-mo-mau-trang-chat-lieu-go-sang-trong',
    'https://xuongmocdct.com.vn/noi-that-phong-ngu/don-ban-phan-thiet-ke-hinh-oval-voi-2-chan-tru-chac-chan',
    'https://xuongmocdct.com.vn/noi-that-phong-ngu/ghe-don-phong-ngu-khung-chan-sat-dem-ngoi-em-ai',
    'https://xuongmocdct.com.vn/noi-that-phong-ngu/ban-phan-treo-tuong-tone-mau-trang-thiet-ke-hien-dai',
    'https://xuongmocdct.com.vn/noi-that-phong-ngu/don-ban-phan-phong-ngu-hinh-tru-thiet-ke-moi-la',
    'https://xuongmocdct.com.vn/noi-that-van-phong/ban-lam-viec-nho-xinh-kem-gia-sach',
    'https://xuongmocdct.com.vn/noi-that-phong-ngu/tap-dau-giuong-btdct09-mau-trang-phong-cach-tan-co',
    'https://xuongmocdct.com.vn/noi-that-phong-ngu/giuong-ngu-boc-ni-bddct07',
    'https://xuongmocdct.com.vn/noi-that-phong-ngu/tap-dau-giuong-btdct08',
    'https://xuongmocdct.com.vn/noi-that-phong-bep/bo-ban-ghe-an-stdct11-04',
    'https://xuongmocdct.com.vn/noi-that-phong-bep/bo-ban-ghe-an-stdct12-04',
    'https://xuongmocdct.com.vn/noi-that-phong-ngu/giuong-ngu-go-bddct06',
    'https://xuongmocdct.com.vn/noi-that-phong-ngu/giuong-ngu-boc-ni-bdct08',
    'https://xuongmocdct.com.vn/noi-that-phong-ngu/tap-dau-giuong-btdct05',
    'https://xuongmocdct.com.vn/noi-that-phong-ngu/tap-dau-giuong-btdct06',
    'https://xuongmocdct.com.vn/noi-that-phong-ngu/tap-dau-giuong-btdct03',
    'https://xuongmocdct.com.vn/noi-that-phong-ngu/tap-dau-giuong-btdct07',
    'https://xuongmocdct.com.vn/noi-that-phong-ngu/tap-dau-giuong-btdct02',
]

for product_url in url:
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

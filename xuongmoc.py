import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
import os
import json
"""https://xuongmocdct.com.vn/"""
class Crawler:
    def __init__(self):
        self.session = requests.Session()  
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        })

    def crawl_post_links(self, path_web, payload):
        all_links = []
        payload = payload.copy()  

        while True:
            response = self.session.post(path_web, data=payload)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Find all elements with 'other-item' class
                items = soup.find_all(class_='other-item')
                
                # Create list of [img, link] for each item
                alls = []
                for item in items:
                    img = item.find('img', src=True)
                    link = item.find('a', href=True)
                    
                    if img and link:
                        
                        img = self.download_image(img['src'],'imgs/')
                        alls.append([img, link['href']])
                
                # Break condition
                if not items:
                    break
                else:
                    all_links.extend(alls)
                
                # Increment page
                payload['page'] += 1
            else:
                print(f"Error! Status code: {response.status_code}")
                break  
        
        return all_links
    
    def download_image(self, img_url, save_dir):
        try:
            img_name = os.path.basename(urlparse(img_url).path)
            img_data = self.session.get(img_url).content
            
            with open(os.path.join(save_dir, img_name), 'wb') as f:
                f.write(img_data)
            print(f"Đã tải xuống: {img_name}")
            return img_name

        except Exception as e:
            print(f"Không thể tải xuống {img_url}: {e}")
            return img_name
        
    def crawl_post(self, url, my_web):
        response = self.session.get(url)
        allowed_tags = {
            'p', 'span', 'img', 'audio', 'video', 'source', 'a', 
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'li', 'ol', 
            'table', 'tr', 'td', 'th', 'thead', 'tbody', 'tfoot'
        }
        unwanted_tags = ["blog-navigation", "the-tags", "post_meta", "relation","toc-list",'entry-header','single-title']
        name_path_images = []

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            imgs = soup.find_all('img')
            # Lấy tiêu đề
            title = soup.find('h1').text
            soup = soup.find(class_="single-post")

            for tag in soup.find_all(recursive=True):
                if tag.name and any(unwanted_class in tag.get('class', []) for unwanted_class in unwanted_tags):
                    tag.decompose()


            content = re.sub(r'</?article[^>]*>', '', str(soup))
            content = re.sub(r'</?div[^>]*>', '', str(content))


            for img_tag in imgs:
                img_url = img_tag.get('src')
                if img_url:
                    img_url = urljoin(url, img_url)
                    name_img = self.download_image(img_url, 'imgs/')
                    name_path_images.append(name_img)


            cleaned_content = re.sub(r'\s(class|style|id)="[^"]*"', '', str(content))

            cleaned_content = re.sub(
                r'https://xuongmocdct.com.vn/',
                lambda match: match.group(0).replace("https://xuongmocdct.com.vn", f"https://{my_web}"),
                cleaned_content
            )
            cleaned_content = re.sub(
                r'/uploads/Tin-tuc/',
                "/wp-content/uploads/",
                cleaned_content
            )
            # Trả về kết quả
            return {"title": fr"{title}", "content": fr"{cleaned_content}","name_path_images":name_path_images}

    def crawl_woo_category(self,way_url,payload) -> list:
        """example of payload
            payload = {
                "category": noi-that-phong-khach,
                "slug": "noi-that-phong-khac",
                "page": 1
            }
        """
        all_links = []
        payload = payload.copy()  
        
        while 1:
            response = self.session.post(way_url,data=payload)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content,"html.parser")
                
                a_links = soup.find_all("a",class_="p-name")
                if a_links!=[]:
                    for a_link in a_links:
                        all_links.append(a_link.get("href"))
                else:
                    break
                    
                if "page" in payload:
                    payload['page']+=1
                else:
                    print("page not in payload")
                    break
            else:
                print("end page")
                break
        return all_links

    def crawl_product(self,url,my_web) -> dict: 
        response = self.session.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content,"html.parser")
            
            title = soup.find('h1',class_="title-global").text.strip()
            
            category_tag = soup.find("p",class_="price_sale")
            category_tag = soup.find("p",class_="category").find_all('a')
            all_category = []
            all_imgs = []

            for category in category_tag:
                category = category.text
                all_category.append(category)
                
            imgs_product = soup.find(class_="picture")
            imgs_product = imgs_product.find_all('img')
            for img_link in imgs_product:
                src = img_link.get("src")
                new_src = f"https://{my_web}/wp-content/uploads/img{src}"

                img_link['src'] = new_src

                all_imgs.append(self.download_image(new_src, "imgs/"))
                
            area_price = soup.find("div",class_="area_price")
            price = area_price.find("strong").text
            price = re.sub(r"[^\d]", "", price)
            
            content = soup.find(id="specs")
            for tag in content.find_all("img"):
                href = tag.get('src')
                # Replace path with just the filename, supporting multiple file extensions
                tag['src'] = re.sub(r'^(https://xuongmocdct\.com\.vn)?(/uploads/[^/]+/)?([^/]+\.\w+)$', r'https://xuongmocdct.com.vn/wp-content/uploads/\3', href)
            
            
            content = re.sub(r'</?article[^>]*>', '', str(content))
            content = re.sub(r'</?div[^>]*>', '', str(content))

            cleaned_content = re.sub(r'\s(class|style|id)="[^"]*"', '', str(content))

            cleaned_content = re.sub(
                r'https://xuongmocdct.com.vn/',
                lambda match: match.group(0).replace("https://xuongmocdct.com.vn", f"https://{my_web}"),
                cleaned_content
            )

            return {"title":fr"{title}","category":category,'price':price,"content":cleaned_content,"all_imgs":all_imgs}
        else:
            return None
    
class Poster(Crawler):
    def __init__(self, user_name, password, webname):
        super().__init__()
        self.user_name = user_name
        self.password = password
        self.webname = webname
        self.id = 1
        
        self.auth = (self.user_name, self.password)

    def post_content(self, title, content,featured_media):
        post_data = {
            "title": str(title),
            "content": str(content),
            "status": "publish",
            "featured_media" : featured_media
            
        }
        
        try:
            response = self.session.post(self.webname, json=post_data,auth=self.auth)
            if response.status_code == 201:  # Assuming 201 is for successful creation
                print("Post created successfully!")
                return response.json()  
            else:
                print(f"Failed to create post: {response.status_code}")
                print(response.text)
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
    def post_image(self,BASE_URL,image_path):
        """Upload an image to WordPress and return the image URL."""
        url = f"{BASE_URL}/media"
        try:
            with open(image_path, 'rb') as image_file:
                files = {'file': image_file}
                headers = {"Content-Disposition": f"attachment; filename={image_path}"}
                
                response = requests.post(url, headers=headers, files=files, auth=self.auth)
                if response.status_code == 201:
                    print("Image uploaded successfully.")
                    return response.json()
                else:
                    print(f"Failed to upload image. Response: {response.text}")
                    return None
        except:
            return
class Woocomercy_Product:
    def __init__(self, url, consumer_key, consumer_secret):
        self.url = url
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret


    def post_product(self, title, price, img_names, category, content):
        """
        Tạo sản phẩm mới trên WooCommerce qua API.
        """

        # Dữ liệu sản phẩm
        data = {
            "name": title,  # Tiêu đề
            "type": "simple",  # Loại sản phẩm
            "regular_price": str(price),  # Giá sản phẩm (phải là chuỗi)
            "description": content,  # Nội dung
            "categories": [{"slug": category}],  # Thể loại theo slug
            "images": img_names  # Danh sách ảnh (URL)
        }

        try:
            # Gửi yêu cầu POST để tạo sản phẩm
            response = requests.post(
                self.url,
                auth=(self.consumer_key, self.consumer_secret),  # Basic Auth
                json=data,  # Dữ liệu dưới dạng JSON
                headers={"Content-Type": "application/json; charset=UTF-8"}  # Đảm bảo UTF-8
            )

            # Kiểm tra phản hồi
            if response.status_code == 201:  # HTTP 201 Created
                print(f"Sản phẩm '{title}' đã được tạo thành công:", response.json())
                return response.json()
            else:
                print(f"Lỗi khi tạo sản phẩm '{title}':", response.status_code, response.text)
                return None
        except requests.exceptions.RequestException as e:
            print(f"Đã xảy ra lỗi khi gửi yêu cầu tạo sản phẩm: {e}")
            return None


         
if __name__ == "__main__":
    payload = {
        "page": 1,
        "slug": "tin-tuc",
        "taxonomy": "category",
        "get": "more"
    }
    """ 
    https://xuongmocdct.com.vn/product/ajax_more_product"""
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
    # print(crawler.crawl_woo_category("https://xuongmocdct.com.vn/product/ajax_more_product",payload))
    # for i in crawler.crawl_woo_category("https://xuongmocdct.com.vn/product/ajax_more_product",payload):
    #     product_data = crawler.crawl_product(i,my_web)
        
    links = crawler.crawl_post_links("https://xuongmocdct.com.vn/load-more-cat-post",payload)
    
    for link in links: 
        Spost = crawler.crawl_post(link[1],"xuongmocdct.okmedia.vn")
        data_post = poster.post_image("https://xuongmocdct.okmedia.vn/wp-json/wp/v2",f"imgs/{link[0]}")
        id_feat = data_post['id']
        print(id_feat)
        name_posts.append({"spost":Spost,'id_feat':id_feat})
        name_path_images.extend(Spost['name_path_images'])
        
        
    # upload img
    for imgs in set(name_path_images):
         for img in imgs:
           poster.post_image("https://xuongmocdct.okmedia.vn/wp-json/wp/v2",f"imgs/{img}")
    # print(name_posts)
    for post in name_posts:
        poster.post_content(post['spost']['title'],post['spost']['content'],post["id_feat"])
        
    

    
  

                        
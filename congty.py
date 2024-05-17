from bs4 import BeautifulSoup
import requests
import json 
import base64
from io import BytesIO
from PIL import Image
import pytesseract
from collections import defaultdict
import sys
import time


url_api = "https://tmproxy.com/api/proxy/get-new-proxy"
data_api = {
    "api_key": "0741366b7d66deb86cfb0662382f3cd3",
    "id_location": 0,
}

post_api = requests.post(url_api,json=data_api)
post_api_json = json.loads(post_api.text)
print(post_api_json)
proxy_https = post_api_json["data"]["https"]
hanoi = defaultdict(lambda: defaultdict(dict))
url = "https://www.tratencongty.com/thanh-pho-ha-noi/"
response  = requests.get(url,proxies={"https": proxy_https})
print(proxy_https)
def regex(soup):
    address = soup.find(string=lambda t: "Địa chỉ:" in t)
    address = address.split(":")[1].strip()
    representative = soup.find(string=lambda t: "Đại diện pháp luật:" in t)
    representative = representative.split(":")[1].strip()
    #print(soup)
    return (address,representative)

def base_64_convert(data,file_name):
    data = data.split(',')[1]
    data = data.encode('utf-8')
    data = base64.decodebytes(data)
    with open(f'{file_name}.jpg', 'wb') as image_file:
        image_file.write(data)
    return

def img_to_text(file_name):
    img = Image.open(f'{file_name}.jpg')
    return pytesseract.image_to_string(img, config='--psm 6')


if response.status_code == 200:
    html_quan = BeautifulSoup(response.content,features="html.parser")
    table_quan = html_quan.findAll('a',class_="list-group-item")
    for tag_table_quan in table_quan[2:]:
        name_quan = tag_table_quan.get("href").split('/')[-2].replace('-','_')
        title_quan = tag_table_quan.get('title') 
        url_quan = tag_table_quan.get('href')+'/'
        print(f'{title_quan}:')

        response_phuong = requests.get(url_quan,proxies={"https": proxy_https})

        if response_phuong.status_code==200:
            html_phuong = BeautifulSoup(response_phuong.content,features="html.parser")
            table_phuong = html_phuong.findAll('a','list-group-item')
            for tag_table_phuong in table_phuong[2:]:
                name_phuong = tag_table_phuong.get('href').split('/')[-2].replace('-','_')
                title_phuong = tag_table_phuong.get('title')
                url_phuong = tag_table_phuong.get('href')
                page = 1
                list_companies = []
                name_companies_dict = defaultdict(lambda:0)
                while 1:
                    try:
                        response_page = requests.get(url_phuong + f'?page={page}',proxies={"https": proxy_https})

                        html_companies = BeautifulSoup(response_page.content,features="html.parser")
                        html_company_class = html_companies.findAll('div',class_="search-results")
                        if html_company_class != []:
                            for tag_div_companies in html_company_class:
                                tag_a_company = tag_div_companies.find('a')
                                url_company = tag_a_company.get('href')+'/'

                                response_company = requests.get(url_company,proxies={"https": proxy_https})

                                if response_company.status_code == 200:
                                    html_company = BeautifulSoup(response_company.content,features="html.parser")
                                    table_company = html_company.find(class_="jumbotron")
                                    tag_img_company =  table_company.findAll('img')
                                    name_company = table_company.find('span').text
                                    if name_company in name_companies_dict:
                                        name_company =  name_company+str(name_companies_dict[name_company]+1)
                                    
                                    address,representative = regex(table_company)
                                    try:
                                        phone_data64_img =  tag_img_company[1].get('src')
                                        base_64_convert(phone_data64_img,name_company)
                                        phone_number=img_to_text(name_company)
                                    except Exception as e:
                                        print(e)
                                        phone_number = "No PhoneNumber"
                                    
                                    dict_company = {"Tên công ty":name_company,
                                                    "Đại diện pháp luật":representative,
                                                    "Địa chỉ":address,
                                                    "Số điện thoại":phone_number.replace('\n','').replace("\x0c","")
                                        }
                                    
                                    list_companies.append(dict_company)
                                    print(dict_company)
                    except Exception as e:
                        print(e)
                        time.sleep(300)
                        url_api = "https://tmproxy.com/api/proxy/get-new-proxy"
                        data_api = {
                            "api_key": "0741366b7d66deb86cfb0662382f3cd3",
                            "id_location": 0,
                        }

                        post_api = requests.post(url_api,json=data_api)
                        post_api_json = json.loads(post_api.text)
                        print(post_api_json)
                        proxy_https = post_api_json["data"]["https"]
                        hanoi = defaultdict(lambda: defaultdict(dict))   
                        continue
                    page+=1
                hanoi[title_phuong][title_quan] = list_companies

with open('khanh.json', 'w') as file:
    # Convert the dictionary to a JSON-compatible format
    json_data = json.dumps(hanoi)

    # Write the JSON data to the file
    file.write(json_data)



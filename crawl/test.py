import requests

def get_random_proxy():
    url = "https://www.proxy-list.download/api/v1/get?type=http"
    try:
        response = requests.get(url)
        proxies = response.text.strip().split("\r\n")
        return proxies[0] if proxies else None
    except requests.exceptions.RequestException:
        return None

proxy = get_random_proxy()
if proxy:
    print(requests.get('http://example.com').text)    
else:
    print("Không thể lấy proxy.")

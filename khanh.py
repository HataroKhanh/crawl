import requests
import json

# Định nghĩa thông tin yêu cầu
url = "https://tmproxy.com/api/proxy//get-new-proxy"
data = {
    "api_key": "12283e0e42251f81650f99f1795c4f20",
    "sign": "string",
    "id_location": 123
}

# Gửi yêu cầu POST
response = requests.post(url, json=data)

# Kiểm tra mã trạng thái
if response.status_code == 200:
    # Lấy dữ liệu JSON từ phản hồi
    data = json.loads(response.text)
    
    # Truy cập các trường trong phản hồi
    print("Code:", data["code"])
    print("Message:", data["message"])
    print("IP Allow:", data["data"]["ip_allow"])
    print("Location Name:", data["data"]["location_name"])
    print("SOCKS5:", data["data"]["socks5"])
    print("HTTPS:", data["data"]["https"])
    print("Timeout:", data["data"]["timeout"])
    print("Next Request:", data["data"]["next_request"])
    print("Expired At:", data["data"]["expired_at"])
else:
    print("Lỗi:", response.status_code, response.text)

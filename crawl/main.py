import requests
import time
urls = [
    'https://xuongmocdct.okmedia.vn/rem-cau-vong-giai-phap-tuyet-voi-cho-khong-gian-song-hien-dai.html',
    'https://xuongmocdct.okmedia.vn/den-tha-tran-trang-tri-su-lua-chon-hoan-hao-cho-khong-gian-song.html',
    'https://xuongmocdct.okmedia.vn/tu-go-roi-tien-loi-cho-noi-that-gia-dinh.html',
    'https://xuongmocdct.okmedia.vn/lua-chon-tap-dau-giuong-dep-cho-khong-gian-phong-ngu-2024.html',
    'https://xuongmocdct.okmedia.vn/mau-ban-an-phong-cach-hien-dai-xu-huong-2024.html',
    'https://xuongmocdct.okmedia.vn/toi-uu-cho-khong-gian-song-cua-ban-voi-do-go-roi.html',
    'https://xuongmocdct.okmedia.vn/thiet-ke-noi-that-duong-dai-xu-huong-hien-dai-va-sang-trong.html',
    'https://xuongmocdct.okmedia.vn/chat-lieu-go-melamine-va-cac-ung-dung-trong-noi-that.html',
    'https://xuongmocdct.okmedia.vn/xu-huong-thiet-ke-ban-an-nam-2024.html',
    'https://xuongmocdct.okmedia.vn/huong-dan-chon-kieu-ghe-sofa-dep-cho-khong-gian-cua-ban.html',
    'https://xuongmocdct.okmedia.vn/ban-tra-may-dep-don-gian-mem-mai-nhung-doc-dao-cuon-hut.html',
    'https://xuongmocdct.okmedia.vn/tu-quan-ao-go-thong.html',
    'https://xuongmocdct.okmedia.vn/dia-chi-mua-ban-tra-o-ha-noi-uy-tin-tai-ha-noi-gia-tot.html',
    'https://xuongmocdct.okmedia.vn/thiet-ke-noi-that-phong-bep-nha-ong-hien-dai-dan-dau-xu-huong.html',
    'https://xuongmocdct.okmedia.vn/tong-hop-10-y-tuong-thiet-ke-noi-that-phong-bep-dep-hien-dai-chi-phi-re-nhat-2024.html',
    'https://xuongmocdct.okmedia.vn/bi-quyet-thiet-ke-phong-ngu-cho-2-be-gai-dep-cuc-tiet-kiem-chi-phi.html',
    'https://xuongmocdct.okmedia.vn/bat-mi-cach-lua-chon-khong-gian-noi-that-phong-bep-nha-ban.html',
    'https://xuongmocdct.okmedia.vn/noi-that-phong-bep-mini-thiet-ke-sao-cho-dep-va-toi-uu-hoa-dien-tich.html',
    'https://xuongmocdct.okmedia.vn/cach-chon-son-noi-that-phong-ngu-xu-huong-nam-2024.html',
    'https://xuongmocdct.okmedia.vn/goc-chia-se-cach-lam-ban-tra-may-don-gian-tai-nha.html',
    'https://xuongmocdct.okmedia.vn/huong-dan-su-dung-ban-tra-dien-trung-quoc-mot-cach-don-gian-nhat.html',
    'https://xuongmocdct.okmedia.vn/go-soi-co-tot-khong-so-sanh-go-soi-voi-go-xoan-dao.html',
    'https://xuongmocdct.okmedia.vn/gia-tu-bep-cap-nhat-moi-nhat-nam-2023.html',
    'https://xuongmocdct.okmedia.vn/di-tim-loi-giai-cho-cau-hoi-nen-mua-sofa-dep-o-dau.html',
    'https://xuongmocdct.okmedia.vn/diem-danh-nhung-chat-lieu-sofa-ben-dep-duoc-nhieu-nguoi-lua-chon.html',
    'https://xuongmocdct.okmedia.vn/top-5-don-vi-thiet-ke-thi-cong-noi-that-uy-tin-tai-ha-noi.html'
]
for i in urls:
    res = requests.get(i)
    if res.status_code != 200:
        print(res.url)
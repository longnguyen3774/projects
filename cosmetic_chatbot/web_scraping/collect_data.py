import requests
from bs4 import BeautifulSoup
import time
import json

# Đọc danh sách URL
with open("my_pham_hrefs.txt", "r", encoding="utf-8") as f:
    urls = [line.strip() for line in f if line.strip()]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36"
}

products = []

for idx, url in enumerate(urls, 1):
    try:
        print(f"[{idx}] Đang xử lý: {url}")
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        # Tên sản phẩm
        title = soup.find("h1").get_text(strip=True) if soup.find("h1") else ""

        # Giá
        price_tag = soup.select_one("div.box-price b")
        price = price_tag.get_text(strip=True) if price_tag else ""
        price = int(price[:-1].replace('.', ''))

        # Thông tin sản phẩm
        content_div = soup.find("div", class_="content")
        content = content_div.get_text(separator="\n", strip=True) if content_div else ""

        # Tạo dict sản phẩm
        product = {
            "Tên sản phẩm": title,
            "Giá": price,
            "Thông tin sản phẩm": content
        }

        # Phân tích ul.des-infor
        des_ul = soup.find("ul", class_="des-infor")
        if des_ul:
            for li in des_ul.find_all("li"):
                key_tag = li.find("b")
                value_tag = li.find("div", class_="des-infor-content")

                if key_tag and value_tag:
                    key = key_tag.get_text(strip=True)

                    # Nếu value_tag chứa nhiều <li>, nối lại bằng \n
                    li_items = value_tag.find_all("li")
                    if li_items:
                        value = "\n".join([li.get_text(strip=True) for li in li_items])
                    else:
                        value = value_tag.get_text(separator="\n", strip=True)

                    product[key] = value

        product['URL'] = url

        products.append(product)

    except Exception as e:
        print(f"[Lỗi] {url} - {e}")

# Ghi toàn bộ kết quả vào file JSON
# with open("my_pham.json", "w", encoding="utf-8") as f:
#     json.dump(products, f, ensure_ascii=False, indent=2)

print("✅ Đã lưu thông tin vào my_pham.json")

import requests
import pandas as pd
from bs4 import BeautifulSoup
from itertools import combinations
import json

# Đọc file CSV chứa danh sách link, không có header
df_links = pd.read_csv("course_links.csv", header=None, names=["url"])

# Chuyển thành list
links = df_links["url"].tolist()

courses = []

for url in links[:1000]:
    print(f"Đang xử lý: {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Tìm instructor links
        instructors = soup.find_all("a", attrs={
            "data-click-key": "unified_description_page.consumer_course_page.click.hero_instructor"
        })

        names = list({a.get_text(strip=True) for a in instructors if a.get_text(strip=True)})
        instructors_list = list({a["href"].replace("/instructor/", "") for a in instructors})

        # Lấy tên khóa học
        course_name = soup.find("h1")
        course_name = course_name.get_text(strip=True) if course_name else ""

        # Lấy nội dung mô tả khóa học
        content_div = soup.find("div", class_="content")
        course_content = content_div.get_text(strip=True) if content_div else ""

        # Lưu thông tin khóa học
        courses.append({
            "url": url,
            "name": course_name,
            "content": course_content,
            "instructors": instructors_list
        })

    except Exception as e:
        print(f"Lỗi khi xử lý {url}: {e}")

# Lưu thành file JSON
with open("courses.json", "w", encoding="utf-8") as f:
    json.dump(courses, f, ensure_ascii=False, indent=2)

print("✅ Đã lưu dữ liệu vào courses.json")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import time

# Cấu hình driver (thay bằng đường dẫn tới ChromeDriver của bạn nếu cần)
driver = webdriver.Chrome()

url = "https://www.nhathuocankhang.com/my-pham"
driver.get(url)

wait = WebDriverWait(driver, 10)

# Click nút 'Xem thêm'
time.sleep(100)

# Lấy tất cả thẻ li có class "item oneUnit"
items = driver.find_elements(By.CSS_SELECTOR, "li.item.oneUnit")

hrefs = []
for item in items:
    try:
        a_tag = item.find_element(By.TAG_NAME, "a")
        href = a_tag.get_attribute("href")
        if href:
            hrefs.append(href)
    except NoSuchElementException:
        continue

# Lưu vào file
# with open("my_pham_hrefs.txt", "w", encoding="utf-8") as f:
#     for link in hrefs:
#         f.write(link + "\n")

print(f"Đã lưu {len(hrefs)} đường dẫn vào my_pham_hrefs.txt")

# Đóng trình duyệt
driver.quit()

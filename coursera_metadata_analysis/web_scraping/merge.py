import glob
import csv

# B1: Tìm tất cả file CSV theo pattern *_courses.csv
csv_files = glob.glob("*_courses.csv")

all_links = set()

# B2: Đọc lần lượt từng file
for file in csv_files:
    with open(file, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:  # tránh dòng rỗng
                link = row[0].strip()
                if link.startswith("https://www.coursera.org/learn"):
                    all_links.add(link)

print(f"🔎 Đã thu thập {len(all_links)} link duy nhất từ {len(csv_files)} file.")

# B3: Ghi vào file course_links.csv
with open("course_links.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    for link in sorted(all_links):
        writer.writerow([link])

print("✅ Đã lưu kết quả vào course_links.csv")

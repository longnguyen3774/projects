import pandas as pd

# Đọc file CSV
df = pd.read_csv("instructor_edges.csv")

# Giữ lại 2 cột instructor_1 và instructor_2, bỏ course_url
df_filtered = df[["instructor_1", "instructor_2"]]

# Xuất ra file mới nếu cần
df_filtered.to_csv("instructor_edges_filtered.csv", index=False)

print(df_filtered.head())
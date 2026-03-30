import json
import pandas as pd
import itertools
import networkx as nx

# ====== B1: Đọc dữ liệu courses.json ======
with open("courses.json", "r", encoding="utf-8") as f:
    courses = json.load(f)

# ====== B2: Tổng hợp instructors và gán ID ======
all_instructors = sorted({inst for c in courses for inst in c["instructors"]})
instructor2id = {name: idx for idx, name in enumerate(all_instructors)}

# Lưu instructors.json
instructors_data = [{"id": idx, "name": name} for name, idx in instructor2id.items()]
with open("instructors.json", "w", encoding="utf-8") as f:
    json.dump(instructors_data, f, ensure_ascii=False, indent=2)

# ====== B3: Thay thế instructors trong courses.json bằng ID ======
for c in courses:
    c["instructors"] = [instructor2id[name] for name in c["instructors"]]

with open("courses_with_ids.json", "w", encoding="utf-8") as f:
    json.dump(courses, f, ensure_ascii=False, indent=2)

# ====== B4: Xây dựng ma trận hợp tác ======
n = len(all_instructors)
matrix = [[0]*n for _ in range(n)]

for c in courses:
    ids = c["instructors"]
    for i, j in itertools.combinations(ids, 2):
        matrix[i][j] += 1
        matrix[j][i] += 1  # vì đồ thị vô hướng

# Lưu ma trận ra CSV
df_matrix = pd.DataFrame(matrix, index=range(n), columns=range(n))
df_matrix.to_csv("cooperation_matrix.csv", encoding="utf-8-sig")

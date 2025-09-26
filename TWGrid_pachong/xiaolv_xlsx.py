import pandas as pd
import csv

# 读取 CSV 文件
csv_data = {}
with open('output.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # 跳过表头
    for row in reader:
        csv_data[row[0]] = row[1]  # 名称作为键，效率作为值

# 读取 Excel 文件
df = pd.read_excel('发电厂效率.xlsx')  # 替换 'your_file.xlsx' 为你的实际文件名

# 定义一个函数来找到最佳匹配
def find_best_match(name, csv_keys):
    matches = [key for key in csv_keys if key in name]
    if matches:
        return max(matches, key=len)  # 返回最长的匹配
    return None

# 处理每一行
for index, row in df.iterrows():
    name = row['名称']
    if pd.notna(name):
        best_match = find_best_match(name, csv_data.keys())
        if best_match:
            df.at[index, '发电效率'] = csv_data[best_match]

# 保存更新后的 Excel 文件
df.to_excel('updated_file.xlsx', index=False)

print("Excel 文件已更新。")

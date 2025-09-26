import json
import csv
from collections import defaultdict
import requests

# 从网页获取 JSON 数据
url = "https://service.taipower.com.tw/data/opendata/apply/file/d006001/001.json"
response = requests.get(url)
response.encoding = 'utf-8-sig'  # 修改这里来处理 UTF-8 BOM
data = json.loads(response.text)

# 创建一个字典来存储聚合数据
aggregated_data = defaultdict(list)

# 遍历 aaData 中的每一项
for item in data['aaData']:
    # 获取第二个属性的前两个汉字
    key = item[1][:2]
    # 获取第五个属性（百分比）
    percentage = item[4]

    # 如果百分比不为空，则添加到对应的列表中
    if percentage and percentage.strip():
        try:
            # 移除百分号并转换为浮点数
            value = float(percentage.rstrip('%'))
            aggregated_data[key].append(value)
        except ValueError:
            # 如果转换失败，跳过这一项
            continue

# 计算平均值
result = []
for key, values in aggregated_data.items():
    if values:  # 确保列表不为空
        avg = sum(values) / len(values)
        result.append([key, f"{avg:.3f}%"])

# 将结果写入 CSV 文件
with open('output.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['名称', '平均值'])  # 写入表头
    writer.writerows(result)

print("CSV 文件已生成。")

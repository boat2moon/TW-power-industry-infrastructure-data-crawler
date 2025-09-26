import pandas as pd

# 读取Excel文件
file_path = 'merged_substations.xlsx'  # 请替换成您的文件路径
df = pd.read_excel(file_path)

# 拆分经纬度
df[['经度', '纬度']] = df['经纬度'].str.strip('[]').str.split(', ', expand=True)
df['经度'] = df['经度'].astype(float)
df['纬度'] = df['纬度'].astype(float)

# 处理空值和转换数字
def process_values(x):
    if pd.isna(x) or x == 'nan':
        return x
    if isinstance(x, str):
        return sum(map(float, x.split(', ')))
    return float(x)

df['输电量'] = df['输电量'].apply(process_values)
df['最大承载额'] = df['最大承载额'].apply(process_values)

# 保存修改后的数据到新的Excel文件
output_file_path = 'processed_excel_file.xlsx'  # 您可以修改保存文件的路径
df.to_excel(output_file_path, index=False)


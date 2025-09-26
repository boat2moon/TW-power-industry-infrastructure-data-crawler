import geojson
import pandas as pd

# 读取 GeoJSON 文件
with open("export_biandian.geojson", "r", encoding='utf-8') as f:
    data = geojson.load(f)

# 提取特征信息
features = data['features']

# 创建 DataFrame 并解析特征
df_list = []
for feature in features:
    properties = feature['properties']
    geometry_type = feature['geometry']['type']

    if geometry_type == 'Polygon':
        # 只保留第一个坐标点
        first_coordinate = feature['geometry']['coordinates'][0][0]
    elif geometry_type == 'MultiPolygon':
        # 只保留第一个多边形中的第一个坐标点
        first_coordinate = feature['geometry']['coordinates'][0][0][0]

    properties['coordinates'] = first_coordinate
    df_list.append(properties)

# 创建 DataFrame，并只保留需要的列
df = pd.DataFrame(df_list, columns=['name', 'voltage', 'coordinates', 'rating'])

# 将 DataFrame 导出为 Excel
df.to_excel("substations_4c.xlsx", index=False)

print("Data successfully exported to substations.xlsx")

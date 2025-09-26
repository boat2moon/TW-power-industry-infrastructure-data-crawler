import json
import pandas as pd

# 读取GeoJSON文件
with open('export_edge.geojson', 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

# 提取数据
features = geojson_data['features']

# 创建一个空的DataFrame来存储数据
data = []

for feature in features:
    properties = feature['properties']
    geometry = feature['geometry']

    # 提取所需的属性
    feature_data = {
        '@id': properties.get('@id'),
        'alt_name': properties.get('alt_name'),
        'cables': properties.get('cables'),
        'layer': properties.get('layer'),
        'name': properties.get('name'),
        'voltage': properties.get('voltage'),
        'first_coordinates': None,
        'last_coordinates': None
    }

    # 处理coordinates列
    if geometry['type'] == 'LineString' and len(geometry['coordinates']) > 0:
        first_coord = geometry['coordinates'][0]
        last_coord = geometry['coordinates'][-1]
        feature_data['first_coordinates'] = first_coord
        feature_data['last_coordinates'] = last_coord

    data.append(feature_data)

# 将数据转换为DataFrame
df = pd.DataFrame(data)

# 将first_coordinates和last_coordinates列转换为字符串
df['first_coordinates'] = df['first_coordinates'].apply(lambda x: json.dumps(x) if x else None)
df['last_coordinates'] = df['last_coordinates'].apply(lambda x: json.dumps(x) if x else None)

# 将DataFrame保存为Excel文件
df.to_excel('output2.xlsx', index=False)

print('GeoJSON文件已成功转换为Excel文件')

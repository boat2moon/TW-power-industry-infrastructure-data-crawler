import pandas as pd
from geopy.geocoders import ArcGIS
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import time
import random
from opencc import OpenCC

# 读取 Excel 文件
df = pd.read_excel('调度人口.xlsx')  # 替换为你的文件名

# 初始化地理编码器
geolocator = ArcGIS()

# 初始化简体到繁体转换器
cc = OpenCC('s2t')

def get_lat_lon(address):
    try:
        # 将地址转换为繁体，并添加 ", 臺灣"
        address_t = cc.convert(address) + ", 臺灣"
        location = geolocator.geocode(address_t, timeout=15)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        print(f"地理编码错误 ({type(e).__name__}): {address}")
        return None, None

# 对每一行进行地理编码
for index, row in df.iterrows():
    if pd.isna(row['位置经度']) or pd.isna(row['位置纬度']):
        print(f"正在处理: {row['名称']}")
        lat, lon = get_lat_lon(row['名称'])
        if lat and lon:
            df.at[index, '位置纬度'] = lat
            df.at[index, '位置经度'] = lon
        # 增加随机延迟，在 1 到 3 秒之间
        time.sleep(random.uniform(1, 3))

# 保存更新后的文件
df.to_excel('updated_locations.xlsx', index=False)
print("已完成地理编码并保存更新后的文件。")

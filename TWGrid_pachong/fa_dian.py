import requests
from bs4 import BeautifulSoup
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import time
import shelve

# 创建用于缓存的shelve对象
with shelve.open('geocode_cache') as cache:
    def get_location(plant_name, geolocator, cache):
        if plant_name in cache:
            return cache[plant_name]
        try:
            location = geolocator.geocode(plant_name + ", Taiwan", timeout=10)
            if location:
                cache[plant_name] = (location.latitude, location.longitude)
            else:
                cache[plant_name] = (None, None)
            return cache[plant_name]
        except (GeocoderTimedOut, GeocoderUnavailable):
            return (None, None)


    def get_address(lat, lon, geolocator, cache):
        cache_key = f"{lat},{lon}"  # 将经纬度转换为字符串键
        if cache_key in cache:
            return cache[cache_key]
        try:
            location = geolocator.reverse((lat, lon), timeout=10)
            if location:
                address = location.address
                cache[cache_key] = address
                return address
            else:
                return None
        except (GeocoderTimedOut, GeocoderUnavailable):
            return None


    # 第1步：获取网页内容
    url = 'https://openinframap.org/stats/area/Taiwan/plants'
    response = requests.get(url)
    response.raise_for_status()  # 检查请求是否成功

    # 第2步：解析HTML内容
    soup = BeautifulSoup(response.content, 'html.parser')

    # 第3步：提取数据
    plant_data = []
    table = soup.find('table')
    headers = [header.text for header in table.find_all('th')]

    # 增加经度、纬度和具体地址的列头
    headers.extend(['Latitude', 'Longitude', 'Address'])

    geolocator = Nominatim(user_agent="power_plant_locator")

    for row in table.find_all('tr')[1:]:
        columns = row.find_all('td')
        plant_info = [col.text.strip() for col in columns]
        plant_name = plant_info[0]  # 假设发电厂名称在第一个列

        # 获取经度和纬度
        lat, lon = get_location(plant_name, geolocator, cache)
        plant_info.extend([lat, lon])

        if lat and lon:
            # 获取具体地址
            address = get_address(lat, lon, geolocator, cache)
            plant_info.append(address)
        else:
            plant_info.append(None)

        plant_data.append(plant_info)

        # 增加延迟，避免频率限制
        time.sleep(1)

    # 第4步：将数据保存到Excel
    df = pd.DataFrame(plant_data, columns=headers)
    df.to_excel('Taiwan_Power_Plants_with_Locations.xlsx', index=False)

    print("数据已写入Taiwan_Power_Plants_with_Locations.xlsx")

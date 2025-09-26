import pandas as pd
import numpy as np


def preprocess_bianyaqi(df):
    # 去除变压名称中的后缀E/S, D/S, S/S, P/S
    df['变压名称'] = df['变压名称'].str.replace(r'[EDS/P]+/[S]+$', '', regex=True)
    return df


def handle_nulls(df):
    # 处理空值字符串为空值当作”nodata“，数值空值当成0处理
    str_cols = df.select_dtypes(include=['object']).columns
    num_cols = df.select_dtypes(include=[np.number]).columns
    df[str_cols] = df[str_cols].fillna('nodata')
    df[num_cols] = df[num_cols].fillna(0)
    return df


# 读取Excel文件
substations_df = pd.read_excel('substations_4c.xlsx')
bianyaqi_df = pd.read_excel('bianyaqi.xlsx')

# 处理空值
substations_df = handle_nulls(substations_df)
bianyaqi_df = handle_nulls(bianyaqi_df)

# 预处理bianyaqi文件
bianyaqi_df = preprocess_bianyaqi(bianyaqi_df)

# 创建一个新的列用于记录合并的变压名称
substations_df['整合项'] = np.nan

# 确保所有列为字符串类型
substations_df = substations_df.astype({col: str for col in substations_df.columns})
bianyaqi_df = bianyaqi_df.astype({col: str for col in bianyaqi_df.columns})

# 遍历bianyaqi_df中的每一行
for _, byq_row in bianyaqi_df.iterrows():
    matched = False
    byq_name = byq_row['变压名称']

    for idx, sub_row in substations_df.iterrows():
        if byq_name in sub_row['变所名称']:
            matched = True

            # 更新整合项
            if not pd.isna(sub_row['整合项']):
                substations_df.at[idx, '整合项'] += f", {byq_row['变压名称']}"
            else:
                substations_df.at[idx, '整合项'] = byq_row['变压名称']

            # 合并数据
            for col in bianyaqi_df.columns[1:]:
                if col not in substations_df.columns:
                    substations_df[col] = ''

                existing_val = substations_df.at[idx, col] if col in substations_df.columns else ''
                new_val = byq_row[col]

                try:
                    if existing_val == '' or existing_val == 'nodata':
                        substations_df.at[idx, col] = new_val
                    elif pd.api.types.is_number(existing_val) or pd.api.types.is_number(new_val):
                        # 数值列相加
                        substations_df.at[idx, col] = float(existing_val) + float(new_val)
                    else:
                        # 文字列拼接并去重
                        existing_data = existing_val.split(", ") if existing_val and existing_val != 'nodata' else []
                        new_data = new_val.split(", ") if new_val and new_val != 'nodata' else []
                        unique_data = list(set(existing_data + new_data))
                        substations_df.at[idx, col] = ", ".join(unique_data)
                except ValueError:
                    substations_df.at[idx, col] = new_val if existing_val == '' or pd.isna(
                        existing_val) else existing_val

# 保存合并后的结果
substations_df.to_excel('merged_substations.xlsx', index=False)

print("数据整合完成，结果保存在 'merged_substations.xlsx'")

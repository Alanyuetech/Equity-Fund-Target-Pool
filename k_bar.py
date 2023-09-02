import pandas as pd  
import numpy as np
import os
import time
# 设定你的文件夹路径
# system_folder_path = '/home/ubuntu/data/Equity-Fund-Target-Pool/'   #服务器端
system_folder_path = ''   # 本地端
folder_path = 'etf_data'

# 获取文件夹下所有文件名
all_files = os.listdir(system_folder_path+folder_path)

# 过滤出所有CSV文件
etf_csv_files = [f for f in all_files if f.startswith('etf_data') and f.endswith('.csv')]
etf_csv_files.sort()
for etf_data_n in etf_csv_files[:]:
    data_df = pd.read_csv(system_folder_path+folder_path+'/'+etf_data_n)
    data_df['real_body'] = abs(data_df['open']-data_df['close'])
    data_df['high_low'] = data_df['high'] - data_df['low']
    data_df['lower_shadow'] = np.nan
    data_df['upper_shadow'] = np.nan
    data_df['bearish_bullish'] = np.nan
    for index,row in data_df[:].iterrows():
        if index % 1000 == 0:
            print(etf_data_n,index)
        if row['open']<row['close']:
            data_df.loc[index,'lower_shadow'] = row['open'] - row['low']
            data_df.loc[index,'upper_shadow'] = row['high'] - row['close']
            data_df.loc[index,'bearish_bullish'] = 'bullish'
        elif row['open']>row['close']:
            data_df.loc[index,'lower_shadow'] = row['close'] - row['low']
            data_df.loc[index,'upper_shadow'] = row['high'] - row['open']
            data_df.loc[index,'bearish_bullish'] = 'bearish'
        else:
            pass
    data_df['real_body_percent'] = (data_df['real_body']/data_df['high_low'])*100
    data_df['lower_shadow_percent'] = (data_df['lower_shadow']/data_df['high_low'])*100
    data_df['upper_shadow_percent'] = (data_df['upper_shadow']/data_df['high_low'])*100

    save_folder_path = 'k_bar_etf_data'  
    if not os.path.exists(system_folder_path+save_folder_path):  
        os.makedirs(system_folder_path+save_folder_path)  
    data_df.to_csv(system_folder_path+'k_bar_etf_data/'+'k_bar_'+etf_data_n)
    
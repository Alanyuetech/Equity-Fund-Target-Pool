
import akshare as ak
import pandas as pd
import time 
from matplotlib import pyplot as plt 
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta
from openpyxl import load_workbook
import xlsxwriter
import openpyxl
from openpyxl.styles import PatternFill,Font,Alignment


######################logging相关##########################
import os
import sys
# 获取当前文件的父目录的父目录
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 将父目录的父目录添加到 sys.path
sys.path.append(parent_dir)
# 现在应该可以正确导入了
from comm_logging.common_logging import Common_logging
logger =  Common_logging('no_data_etf').get_logger()
######################logging相关##########################

def getLastWeekDay(day=datetime.datetime.now()):
    now=day
    if now.isoweekday()==1:
      dayStep=3
    else:
      dayStep=1
    lastWorkDay = now - datetime.timedelta(days=dayStep)
    return lastWorkDay
date_work=getLastWeekDay().strftime('%Y%m%d')
now_day = datetime.datetime.now().strftime('%Y%m%d')

#加载etf_info,去除第一列index
etf_info = pd.read_csv('etf_data/etf_info.csv')
#循环获取所有代码的历史数据，将没有获取到历史数据的代码添加到新的dataframe中,新的dataframe的列名和etf_info相同
no_data_etf =  pd.DataFrame(columns=list(etf_info.keys())[:3] + ['comment'])
etf_data = pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume'])
for index,row in etf_info[:].iterrows():
  # time.sleep(4)
  try:
    etf_data_b = ak.stock_us_daily(symbol=row['Symbol'], adjust="")
    etf_data_b['symbol'] = row['Symbol']
    if (etf_data_b.empty)|(len(etf_data_b)==0)|(etf_data_b is None):
        row['comment']='no data'
        no_data_etf = no_data_etf.append(row[no_data_etf.columns],ignore_index=True)
        logger.info("index: %s Symbol: %s comment: %s", index, row['Symbol'], row['comment'])
    else:
      etf_data = pd.concat([etf_data,etf_data_b],axis=0)
      print(index,row['Symbol'],'etf_data:',len(etf_data),'etf_data_b:',len(etf_data_b))
    #index 每200 执行一次 to_csv操作
    if ((index%200==0)&(index!=0))|(index==len(etf_info)-1):     
    #   etf_data.to_csv('etf_data/etf_data{}.csv'.format(index), index=False)
    #   print('etf_data.csv:',len(etf_data))
      etf_data = pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume'])
  except Exception as e:  # 捕获所有异常
      row['comment'] = str(e)  # 将异常转换为字符串
      no_data_etf = no_data_etf.append(row[no_data_etf.columns],ignore_index=True)
      logger.info("index: %s Symbol: %s comment: %s", index, row['Symbol'], row['comment'])

no_data_etf.to_csv('etf_data/no_data_etf.csv', index=False)
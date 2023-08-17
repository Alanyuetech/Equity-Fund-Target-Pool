
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


stock_list = ak.get_us_stock_name()  #股票代码可通过 ak.get_us_stock_name() 函数返回值

us_stock =  ak.stock_us_spot_em()   #实时行情数据-东财
# stock_data_b = ak.stock_us_hist(symbol='105.QQQ', start_date="20110101", end_date="22220101", adjust="")  #这里使用不复权的数据

#依据us_stock名单，获取数据，通过stock_us_hist获取历史数据
stock_data = ak.stock_us_hist(symbol=us_stock['代码'].tolist(), start_date="20110101", end_date=now_day, adjust="")  #这里使用不复权的数据
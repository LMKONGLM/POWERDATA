#!usr/bin/env python
# -*-coding: utf-8 -*-
import sys
import os
import codecs
sys.path.append('D:\Python27\Lib\site-packages')
from numpy import *
import func
import math
from scipy import optimize
import numpy as np
import pandas as pd
os.getcwd()
os.chdir(r'd:\data\python')
FilenameR = 'rain.xlsx'
FilenameW = 'rain.txt'
#清空日志
log='log.csv'
rain_msg='rain_msg.txt'
csvfile=open(log,'w')
csvfile.write('')
csvfile.close
txtfile=open(rain_msg,'w')
#天气预报
data=pd.read_excel(io=FilenameR,sheet_name=0)
data=data.sort_values(by=['区局'],ascending=True)
depa=data.drop_duplicates(['区局'])
func.writedf(log,depa,'去重区局列表')
data_group_rain=data['降雨量'].groupby(data['区局']).mean()
data_group_cloud=data['风速'].groupby(data['区局']).mean()
data_group_wheather=pd.DataFrame({'降雨量':data_group_rain,'风速':data_group_cloud})
data_group_wheather.reset_index(inplace=True)
func.writedf(log,data_group_wheather,'各区局天气预报')
#排名前十历史降雨量配电房
data=pd.read_excel(io=FilenameR,sheet_name=1)
data=data.sort_values(by=['区局','未来1小时降雨量'],ascending=[True,False])
#data_group=data.groupby(by='区局').agg({'未来12小时降雨量':np.average})
data_group_history=data.groupby(by='区局').head(10)
func.writedf(log,data_group_history,'排名前十历史降雨量配电房')
#排名前十预测降雨量配电房
data=pd.read_excel(io=FilenameR,sheet_name=2)
data=data.sort_values(by=['区局','未来1小时降雨量'],ascending=[True,False])
data_group_pred=data.groupby(by='区局').head(10)
func.writedf(log,data_group_pred,'排名前十预测降雨量配电房')
#排名前三涝区配电房（不在历史前十里）
data=pd.read_excel(io=FilenameR,sheet_name=3)
data=data.sort_values(by=['区局','未来1小时降雨量'],ascending=[True,False])
data_group_zone=data.groupby(by='区局').head(10)
data_group_zone=data_group_zone[~data_group_zone['配电站房'].isin(data_group_history['配电站房'])]
data_group_zone=data_group_zone.groupby(by='区局').head(3)
func.writedf(log,data_group_zone,'排名前三涝区配电房')
#编辑短信
for depa in depa['区局']:
    rain_text=''
    #1、天气预报
    data_depa_wheather=data_group_wheather[data_group_wheather['区局']==depa]
    
    rain_text="【电力气象监测预警】["
    rain_text=rain_text+depa
    rain_text=rain_text+"水浸隐患配电房降雨监测09：00]一、天气预报：未来3小时降雨量为"
    rain_text=rain_text+str(data_depa_wheather.iloc[0,1])[:4]+"mm,"
    rain_text=rain_text+"未来3小时平均风速为"
    rain_text=rain_text+str(data_depa_wheather.iloc[0,2])[:4]+"m/s。"
    #2历史降雨
    data_depa_history=data_group_history[data_group_history['区局']==depa]
    rain_text=rain_text+"二、历史降雨情况：水浸隐患配电房中历史1小时累计降雨量前十为"
    rain_text=rain_text+func.msg(data_depa_history,1,2)
    rain_text=rain_text+'。'
    #3、涝区降雨
    data_depa_zone=data_group_zone[data_group_zone['区局']==depa]
    if data_depa_zone.empty !=True:
        rain_text=rain_text+"此外，"
        rain_text=rain_text+func.msg(data_depa_zone,1,2)
        rain_text=rain_text+"处于城市内涝区域，历史1小时降雨量较大。"
    #4、预测降雨
    data_depa_pred=data_group_pred[data_group_pred['区局']==depa]
    rain_text=rain_text+"三、预测降雨情况：水浸隐患配电房中未来1小时累计降雨量前十为"
    rain_text=rain_text+func.msg(data_depa_pred,1,2)
    rain_text=rain_text+'。'
    #4存储短信
    txtfile.write(rain_text)
    txtfile.write('\n')
txtfile.close
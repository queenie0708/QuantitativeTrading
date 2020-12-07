# coding=utf-8
import datetime
import tushare as ts
import csv
import json
import pandas as pd
from openpyxl import Workbook
from openpyxl import load_workbook
import glob
import os

auth = open('./auth.json')
info = json.load(auth)
token = info['token']
ts.set_token(token)
pro = ts.pro_api()

today = datetime.date.today().__str__().replace("-", "")

#df = pro.concept_detail(id='TS290', fields='ts_code,name')
def getConcepts():
    df = pro.concept()
#df = pro.concept_detail(ts_code = '300296.SZ')
#df.to_excel('./all_concepts.xlsx') 
    df.to_csv('./all_concepts.csv',encoding='gb2312')

def getConceptContents():
    codes = []
    with open('./all_concepts.csv','r') as myFile:
            lines=csv.reader(myFile)
            for line in lines: 
                codes.append(line[1])
    for i in range (1,len(codes)):
        df = pro.concept_detail(id=codes[i], fields='ts_code,name')
        df.to_excel('concept'+str(i)+contents.xlsx)

def getAlldata():
    df = pro.daily_basic(trade_date='20201204', fields='ts_code,total_mv,close')
    df.to_excel('mv_price.xlsx')

def getStockMV():
    mv=pd.DataFrame(pd.read_excel('mv_price.xlsx'))
    for i in range(1,360):
        stock=pd.DataFrame(pd.read_excel('concept'+str(i)+'contens.xlsx'))
        new = stock.merge(mv,how='inner',on='ts_code')
        new.to_excel('concept'+str(i)+'.xlsx')

def processConcept():
    for i in range(1,360):
        df = pd.read_excel('concept'+str(i)+'.xlsx')
        sum_mv =  df['total_mv'].sum()
        price_pct=df['total_mv']/sum_mv*df['close']
        df['price_pct'] = price_pct
        df.to_excel('concept'+str(i)+'.xlsx')

def getConceptIndex():
    concept_index = []
    for i in range(1,360):
        df = pd.read_excel('concept'+str(i)+'.xlsx')
        sum_share = df['price_pct'].sum()
        concept_index.append(sum_share)
        concept = pd.read_excel('all_concepts.xlsx')
    concept['concept_index'] = concept_index
    concept.to_excel('all_concepts.xlsx')


def _main():
    getConceptIndex()

if __name__ == '__main__':
    _main()

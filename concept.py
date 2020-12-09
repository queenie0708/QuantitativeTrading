# coding=utf-8
import datetime
import tushare as ts
import csv
import json
import pandas as pd

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
    df.to_csv('./all_concepts.csv',encoding='utf-8')

def getAllIndustryContents():
    df = pd.read_csv('all_industries.csv')
    index_code = df['index_code']
    for i in range (1,len(index_code)):
        print(i)
        df = pro.index_member(index_code=index_code[i], fields='con_code,con_name')
        df.to_excel('industry'+str(i)+'contents.xls')


def getConceptContents():
    codes = []
    with open('./all_concepts.csv','r') as myFile:
            lines=csv.reader(myFile)
            for line in lines: 
                codes.append(line[1])
    for i in range (1,360):
        print(i)
        df = pro.concept_detail(id=codes[i], fields='ts_code,name')
        df.to_excel('concept'+str(i)+'contents.xlsx')

def getYearlyData():
    with pd.ExcelWriter('mv_price.xlsx') as writer:
        for i in range(20200101,int(today)): 
            name = 'df_' + str(i)
            name = pro.daily_basic(trade_date=i, fields='ts_code,total_mv,close')
            if len(name['total_mv']) >2 :
                name.to_excel(writer, sheet_name=str(i))
        writer.save()

def getIndexData():
    df = pro.index_daily(ts_code='000001.SH', start_date='20200102', end_date='20201207', fields='ts_code,trade_date,close')
    df.to_excel('index_close.xlsx')

def getStockMV():
    xl = pd.read_excel('index_close.xlsx')
    date = xl['trade_date']
    choosed = [25,110,230,97,82,22,280,79,126,87,313,207,219,51,293,114,264,312,237,152,259,141,189,59,145]
    for j in choosed:
        print('concept'+str(j)+'contents.xlsx')
        with pd.ExcelWriter('concept'+str(j)+'contents.xlsx') as writer:
            for i in range(len(date)):
                print(date[i])
                mv=pd.DataFrame(pd.read_excel('mv_price.xls',str(date[i])))
                stock = pd.read_excel(writer)
                new = stock.merge(mv,how='inner',on='ts_code',suffixes=('',date[i]))
                new.to_excel(writer,index=False)
                writer.save()

def processConcept():
    xl = pd.read_excel('index_close.xlsx')
    date = xl['trade_date']
    with pd.ExcelWriter('concept14contents.xlsx') as writer:
        df = pd.read_excel(writer)
  #  df.var().to_excel('conceptvar.xls')
        for i in range(len(date)):
            print(date[i])
            sum_mv =  df['total_mv'+str(date[i])].sum()
            price_pct=df['total_mv'+str(date[i])]/sum_mv*df['close'+str(date[i])]
            df['price_pct'+str(date[i])] = price_pct
            df.to_excel(writer)
        writer.save()


def getConceptIndex():
    concept_index = []
    for i in range(1,360):
        df = pd.read_excel('concept'+str(i)+'.xlsx','',)
        sum_share = df['price_pct'].sum()
        concept_index.append(sum_share)
        concept = pd.read_excel('all_concepts.xlsx')
    concept['concept_index'] = concept_index
    concept.to_excel('all_concepts.xlsx')

def getConceptAmount():
    concept_amount = []
    for i in range(1,360):
        df = pd.read_excel('concept'+str(i)+'.xlsx')
        sum_amount = df['amount'].sum()
        concept_amount.append(sum_amount)
        concept = pd.read_excel('all_concepts.xlsx')
    concept['concept_amount'] = concept_amount
    concept.to_excel('all_concepts.xlsx')

def _main():
    getStockMV()

if __name__ == '__main__':
    _main()

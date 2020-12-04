# coding=utf-8
from datetime import datetime, timedelta
import tushare as ts
import csv
import json
from sqlalchemy import create_engine 
import pymysql

auth = open('./auth.json')
info = json.load(auth)
token = info['token']
ts.set_token(token)
pro = ts.pro_api()


#df = pro.concept_detail(id='TS290', fields='ts_code,name')
def getConcepts():
    df = pro.concept()
#df = pro.concept_detail(ts_code = '300296.SZ')
#df.to_excel('./all_concepts.xlsx') 
    df.to_csv('./all_concepts.csv')

def getConceptContents():
    codes = []
    with open('./all_concepts.csv','r') as myFile:
            lines=csv.reader(myFile)
            for line in lines: 
                codes.append(line[1])
    for i in range (1,len(codes)):
        df = pro.concept_detail(id=codes[i], fields='ts_code,name')
        df.to_excel('concept'+str(i)+contents.xlsx)

def _main():
    getConceptContents()

if __name__ == '__main__':
    _main()

import datetime
import argparse
import pandas_datareader.data as web
import matplotlib.pyplot as plt

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--stock", required=True, help='which stock to query e.g 300296.SZ')
    parser.add_argument("-f","--start_time",required=True, help='from time format 2017,1,1')
    parser.add_argument("-t","--end_time",required=True, help='to time format 2020,12,3')
    parser.add_argument('-v', "--verbose", action='store_true',  default=False,  help='output verbose information if specified')
    return parser.parse_args()

def StrToDate(s):
    date = s.split(',')
    return date

def _main():
    try:
        global verbose_flag
        args = parse_args()
        if args.verbose:
            verbose_flag = True
        success = True
       
    except Exception as e:
        print("e=%s" % e)

    if success:
        start = StrToDate(args.start_time)
        end = StrToDate(args.end_time)
        start_time = datetime.datetime(int(start[0]),int(start[1]),int(start[2]))
        end_time = datetime.datetime(int(end[0]),int(end[1]),int(end[2]))
        stock = web.DataReader(args.stock, "yahoo", start_time, end_time)
        change = stock.Close.diff()
        stock['Change'] = change
        format = lambda x: '%.2f' % x
        stock = stock.applymap(format)
        print(stock)

if __name__ == '__main__':
    _main()



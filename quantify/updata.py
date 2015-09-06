# -*- coding: utf-8 -*-

import chardet
from quantify import db,dataApi
import pandas as pd
from pandas import DataFrame
import time
import traceback

db.create_engine(user='root', password='', database='quant', host='127.0.0.1', port=3306)
#导入所有代码进数据库
def input_list_data(buf):
    #buf='SH' or buf='SZ'
    
    f=open('../data/%s.SNT'%buf,'r')
    str=f.readlines()
    for index,i in enumerate(str):
        if index>1:
            line=i.strip().split('\t')
        
            try:
                code_name=line[1].decode('GB2312').encode('utf-8')
                code=line[0]+'.%s'%buf
                n = db.update('insert into code_list(code, name , market) values(?, ? ,?)',code , code_name , buf)
                print n
            except Exception as e:
                print e
    
        #print chardet.detect(code_name)查看编码
    f.close()

def input_stock_data():
    res=db.select('select * from code_list')
    #string_list=[]
    for i in res:
        stock_code=i[u'code'].decode('utf-8')
        stock_num=stock_code.split('.')
        get_sd_csv('20010101','20150814',stock_num[0],'../stock_data/%s.csv'%stock_num[0])
        print stock_num[0]
        

def get_sd_csv(start,end,stock_num,filename):
    client = dataApi.Client()
    url='/api/market/getMktEqud.csv?field=&beginDate=%s&endDate=%s&secID=&ticker=%s&tradeDate='%(start,end,stock_num)
    code, result = client.getData(url)
    if(code==200):
        file_object = open(filename, 'w')
        file_object.write(result)
        file_object.close( )
        print 'ok'
    else:
        print code
        print result

def input_daily_data():
    res=db.select('select * from code_list')
    #string_list=[]
    for i in res:
        stock_code=i[u'code'].decode('utf-8')
        stock_num=stock_code.split('.')
        stock_data=open_csv('../stock_data/%s.csv'%stock_num[0])
        try:
            for i in range(stock_data.shape[0]):
                only_key='%s+%s'%(stock_data.iloc[i]['secID'],stock_data.iloc[i]['tradeDate'])
                charset=chardet.detect(stock_data.iloc[i]['secShortName'])
                print charset,stock_data.iloc[i]['secShortName'].decode('GB2312')
                n = db.update('insert into daily_data(secID, ticker , secShortName , exchangeCD , tradeDate , preClosePrice , actPreClosePrice ,openPrice , highestPrice , lowestPrice , closePrice , turnoverVol , turnoverValue , dealAmount , turnoverRate , accumAdjFactor ,negMarketValue , marketValue , PE ,PE1, PB, only_key) values(?, ? ,? ,? ,? ,? ,? ,? ,? ,?, ?, ? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? )',stock_data.iloc[i]['secID'],  str(stock_data.iloc[i]['ticker']) ,stock_data.iloc[i]['secShortName'].decode('GB2312').encode('utf-8'), stock_data.iloc[i]['exchangeCD'] , stock_data.iloc[i]['tradeDate'] , float(stock_data.iloc[i]['preClosePrice']) , float(stock_data.iloc[i]['actPreClosePrice']) ,float(stock_data.iloc[i]['openPrice']) , float(stock_data.iloc[i]['highestPrice']) , float(stock_data.iloc[i]['lowestPrice']) , float(stock_data.iloc[i]['closePrice']) , int(stock_data.iloc[i]['turnoverVol']) , float(stock_data.iloc[i]['turnoverValue']) , int(stock_data.iloc[i]['dealAmount']) , float(stock_data.iloc[i]['turnoverRate']) , float(stock_data.iloc[i]['accumAdjFactor']) , float(stock_data.iloc[i]['negMarketValue']) , float(stock_data.iloc[i]['marketValue']) , float(stock_data.iloc[i]['PE']) , float(stock_data.iloc[i]['PE1']), float(stock_data.iloc[i]['PB']),only_key)
                print n
            print '%s:插入完成'%stock_num[0]
        except Exception as e:
            print e 
            f=open('log.txt','a')
            traceback.print_exc(file=f)   
            f.flush()   
            f.close()   
            #f.write('time:%s,error:%s')%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),str(e))
            #f.close()
            
    

def open_csv(filename):
    try:
        res=pd.read_csv(filename)
        return res

    except Exception as e:
        print e 



def up_data(start,end,stock_num):
    client = dataApi.Client()
    url='/api/market/getMktEqud.csv?field=&beginDate=%s&endDate=%s&secID=&ticker=%s&tradeDate='%(start,end,stock_num)
    code, result = client.getData(url)
    if(code==200):
        return result 
   
    else:
        print code
      

def select_updata():
    stock_list=db.select('select * from code_list')
   
    
    for i in stock_list:
        stock_code=i[u'code'].decode('utf-8')
        stock_num=stock_code.split('.')
        rs=up_data('20150817', '20150817', stock_num[0])
        if '-1:No Data Returned' in rs:
            print '00'
        else:
            hs=rs.split(',')
            temp=[]
            
            for index,i in enumerate(hs[20:]):
                if index==0:
                    h=i.replace('PB\n','')
                    temp.append(h.strip('\"'))
                elif index==20:
                    temp.append(i.replace('\n',''))
                else:
                    temp.append(i.strip('\"'))
    
              
            
            if temp[2] :  
                only_key='%s+%s'%(temp[0],temp[4])
                
                try:
                
                    n=db.update('insert into daily_data(secID, ticker , secShortName , exchangeCD , tradeDate , preClosePrice , actPreClosePrice ,openPrice , highestPrice , lowestPrice , closePrice , turnoverVol , turnoverValue , dealAmount , turnoverRate , accumAdjFactor ,negMarketValue , marketValue , PE ,PE1, PB, only_key) values(?, ? ,? ,? ,? ,? ,? ,? ,? ,?, ?, ? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? )',temp[0],  temp[1] ,temp[2].decode('GB18030').encode('utf-8'), temp[3] , temp[4] , float(temp[5]) , float(temp[6]) ,float(temp[7]) , float(temp[8]) , float(temp[9]) , float(temp[10]) , int(temp[11]) , float(temp[12]) , int(temp[13]) , float(temp[14]) , float(temp[15]) , float(temp[16]) , float(temp[17]) , float(temp[18]) , float(temp[19]), float(temp[20]),only_key)
                    print temp[2].decode('GB18030').encode('utf-8'),n
                    f=open('stock_list.txt','a')
                    f.write('%s,%s,%s\n'%(temp[0],temp[1],temp[2].decode('GB18030').encode('utf-8')))
                    f.close()
                except Exception as e:
                    print e
        
        
    print 'All stock updata done!'

def auto_updata(day):
    f=open('stock_list.txt','r')
    h=f.readlines()
    f.close()
    for i in h:
        stock_line=i.strip().split(',')
        rs=up_data(day, day, stock_line[1])
        if '-1:No Data Returned' in rs:
            print '00'
        else:
            hs=rs.split(',')
            temp=[]
            
            for index,i in enumerate(hs[20:]):
                if index==0:
                    h=i.replace('PB\n','')
                    temp.append(h.strip('\"'))
                elif index==20:
                    temp.append(i.replace('\n',''))
                else:
                    temp.append(i.strip('\"'))
    
                #return temp
            
            if temp[2] :  
                only_key='%s+%s'%(temp[0],temp[4])
                
                try:
                
                    n=db.update('insert into daily_data(secID, ticker , secShortName , exchangeCD , tradeDate , preClosePrice , actPreClosePrice ,openPrice , highestPrice , lowestPrice , closePrice , turnoverVol , turnoverValue , dealAmount , turnoverRate , accumAdjFactor ,negMarketValue , marketValue , PE ,PE1, PB, only_key) values(?, ? ,? ,? ,? ,? ,? ,? ,? ,?, ?, ? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? )',temp[0],  temp[1] ,temp[2].decode('GB18030').encode('utf-8'), temp[3] , temp[4] , float(temp[5]) , float(temp[6]) ,float(temp[7]) , float(temp[8]) , float(temp[9]) , float(temp[10]) , int(temp[11]) , float(temp[12]) , int(temp[13]) , float(temp[14]) , float(temp[15]) , float(temp[16]) , float(temp[17]) , float(temp[18]) , float(temp[19]), float(temp[20]),only_key)
                    print temp[2].decode('GB18030').encode('utf-8'),n
                except Exception as e:
                    print e
        
        
    print 'All stock updata done!'


def getTradeCal(exchangeCD,beginDate,endDate,field):
    client = dataApi.Client()
    url='/api/master/getTradeCal.csv?field=%s&exchangeCD=%s&beginDate=%s&endDate=%s'%(field,exchangeCD,beginDate,endDate)
    code, result = client.getData(url)
    if(code==200):
        return result 
   
    else:
        print code


today=time.strftime("%Y%m%d",time.localtime())
tradecal=getTradeCal(exchangeCD='XSHG',beginDate=today,endDate=today,field='isOpen')
is_open=tradecal.split('\n')
if is_open[1]=='1':
    auto_updata(today)
    print today
else:
    print "today is not trade day!"

#auto_updata('20150901')




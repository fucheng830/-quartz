# -*- coding: utf-8 -*-

import pandas as pd
import dataApi as DA
import cPickle as pickle
import threading
import glob
import os
import time
import lock
from multiprocessing import Process

class account(object):
    
    def __init__(self):
        self.universe=[]
        self.current_date=''
        self.cash=0
        self.secpos={}
        self.valid_secpos={}
        self.referencePrice={}
        self.referencePortfolioValue=0
        self.blotter=[]
        self.days_counter=0
     
        
class StrategyBase(object):
    '''
    @var start:回测开始时间
    @var end:回测结束时间
    @int capital_base:起始资金
    @var commission:手续费标准
    @var slippage:滑点标准
    '''
    def __init__(self,start,end,hist,banchmark,universe,capital_base,commission,slippage):
        self.start = start #开始时间
        self.end = end #结束时间
        self.hist=hist #历史数据长度
        self.banchmark =banchmark #业绩基准
        self.universe =universe #股票池
        self.capital_base = capital_base #起始资金
        self.commission = commission
        self.slippage = slippage
        self.account = account()
        self.today_data= pd.DataFrame()
        self.date_range = pd.DataFrame()
        self.hist_range = pd.DataFrame()
        self.last_hist =[]
        self.stop_change_stock={}
        self.day_hist=[] #日期记录
        self.value_hist =[] #资产记录
        self.return_hist =[] #回报记录
        self.return_view =pd.DataFrame()
        self.__init__ =self.init()
        
        
    def get_cal_date(self):#获取日历
        try:
            res=DA.Api()
            date_range=res.getTradeCal('XSHG','','','calendarDate,isOpen,prevTradeDate')
            hist_range=date_range[date_range['calendarDate']<self.start]
            hist_range=hist_range[hist_range['isOpen']=='1']#isOpen为字符串
            hist_range=hist_range.iloc[hist_range.shape[0]-self.hist:hist_range.shape[0]] 
            date_range=date_range[date_range['calendarDate']>=self.start]
            date_range=date_range[date_range['calendarDate']<=self.end]
            self.date_range=date_range
            self.hist_range=hist_range
        except Exception as e:
            raise e
          
    def init(self):
        
        self.get_cal_date()#获取日历
        p1 = Process(target=chack_cache,args=(self.date_range,))
        #print "start download data!"
        p2 = Process(target=chack_cache,args=(self.hist_range,))
        p1.start()
        p2.start()
        self.get_hist_day()
         
    def get_hist_day(self):
        hist_data_list=[]
        for i in range(self.hist_range.shape[0]):
            temp=self.read_cache(self.hist_range.iloc[i]['calendarDate'].replace('-',''))
            hist_data_list.append(temp)
        self.last_hist=hist_data_list
           
    def save_hist(self):
        self.last_hist.append(self.today_data)
        while len(self.last_hist)>self.hist:
            self.last_hist.pop(0)
            
    def get_last_data(self):
        last_data=pd.concat(self.last_hist)
        return last_data
        
    def read_cache(self,name):#读缓存函数
        abs_path=os.path.abspath('..')
        while glob.glob("%s\data\%s.pkl"%(abs_path,name)) == []:
            time.sleep(6)
        t1=time.time()
        while True:
            try:
                f1=file('../data/%s.pkl'%name,'rb')
                p1=pickle.load(f1)
                f1.close()
                return p1
                break
            except:
                time.sleep(6)
           
    def get_singal_price(self,aymbol):
        rows=self.today_data[self.today_data.secID==aymbol]
        self.tempdata=rows
        return float(rows.iloc[0]['openPrice'])
        
    def run(self):
        #self.my_thread(self.chack_cache(self.date_range))
        #self.my_thread(self.orap())
        print "start strategy..."
        len=self.date_range.shape[0]
        self.account.cash=self.capital_base
        self.initialize()
        for i in range(len):
            if self.date_range.iloc[i]['isOpen']=='1':
                self.account.days_counter=i+1
                self.account.current_date=self.date_range.iloc[i]['calendarDate'].replace('-','')
                self.today_data=self.read_cache(self.account.current_date)
                self.handle_data()
                self.save_hist()#更新30天数据池
                self.day_record()
        data={'time': self.day_hist,
              'return_back':self.return_hist,
              'value':self.value_hist
             
              }
        self.return_view=pd.DataFrame(data,index=data['time'])
       
        
    
    def day_record(self):
        self.account.cash
        value=0
        for stock in self.account.secpos:
            stock_data=self.today_data[self.today_data['secID']==stock]
            price=float(stock_data.iloc[0]['closePrice'])
            if price == 0 :
                if stock in self.stop_change_stock:
                    price=float(self.stop_change_stock[stock])#查询是否属于停牌股票，获得停牌前价格
                else:
                    price=float(stock_data.iloc[0]['preclosePrice']) #首次停牌股票，获得停牌前价格
                    self.stop_change_stock[stock]=price
            else:
                if stock in self.stop_change_stock:
                    self.stop_change_stock.pop(stock)
                else:
                    pass
            value+=(int(self.account.secpos[stock])*price)
        
        
        self.account.referencePortfolioValue=value+self.account.cash
        value_return=float(self.account.referencePortfolioValue-self.capital_base)/self.capital_base
        self.return_hist.append(value_return)
        self.value_hist.append(self.account.referencePortfolioValue)
        self.day_hist.append(self.account.current_date)
        
        

    
    def initialize(self):
        pass
    
    def handle_data(self):
        pass
        
    def order(self,aymbol,amount):
        
        price=self.get_singal_price(aymbol)
        if amount>0 and price>0:
            #买入
            volum=int(amount/100)*100
            order_money=(price*volum)*(1+float(self.commission[0]))
            if order_money<=self.account.cash:
                self.account.cash-=order_money
                if aymbol in  self.account.secpos:
                    self.account.secpos[aymbol]+=volum
                else:
                    self.account.secpos[aymbol]=volum
                self.botter=['behaviour:buy','secID:%s'%aymbol,'secShortName:%s'%self.tempdata.iloc[0]['secShortName'],'tradeDate:%s'%self.account.current_date,'price:%f'%price,'volum:%d'%volum,'cost_money:%f'%order_money]
                return 1
            else :
                return 0
        elif amount<0 and price>0:
            #卖出
            volum=int(abs(amount)/100)*100
            order_money=(price*volum)*(1-float(self.commission[1]))
            if aymbol in  self.account.secpos and self.account.secpos[aymbol]>=volum :
                self.account.cash+=order_money
                self.account.secpos[aymbol]-=volum
                self.botter=['behaviour:sell','secID:%s'%aymbol,'secShortName:%s'%self.tempdata.iloc[0]['secShortName'],'tradeDate:%s'%self.account.current_date,'price:%f'%price,'volum:%d'%volum,'cost_money:%f'%order_money]
                return 1
            else:
                print "botter_error:no enough stock!"
                return 0
        else:
            pass
            
            
    
    def order_to(self,symbol,amount):
        pass
    
    def max_buy(self,aymbol,cash):
        pass  


def chack_cache(date_range):#检查数据缓存
    try:
        date_range=date_range[date_range['isOpen']=='1']
        abs_path=os.path.abspath('..')
        for i in range(date_range.shape[0]):
            day=date_range.iloc[i]['calendarDate'].replace('-','')
            have_file=glob.glob("%s\data\%s.pkl"%(abs_path,day))
            if have_file == []:
                write_cache(day)
                print "download data: %s done!"%day
            else:
                size=os.path.getsize("%s\data\%s.pkl"%(abs_path,day))
                if size < 10:
                    write_cache(day)
                
    except Exception as e:
        print e

def write_cache(name):#写入数据缓存
    
    f1=file('../data/%s.pkl'%name,'wb')
    p1=get_all_market_data(name)
    if p1 is not None:
        pickle.dump(p1,f1,True)
    f1.close()
    
    

def get_all_market_data(current_data):
        res=DA.Api()
        data=res.getMktEqud('','',current_data,'','')
        
        #print data
        return data


if __name__ == '__main__':
    pass
    #data=pd.read_csv('../data/600006.csv')
    #new_obj=take_back('2006-01-09','2007-01-09',data,cash=100000)
    #new_obj.handle()
    
    #res=DA.Api()
    #print res.getTradeCal('XSHG','','','calendarDate,isOpen,prevTradeDate')
    #mystrategy=StrategyBase(start='2012-01-01',end='2014-01-01',banchmark='HS300',universe='A',capital_base=10000000,commission=0.01,slippage=0)
    #date_range=mystrategy.get_cal_date()
    #date_range=date_range[date_range['isOpen']=='1']
    #for i in range(date_range.shape[0]):
        #name=date_range.iloc[i]['calendarDate'].replace('-','')
        #print name
        #mystrategy.write_cache(name)
        
       
   
    #print mystrategy.get_all_market_data('20150902')
    
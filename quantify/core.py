# -*- coding: utf-8 -*-

import pandas as pd
import dataApi as DA

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
    @var capital_base:起始资金
    @var commission:手续费标准
    @var slippage:滑点标准
    '''
    def __init__(self,start,end,banchmark,universe,capital_base,commission,slippage):
        self.start = start
        self.end = end
        self.banchmark =banchmark
        self.universe =universe
        self.capital_base = capital_base
        self.commission = commission
        self.slippage = slippage
        self.account = account()
        self.all_market_data= pd.DataFrame()
    
    def get_cal_date(self):
        try:
            res=DA.Api()
            date_range=res.getTradeCal('XSHG',self.start.replace('-',''),self.end.replace('-',''),'calendarDate,isOpen,prevTradeDate')
            return date_range
        except Exception as e:
            raise e
        
    def get_all_market_data(self,current_data):
        try:
            res=DA.Api()
            all_market_data=res.getMktEqud('','',current_data,'','','')
            return all_market_data
        except Exception as e:
            raise e
    
    def get_singal_price(self,aymbol):
        rows=self.all_market_data[self.all_market_data.secID==aymbol]
        self.tempdata=rows
        return float(rows.iloc[0]['openPrice'])
        
    def run(self):
        date_range=self.get_cal_date()
        #print date_range
        #all_market_data=self.get_all_market_data()
        len=date_range.shape[0]
        self.account.cash=self.capital_base
        self.initialize()
        for i in range(len):
            if date_range.iloc[i]['isOpen']=='1':
                self.account.days_counter=i+1
                self.account.current_date=date_range.iloc[i]['calendarDate'].replace('-','')
                self.all_market_data=self.get_all_market_data(self.account.current_date)
                self.handle_data()
    
    
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
        
class take_back:
    
    def __init__(self,start,end,data,cash,rate=0.003):
        self.start=start #回测开始时间
        self.end=end #回测结束时间
        self.data=data
        self.today=start
        self.days_counter=0
        self.cash=cash
        self.stock=0
        self.back_data=pd.DataFrame({})
        self.rate=rate
        self.tax=0.001
        self.max_buy=0
        self.max_sell=0
        self.price=0 
        
        
    def get_back_data(self):
        temp_a=self.data[self.data['tradeDate']<=self.end]
        temp_b=temp_a[temp_a['tradeDate']>=self.start]
        return temp_b
    
    def strategy(self):
        pass
        
    def order(self,num,market):
        i=self.days_counter-1
        order_time=self.back_data.iloc[i]['tradeDate']
        
        if num>0:
            behavior='buy' #操作：1=买，-1=卖
            if self.max_buy>0:
            
                if num>self.max_buy:
                    num=self.max_buy
                    print 'order:buy %f ,max_buy %f , max_sell %f '%(num,self.max_buy,self.max_sell)
                    #num单位为手
                    self.cash=self.cash-(num*self.price*100+self.cost(self.price, num, market, behavior, self.rate))
                    self.stock=self.stock+num*100
                else:
                    print 'order:buy %f ,max_buy %f , max_sell %f '%(num,self.max_buy,self.max_sell)
                    self.cash=self.cash-(num*self.price*100+self.cost(self.price, num, market, behavior, self.rate))
                    self.stock=self.stock+num*100
            else:
                print 'order:buy %f faild ,no enough money'%num
                
        elif num<0 :
            
            behavior='sell'
            
            if self.max_sell>0:
                
                if abs(num)>self.max_sell:
                    num=self.max_sell
                    print 'order:sell %f ,max_buy %f , max_sell %f '%(num,self.max_buy,self.max_sell)
                    self.cash=self.cash+num*self.price*100-self.cost(self.price, num*100, market, behavior, self.rate)
                    self.stock=self.stock-num*100
                else:
                    num=abs(num)
                    print 'order:sell %f ,max_buy %f , max_sell %f '%(num,self.max_buy,self.max_sell)
                    self.cash=self.cash+num*self.price*100-self.cost(self.price, num*100, market, behavior, self.rate)
                    self.stock=self.stock-num*100
                    
            else:
                print 'order:sell %f faild ,no enough stock'%abs(num)
            
    def max_num(self,price,market,behavior,rate):
        if behavior=='buy':
            num=0
            #print self.cash,num*price*100+self.cost(price, num*100, market, behavior, rate)
            #print self.cash,num*price*100+self.cost(price, num*100, market, behavior, rate)
            while self.cash>=(num*price*100+self.cost(price, num*100, market, behavior, rate)):
                num+=1
            
                #print num
            return num-1
        elif behavior=='sell':
            if self.stock:
                sell_num=self.stock/100
            else:
                sell_num=0
            return sell_num
        
            
            
    def cost(self,price,num,market,behavior,rate):
        if behavior=='buy':
            if market=='sh':
                if num<=1000:
                    if price*num*rate<=5:
                        cost=1+5
                    elif price*num*rate>5:
                        cost=1+price*num*rate
                    else:
                        message="num or rate or price数据类型错误"
                        return  message
                elif num>1000:
                    if price*num*rate<=5:
                        cost=0.001*num+5
                    elif price*num*rate>5:
                        cost=0.001*num+price*num*rate
                    else:
                        message="num or rate or price数据类型错误"
                        return  message
                else:
                    message="num数据类型错误"
                    return  message
                
            elif market=='sz':
                if price*num*rate<=5:
                    cost=5
                elif price*num*rate>5:
                    cost=price*num*rate
                else:
                    message="num or rate or price数据类型错误"
                    return  message
            
        if behavior=='sell':
            if market=='sh':
                if num<=1000:
                    if price*num*rate<=5:
                        cost=1+5+self.tax*num
                    elif price*num*rate>5:
                        cost=1+price*num*rate+self.tax*num
                    else:
                        message="num or rate or price数据类型错误"
                        return  message
                elif num>1000:
                    if price*num*rate<=5:
                        cost=0.001*num+5+self.tax*num
                    elif price*num*rate>5:
                        cost=0.001*num+price*num*rate+self.tax*num
                    else:
                        message="num or rate or price数据类型错误"
                        return  message
                else:
                    message="num数据类型错误"
                    return  message
                
            if market=='sz':
                if price*num*rate<=5:
                    cost=5+self.tax*num
                elif price*num*rate>5:
                    cost=price*num*rate+self.tax*num
                else:
                    message="num or rate or price数据类型错误"
                    return  message
        return cost
    
    def handle(self):
        self.back_data=self.get_back_data()
        data_length=self.back_data.shape[0]
        for i in range(data_length):
            self.today=self.back_data.iloc[i]['tradeDate']
            self.days_counter=i+1
            self.price=self.back_data.iloc[i]['openPrice']
            if self.price>0:
                self.max_buy=self.max_num(self.price, 'sh', 'buy', self.rate)
                self.max_sell=self.max_num(self.price, 'sh', 'sell', self.rate)
                #print self.max_buy,self.max_sell
                self.strategy()
            else:
                print 'today is suspended '
            
        
    
if __name__ == '__main__':
    #data=pd.read_csv('../data/600006.csv')
    #new_obj=take_back('2006-01-09','2007-01-09',data,cash=100000)
    #new_obj.handle()
    
    #res=DA.Api()
    #print res.getTradeCal('XSHG','','','calendarDate,isOpen,prevTradeDate')
    mystrategy=StrategyBase(start='2012-01-01',end='2014-01-01',banchmark='HS300',universe='A',capital_base=10000000,commission=0.01,slippage=0)
    #print mystrategy.get_all_market_data('20150902')
    
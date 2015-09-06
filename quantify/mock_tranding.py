# -*- coding: utf-8 -*-

import tushare as ts
import time

#===============================================================================
# 沪深股票模拟仿真交易系统
#===============================================================================
rate=0.00025
tax=0.001 



class tranding:
    
    def __init__(self):
        pass
    
    def get_today_all(self):
        #--获取全市场行情快照
        res=ts.get_today_all()
        return res
    
    def order_buy(self,symbols):
        df=ts.get_realtime_quotes(symbols)
        return df.iloc[0]
    
#------------------------------------------------------------------------------ 行情订阅函数(不太稳定)
    def subscuiber(self,symbols):
        df=ts.get_realtime_quotes(symbols)
        print df[['code','name','price','bid','ask','volume','time']]
        str_time='%s %s'%(df.iloc[0]['date'],df.iloc[0]['time'])
        unix_time=time.mktime(time.strptime(str_time,"%Y-%m-%d %H:%M:%S")) #把时间转换为时间戳
        now_time=time.time()
        next_time=unix_time+3
        sleep_time=now_time-next_time
        time.sleep(sleep_time)
        self.subscuiber(symbols)
    
    
    def buy_market_price(self,ticker,exchangeCD,hand_num):#此模块需要优化
        ''' symbol 为 secID  XSHG  为沪市股票    XSHE 为深市股票'''
        
        df=ts.get_realtime_quotes(ticker)
        num_list=[int(df.iloc[0]['a1_v']),int(df.iloc[0]['a2_v']),int(df.iloc[0]['a3_v']),int(df.iloc[0]['a4_v']),int(df.iloc[0]['a5_v'])]
        price_list=[float(df.iloc[0]['a1_p']),float(df.iloc[0]['a2_p']),float(df.iloc[0]['a3_p']),float(df.iloc[0]['a4_p']),float(df.iloc[0]['a5_p'])]
        #exchang_list:成交详细  total_money:成交总额金额 未加手续费
        exchang_list,total_money,exchange_num=self.num_list_ad(num_list,price_list,hand_num)
        cost_money=self.cost(total_money,hand_num*100,exchangeCD,'buy')
        toal_need_money=total_money+cost_money
        return toal_need_money,exchange_num,exchang_list
    
    def sell_market_price(self,ticker,exchangeCD,hand_num): 
        pass
    
    
        
    def cost(self,total_money,stock_num,exchangeCD,behavior):
        if behavior=='buy':
            if exchangeCD=='XSHG':
                transfer_cost=stock_num*0.001
                if transfer_cost>1:
                    pass
                else:
                    transfer_cost=1
                
                rate_cost=total_money*rate
                if rate_cost>5:
                    pass
                else:
                    rate_cost=5
                
                total_cost=transfer_cost+rate_cost
                
              
            elif exchangeCD=='XSHE':
                rate_cost=total_money*rate
                if rate_cost>5:
                    pass
                else:
                    rate_cost=5
                total_cost=rate_cost
                
            
        if behavior=='sell':
            if exchangeCD=='XSHG':
                transfer_cost=stock_num*0.001
                if transfer_cost>1:
                    pass
                else:
                    transfer_cost=1
                
                rate_cost=total_money*rate
                if rate_cost>5:
                    pass
                else:
                    rate_cost=5
                
                tax_cost=total_money*tax
                
                total_cost=transfer_cost+rate_cost+tax_cost
                
            
            elif  exchangeCD=='XSHE':
              
                rate_cost=total_money*rate
                if rate_cost>5:
                    pass
                else:
                    rate_cost=5
                
                tax_cost=total_money*tax
                
                total_cost=rate_cost+tax_cost
               
        return total_cost
        

    
    def num_list_ad(self,num_list,price_list,num):#累加计算num
        i=0
        num_l=num_list[i]
        exchange_list=[]
        money=0.0
        while num>num_l:
            i+=1
            
            if i>4:
                num=num_l
            else:
                num_l+=num_list[i]
        #print i,num,num_l
        if i==5:
            i=4        
        step_list=range(i+1)
        #print step_list
        for x in step_list:
            if x==step_list[-1]:
                exchange_list.append([num_list[x]-num_l+num,price_list[x]])
                money+=(num_list[x]-num_l+num)*price_list[x]*100
            else:
                exchange_list.append([num_list[x],price_list[x]])
                money+=num_list[x]*price_list[x]*100
            
        return exchange_list,money,num
            
            
        
        

if __name__ == '__main__':
    mock=tranding()
    print mock.buy_market_price('600006','XSHG',50000)
    #print mock.get_today_all()
    
    
    
# -*- coding: utf-8 -*-

import pandas as pd 
import talib as ta
import numpy as np
from quantify.core import take_back

#temp_a=data[data['tradeDate']<='2007-01-09']
#temp_b=temp_a[temp_a['tradeDate']>='2006-01-09']
#print temp_b
#计算RSI值
#data['RSI']=ta.RSI(close_price)




def Get_KDJ(data):
    #参数9,3,3
    slowk,slowd=ta.STOCH(np.array(data['highestPrice']), np.array(data['lowestPrice']), np.array(data['closePrice']),fastk_period=9, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    data['slowk']=slowk
    data['slowd']=slowd
    

    

    
class new_tack_back(take_back):    
    
    def strategy(self):
        if self.back_data.iloc[self.days_counter-1]['slowk']<10:
            self.order(num=10000, market='sh')
            #print self.cash,self.stock
        elif self.back_data.iloc[self.days_counter-1]['slowd']<self.back_data.iloc[self.days_counter-2]['slowd']:
            self.order(num=-10000, market='sh')
            #print self.cash,self.stock
        print self.cash,self.stock
        
    
            
if __name__ == '__main__':
    data=pd.read_csv('../data/600006.csv')
    
    #Get_KDJ(data)
    #tb=new_tack_back('2006-01-09','2015-01-09',data,100000)
    #tb.handle()


'''
length=data.shape[0]
for i in range(length):
    print data.iloc[i]['closePrice'],data.iloc[i]['slowk'],data.iloc[i]['slowd']
''' 

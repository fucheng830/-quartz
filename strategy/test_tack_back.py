# -*- coding: utf-8 -*-

from quantify.core import StrategyBase
import pandas as pd
from pylab import *

class mystrategy(StrategyBase):
    
    def handle_data(self):
        data=pd.DataFrame()
        last_data=self.get_last_data()
        ls=last_data[last_data['secID']=='600006.XSHG']
        m1=np.array(pd.rolling_mean(ls['closePrice'],5))
        m2=np.array(pd.rolling_mean(ls['closePrice'],15))
        
  

        if isnan(m1[-1]) or isnan(m2[-1]) :
            pass
        else:
            if m1[-1]>m2[-1] and m1[-2]<m2[-2]:
                res=self.order('600006.XSHG',100000)
            if m1[-1]<m2[-1] and m1[-2]>m2[-2]:
                res=self.order('600006.XSHG',-100000)
            print self.account.referencePortfolioValue
        #print self.botter
        
        
if __name__ == '__main__':
    my=mystrategy(start='2011-01-01',end='2015-01-01',hist=30,banchmark='HS300',universe='A',capital_base=10000000,commission=[0.001,0.002],slippage=0)
    #my.get_cal_date()
    #my.get_hist_day()
    #print my.date_range.shape[0]
    #print my.hist_range.shape[0]
   
    my.run()
    print my.get_botter_list()
    #my.return_view['return_back'].plot()
    #show()
    
    
    #plt.savefig('hf.png')
    
    
    
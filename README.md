# -quartz
量化回测框架
例程：

from quantify.core import StrategyBase  
import pandas as pd     
from pylab import *  
核心类库引用
引入pandas
如果需要可视化结果 需要引入pylab库

继承策略类

class mystrategy(StrategyBase):

    #重写策略主函数  默认每个交易日调用一次
    
    def handle_data(self):
    
        #实现策略代码 
        
        data=pd.DataFrame()
        last_data=self.get_last_data() 
        
        #调用get_last_data()方法可以获得当前回测日期的历史数据 数据长度由参数定义
        
        ls=last_data[last_data['secID']=='600006.XSHG']  
        
        #get_last_Data()返回的是历史数据的pandas数据格式 
        
        m1=np.array(pd.rolling_mean(ls['closePrice'],5)) 
        
        #计算5日均线
        
        m2=np.array(pd.rolling_mean(ls['closePrice'],15)) 
        
        #计算10日均线
        
  

        if isnan(m1[-1]) or isnan(m2[-1]) :  #排除空值
            pass
        else:
            if m1[-1]>m2[-1] and m1[-2]<m2[-2]:    #金叉
                res=self.order('600006.XSHG',100000)   #买入600006 100000 股
            if m1[-1]<m2[-1] and m1[-2]>m2[-2]:   #死叉
                res=self.order('600006.XSHG',-100000)  #卖出 600006 100000股
            print self.account.referencePortfolioValue   
        #print self.botter
        
        
if __name__ == '__main__':

    my=mystrategy(start='2011-01-01',end='2015-01-01',hist=30,banchmark='HS300',universe='A',capital_base=10000000,commission=[0.001,0.002],slippage=0)#初始化策略类
    my.run()#执行回测
    #start 开始日期
    #end 结束日期
    #hist 历史数据长度
    #banchmark 业绩基准
    #universe 股票池
    #capital_base 初始金额
    #commission 交易手续费
    #slippage 滑点

   
    

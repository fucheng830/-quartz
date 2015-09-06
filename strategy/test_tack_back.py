# -*- coding: utf-8 -*-

from quantify.core import StrategyBase

class mystrategy(StrategyBase):
    
    def handle_data(self):
        res=self.order('601288.XSHG',100000)
        if self.account.secpos['601288.XSHG']>=300000:
            res=self.order('601288.XSHG',-400000)
        print res,self.account.cash
        print self.botter
        
if __name__ == '__main__':
    my=mystrategy(start='2012-01-01',end='2014-01-01',banchmark='HS300',universe='A',capital_base=10000000,commission=[0.001,0.002],slippage=0)
    my.run()
    
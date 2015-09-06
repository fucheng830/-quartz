# -*- coding: utf-8 -*-

import pandas as pd 
import talib as ta
import numpy as np

def Get_ADX(data):
    #print ta.ADX(np.array(data['highestPrice']), np.array(data['lowestPrice']), np.array(data['closePrice']))
    
    for i in range(data.shape[0]):
        if i>14:
            hd=np.array(data.iloc[i-13:i]['highestPrice'])-np.array(data.iloc[i-14:i-1]['highestPrice'])
            ld=np.array(data.iloc[i-14:i-1]['lowestPrice'])-np.array(data.iloc[i-13:i]['lowestPrice'])
            t1=np.array(data.iloc[i-13:i]['highestPrice'])-np.array(data.iloc[i-13:i]['lowestPrice'])
            t2=np.array(data.iloc[i-13:i]['highestPrice'])-np.array(data.iloc[i-14:i-1]['closePrice'])
            t3=np.array(data.iloc[i-13:i]['lowestPrice'])-np.array(data.iloc[i-14:i-1]['closePrice'])
            PDI,MDI=D_MIp_MIn(hd,ld,t1,t2,t3)
            return PDI,MDI 
            
def D_MIp_MIn(hd,ld,t1,t2,t3):
    MIp=[]
    NIp=[]
    tr=[]
    for i in range(len(hd)):
        if hd[i]>0 and hd[i]>ld[i]:
            MIp.append(hd[i])
        else:
            MIp.append(0)
        if ld[i]>0 and ld[i]>hd[i]:
            NIp.append(ld[i])
        else:
            NIp.append(0)
            
            
        tr_n=max(max(t1[i],abs(t2[i])),abs(t3[i]))
        tr.append(tr_n)
        
    np_MIP=np.array(MIp)
    np_NIP=np.array(NIp)
    np_tr=np.array(tr)
    PDI=np_MIP.mean()*100/np_tr.mean()
    MDI=np_NIP.mean()*100/np_tr.mean()
    return PDI,MDI
            

 
    
    
    
data=pd.read_csv('../data/600006.csv')   
Get_ADX(data)



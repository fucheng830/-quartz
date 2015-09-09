#-*-coding:utf-8 -*-

import httplib
import traceback
import urllib
import ssl
import pandas as pd

HTTP_OK = 200
HTTP_AUTHORIZATION_ERROR = 401

ssl._create_default_https_context = ssl._create_unverified_context

class Api:
    domain = 'api.wmcloud.com'
    port = 443
    token = '7cd1e7bca0ec4c91aa2bdb09d96dc5497ce01aad745b510435462c81198a8638'
    httpClient = None
    def __init__( self ):
        self.httpClient = httplib.HTTPSConnection(self.domain, self.port)
    def __del__( self ):
        if self.httpClient is not None:
            self.httpClient.close()
    def encodepath(self, path):
        #转换参数的编码
        start=0
        n=len(path)
        re=''
        i=path.find('=',start)
        while i!=-1 :
            re+=path[start:i+1]
            start=i+1
            i=path.find('&',start)
            if(i>=0):
                for j in range(start,i):
                    if(path[j]>'~'):
                        re+=urllib.quote(path[j])
                    else:
                        re+=path[j]  
                re+='&'
                start=i+1
            else:
                for j in range(start,n):
                    if(path[j]>'~'):
                        re+=urllib.quote(path[j])
                    else:
                        re+=path[j]  
                start=n
            i=path.find('=',start)
        return re
    def init(self, token):
        self.token=token
    def getData(self, path):
        result = None
        path='/data'+path
        path=self.encodepath(path)
        #print path
        try:
            #set http header here
            self.httpClient.request('GET', path, headers = {"Authorization": "Bearer " + self.token})
            #make request
            response = self.httpClient.getresponse() 
            #read result
            if response.status == HTTP_OK:
                
                result = response.read()
                
            else:
                
                result = response.read()
               
            return response.status, result
        
        except Exception, e:
            #traceback.print_exc()
            raise e
        return -1, result
 
    def getMktEqud(self,secID,ticker,tradeDate,beginDate,endDate):
        url='/api/market/getMktEqud.csv?field=&beginDate=%s&endDate=%s&secID=%s&ticker=%s&tradeDate=%s'%(beginDate,endDate,secID,ticker,tradeDate)
        code, result = self.getData(url)
        if(code==200):
            #print len(result)
            while len(result)==0:
                pass
            
            result=result.split('\n')                   
            colume=result[0].split(',')#获取字段名称
            result.pop(0)
            result.pop(-1)
            temp=[]
            for line in result:
                temp1=line.split(',')
                temp_line=[]
                #print temp1
                for index,i in enumerate(temp1):
                    if index<5:
                        temp_line.append(i.strip('\"').decode('GB18030').encode('utf-8'))
                    elif index>=5:
                        while i=='':
                            i='0'
                        temp_line.append(float(i.strip('\"').decode('GB18030').encode('utf-8')))
                temp.append(temp_line)
            return pd.DataFrame(temp,columns=colume)
            
        else:
            print code
    
    def getTradeCal(self,exchangeCD,beginDate,endDate,field):
        url='/api/master/getTradeCal.csv?field=%s&exchangeCD=%s&beginDate=%s&endDate=%s'%(field,exchangeCD,beginDate,endDate)
        code, result = self.getData(url)
        if(code==200):
            return csv_to_pandas(result) 
        else:
            print code 


def csv_to_pandas(data):
    data=data.split('\n')
    #print data
    #获取字段名称
    colume=data[0].split(',')
    data.pop(0)
    data.pop(-1)
    temp=[]
    for line in data:
        temp1=line.split(',')
        temp_line=[]
        for i in temp1:
            temp_line.append(i.strip('\"').decode('GB18030').encode('utf-8'))
        temp.append(temp_line)
    return pd.DataFrame(temp,columns=colume)

def change_str(char):
    while char=='':
        char=='0'
    try:
        temp=float(char)
        if str(temp) == char:
            return float(char) 
        else:
            return int(char)      
    except:
        return char
    
    
        
    
            
if __name__ == '__main__':
        
    api=Api()
    res=api.getTradeCal('XSHG','','','calendarDate')
    res=res[res['calendarDate']>='2006-01-01']  
    #res=api.getMktEqud('', '', '20120104', '', '')
    print res
    #print res[res.secID=='601288.XSHG']

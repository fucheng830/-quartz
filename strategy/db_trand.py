# -*- coding: utf-8 -*-

import pandas as pd 
import talib as ta
import numpy as np
from quantify import db,dataApi 
import mysql.connector


#db.create_engine(user='root', password='', database='quant', host='127.0.0.1', port=3306)
#res=db.select('select * from daily_data where secID=?','300482.XSHE')
#for index,i in enumerate(res):
    #print index,i 

conn=mysql.connector.connect(user='root',password='',database='quant')
#cursor=conn.cursor()
#cursor.execute('select * from daily_data where secID=%s',['300482.XSHE'])
sql="SELECT * FROM daily_data"
res=pd.read_sql(sql, conn, index_col='data_id')
print res.iloc[0]['secID'].decode('utf-8')
#values=cursor.fetchall()
#print values    

#cursor.close()
#conn.close()
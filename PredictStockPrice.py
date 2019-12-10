# *********************************************************************
# Future Stick Price Prediction using StockPricePredictModel (ver 1.0)
#
# Model Location            : C:\Datapy\stockPricePredictModel.sav
# Language                  : Python
# Command Line Aurguments   : Stock Symbol
#
# *********************************************************************

import pandas as pd
import numpy as np
import pyodbc
import pickle
import sys

try:

    # Read the 2nd Arg
    stockSymbol = sys.argv[1]

    # Connect to SQL Server
    conn_str = ('server=WIN-EEL3AK31AJF;database=DatapyDB;TRUSTED_CONNECTION=yes')
    conn = pyodbc.connect(r'DRIVER={ODBC Driver 13 for SQL Server};' + conn_str)

    
    # Get the last record from dbo.Stock table and use it as input to the Model
    # to predict future stock price
    
    sql = str("SELECT TOP 1 StockSym,StockDt,StockOpen,StockHigh,StockLow,StockClose,StockAdjClose,StockVol,\
           LAG(StockAdjClose,1,NULL) over (order by StockDt) StockAdjClose_DayMinus1, \
           LAG(StockVol,1,NULL) over (order by StockDt) StockVol_DayMinus1, \
           LAG(StockVol,2,NULL) over (order by StockDt) StockVol_DayMinus2, \
           LAG(StockVol,3,NULL) over (order by StockDt) StockVol_DayMinus3 \
           FROM dbo.Stock where StockSym = '$' \
           AND StockDt < '2019-12-06' \
           ORDER BY StockDt DESC;").replace('$',stockSymbol) 

    dfLastRecordedTrade = pd.read_sql(sql,conn)

    # Remove Stock Symbol and Stock Date Columns from the DataFrame
    dfLastRecordedTrade = dfLastRecordedTrade.drop(['StockSym'],axis=1)
    dfLastRecordedTrade = dfLastRecordedTrade.drop(['StockDt'],axis=1)

    inputX = np.array(dfLastRecordedTrade)

    # Load the Model (from file system) using pickle module
    StockPricePredictModel = pickle.load(open('C:\\Datapy\\stockPricePredictModel.sav', 'rb'))
    futureStockPrice = StockPricePredictModel.predict(inputX)

    print('Future Stock Price is :' + str(futureStockPrice[0]))

except Exception as e:
    print('Please check errors')
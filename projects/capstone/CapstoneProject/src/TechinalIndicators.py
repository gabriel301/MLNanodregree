# -*- coding: utf-8 -*-
import pandas as pd
import os 
import argparse
import numpy as np
import talib
import ntpath
from Util import Util

class TechnicalIndicators:

    #ShortTerm - 10 days, 1.9 std
    #Standard - 20 days, 2 std
    #LongTerm - 50 days, 2.1 std
    def GetBollingerBands(self,values,period,std,prefix,supressMessage = True):
        prefix = prefix+"_"
        if not supressMessage:
            print "Calculating Bollinger Bands..."
        upperband, middleband, lowerband = talib.BBANDS(values,period,std)
        values = [lowerband,middleband,upperband]
        columns = [prefix+"Lower_BBand",prefix+"Mid_BBand",prefix+"Upper_BBand"]
        df = Util().BuildDataFrame(columns,values).copy()
        return df
    
    #Short Term - 15 days
    #Standard - 30 days
    #Long Term - 60 days
    def GetSMA(self,values,period,prefix,supressMessage = True):
        prefix = prefix+"_"
        if not supressMessage:
            print "Calculating Simple Moving Average..."
        result = talib.SMA(values,period)
        values = [result]
        columns = [prefix+"SMA"]
        df = Util().BuildDataFrame(columns,values).copy()
        return df

    #Short Term - 15 days
    #Standard - 30 days
    #Long Term - 60 days
    def GetEMA(self,values,period,prefix,supressMessage = True):
        prefix = prefix+"_"      
        if not supressMessage:
            print "Calculating Exponential Moving Average..."
        result = talib.EMA(values,period)
        values = [result]
        columns = [prefix+"EMA"]
        df = Util().BuildDataFrame(columns,values).copy()
        return df

    def GetMomentum(self,values,prefix,supressMessage = True):
        prefix = prefix+"_"
        if not supressMessage:
            print "Calculating Momentum..."
        result = talib.MOM(values)
        values = [result]
        columns = [prefix+"MOM"]
        df = Util().BuildDataFrame(columns,values).copy()
        return df

    def GetRSI(self,values,prefix,supressMessage):
        prefix = prefix+"_"
        if not supressMessage:
            print "Calculating Relative Strength Index (RSI)..."          
        result = talib.RSI(values)
        values = [result]
        columns = [prefix+"RSI"]
        df = Util().BuildDataFrame(columns,values).copy()
        return df

    #Standard - fastperiod=12, slowperiod=26, signalperiod=9   
    def GetMACD(self,values,prefix,supressMessage = True):
        prefix = prefix+"_"
        if not supressMessage:
            print "Calculating Moving Average Convergence/Divergence (MACD)..."
        macd, macdsignal, macdhist = talib.MACD(values)
        values = [macd,macdsignal,macdhist]
        columns = [prefix+"MACD",prefix+"MACD_SIGNAL",prefix+"MACD_HIST"]
        df = Util().BuildDataFrame(columns,values).copy()
        return df

      
    def GetStochastic(self,high,low,close,prefix,supressMessage = True):
        if not supressMessage:
            print "Calculating Sthocastic Indicator..."
        slowk, slowd = talib.STOCH(high,low,close)
        values = [slowk,slowd]
        columns = [prefix+"SLOWK",prefix+"SLOWD"]
        df = Util().BuildDataFrame(columns,values).copy()
        return df

    def GetIndicators(self,df,ticker,outputFolder="",writeInFile = False, supressMessage = True):
        outputFolder = os.path.join(outputFolder,"Data/Historical/Indicators")
        values = df['Norm_Adjusted_Close'].values
        dfs = []
        #dfs.append(self.GetSMA(values,15,"Short",supressMessage))
        dfs.append(self.GetSMA(values,30,"Middle",supressMessage))
        #dfs.append(self.GetSMA(values,50,"Long",supressMessage))
        #dfs.append(self.GetEMA(values,15,"Short",supressMessage))
        dfs.append(self.GetEMA(values,30,"Middle",supressMessage))
        #dfs.append(self.GetEMA(values,50,"Long",supressMessage))
        dfs.append(self.GetMomentum(values,"Std",supressMessage))
        dfs.append( self.GetRSI(values,"Std",supressMessage))
        dfs.append(self.GetMACD(values,"Std",supressMessage))
        dfs.append(self.GetStochastic(df['Norm_High'].values,df['Norm_Low'].values,values,"Std",supressMessage))
        #dfs.append(self.GetBollingerBands(values,10,1.9,"Short",supressMessage))
        dfs.append(self.GetBollingerBands(values,20,2,"Middle",supressMessage))
        #dfs.append(self.GetBollingerBands(values,50,2.1,"Long",supressMessage))
        dfResult = pd.concat(dfs,axis=1)
        dfResult = Util().Normalize(dfResult,dfResult.columns.values)
        if(writeInFile):
            Util().WriteDataFrame(dfResult,outputFolder,ticker+".csv")
        return dfResult

    def GetIndicatorsFromDF(self,dfQuotes,outputFolder="",writeInFile = False,supressMessages = False):
        ticker = dfQuotes['Ticker'][0]
        outputFolder = os.path.join(outputFolder,"Data/Historical/Indicators")
        dfIndicators = self.GetIndicators(dfQuotes,dfQuotes['Ticker'][0],outputFolder,False,supressMessages)
        dfs = [dfQuotes,dfIndicators]
        dfResult = pd.concat(dfs,axis=1)
        if(writeInFile):
            Util().WriteDataFrame(dfResult,outputFolder,ticker+".csv")
        return dfResult

def main():
    inputFolder = "C:\Users\Augus\Desktop\TesteDonwloader\Data\Historical\Quotes\Normalized"
    outputFolder = "C:\Users\Augus\Desktop\TesteDonwloader\Data\Historical\Indicators"
    indicators = TechnicalIndicators()
    files = Util().GetFilesFromFolder(inputFolder,"csv")
    for file in files:
        df = pd.read_csv(file)
        indicators.GetIndicatorsFromDF(df.copy(),outputFolder,True)

if  __name__ =='__main__': main() 



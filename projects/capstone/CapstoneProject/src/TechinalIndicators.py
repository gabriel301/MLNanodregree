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
    def GetBoillingerBands(self,values,period,std,prefix):
        prefix = prefix+"_"
        print "Calculating Billinger Bands..."
        upperband, middleband, lowerband = talib.BBANDS(values,period,std)
        values = [lowerband,middleband,upperband]
        columns = [prefix+"Lower_BBand",prefix+"Mid_BBand",prefix+"Upper_BBand"]
        df = Util().BuildDataFrame(columns,values).copy()
        return df
    
    #Short Term - 15 days
    #Standard - 30 days
    #Long Term - 60 days
    def GetSMA(self,values,period,prefix):
        prefix = prefix+"_"
        print "Calculating Simple Moving Average..."
        result = talib.SMA(values,period)
        values = [result]
        columns = [prefix+"SMA"]
        df = Util().BuildDataFrame(columns,values).copy()
        return df

    #Short Term - 15 days
    #Standard - 30 days
    #Long Term - 60 days
    def GetEMA(self,values,period,prefix):
        prefix = prefix+"_"      
        print "Calculating Exponential Moving Average..."
        result = talib.EMA(values,period)
        values = [result]
        columns = [prefix+"EMA"]
        df = Util().BuildDataFrame(columns,values).copy()
        return df

    def GetMomentum(self,values,prefix):
        prefix = prefix+"_"
        print "Calculating Momentum..."
        result = talib.MOM(values)
        values = [result]
        columns = [prefix+"MOM"]
        df = Util().BuildDataFrame(columns,values).copy()
        return df

    def GetRSI(self,values,prefix):
        prefix = prefix+"_"
        print "Calculating Relative Strength Index (RSI)..."          
        result = talib.RSI(values)
        values = [result]
        columns = [prefix+"RSI"]
        df = Util().BuildDataFrame(columns,values).copy()
        return df

    #Standard - fastperiod=12, slowperiod=26, signalperiod=9   
    def GetMACD(self,values,prefix):
        prefix = prefix+"_"    
        print "Calculating Moving Average Convergence/Divergence (MACD)..."
        macd, macdsignal, macdhist = talib.MACD(values)
        values = [macd,macdsignal,macdhist]
        columns = [prefix+"MACD",prefix+"MACD_SIGNAL",prefix+"MACD_HIST"]
        df = Util().BuildDataFrame(columns,values).copy()
        return df

      
    def GetStochastic(self,dfQuote,prefix):
        if 'Norm_Adjusted_Close' in dfQuote.columns:
            print "Calculating Sthocastic Indicator..."
            prices = dfQuote['Norm_Adjusted_Close'].tolist()
            slowk, slowd = talib.STOCH(dfQuote['High'].values,dfQuote['Low'].values,values)
            values = [slowk,slowd]
            columns = [prefix+"SLOWK",prefix+"SLOWD"]
            df = Util().BuildDataFrame(columns,values).copy()
        return df

    def GetIndicators(self,values,ticker,outputFolder="",writeInFile = False):
        dfs = []
        dfs.append(self.GetSMA(values,15,"Short"))
        dfs.append(self.GetSMA(values,30,"Middle"))
        dfs.append(self.GetSMA(values,50,"Long"))
        dfs.append(self.GetEMA(values,15,"Short"))
        dfs.append(self.GetEMA(values,30,"Middle"))
        dfs.append(self.GetEMA(values,50,"Long"))
        dfs.append(self.GetMomentum(values,"Std"))
        dfs.append( self.GetRSI(values,"Std"))
        dfs.append(self.GetMACD(values,"Std"))
        #dfs.append(self.GetStochastic(dfQuotes.copy(),"Std"))
        dfs.append(self.GetBoillingerBands(values,10,1.9,"Short"))
        dfs.append(self.GetBoillingerBands(values,20,2,"Middle"))
        dfs.append(self.GetBoillingerBands(values,50,2.1,"Long"))
        dfResult = pd.concat(dfs,axis=1)
        if(writeInFile):
            Util().WriteDataFrame(dfResult,outputFolder,ticker+".csv")
        return dfResult

    def GetIndicatorsFromDF(self,dfQuotes,outputFolder="",writeInFile = False):
        ticker = dfQuotes['Ticker'][0]
        dfIndicators = self.GetIndicators(dfQuotes['Norm_Adjusted_Close'].values,dfQuotes['Ticker'][0],outputFolder,False)
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



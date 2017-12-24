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
    def GetBoillingerBands(self,dfQuote,period,std,prefix):
        prefix = prefix+"_"
        if 'Norm_Adjusted_Close' in dfQuote.columns:
            print "Calculating Billinger Bands..."
            upperband, middleband, lowerband = talib.BBANDS(dfQuote['Norm_Adjusted_Close'].values,period,std)
            values = [lowerband,middleband,upperband]
            columns = [prefix+"Lower_BBand",prefix+"Mid_BBand",prefix+"Upper_BBand"]
            df = Util().BuildDataFrame(columns,values).copy()
        return df
    
    #Short Term - 15 days
    #Standard - 30 days
    #Long Term - 60 days
    def GetSMA(self,dfQuote,period,prefix):
        prefix = prefix+"_"
        if 'Norm_Adjusted_Close' in dfQuote.columns:
            print "Calculating Simple Moving Average..."
            prices = dfQuote['Norm_Adjusted_Close'].tolist()
            result = talib.SMA(dfQuote['Norm_Adjusted_Close'].values,period)
            values = [result]
            columns = [prefix+"SMA"]
            df = Util().BuildDataFrame(columns,values).copy()
        return df

    #Short Term - 15 days
    #Standard - 30 days
    #Long Term - 60 days
    def GetEMA(self,dfQuote,period,prefix):
        prefix = prefix+"_"
        if 'Norm_Adjusted_Close' in dfQuote.columns:
            print "Calculating Exponential Moving Average..."
            prices = dfQuote['Norm_Adjusted_Close'].tolist()
            result = talib.EMA(dfQuote['Norm_Adjusted_Close'].values,period)
            values = [result]
            columns = [prefix+"EMA"]
            df = Util().BuildDataFrame(columns,values).copy()
        return df

    def GetMomentum(self,dfQuote,prefix):
        prefix = prefix+"_"
        if 'Norm_Adjusted_Close' in dfQuote.columns:
            print "Calculating Momentum..."
            prices = dfQuote['Norm_Adjusted_Close'].tolist()
            result = talib.MOM(dfQuote['Norm_Adjusted_Close'].values)
            values = [result]
            columns = [prefix+"MOM"]
            df = Util().BuildDataFrame(columns,values).copy()
        return df

    def GetRSI(self,dfQuote,prefix):
        prefix = prefix+"_"
        if 'Norm_Adjusted_Close' in dfQuote.columns:
            print "Calculating Relative Strength Index (RSI)..."
            prices = dfQuote['Norm_Adjusted_Close'].tolist()
            result = talib.RSI(dfQuote['Norm_Adjusted_Close'].values)
            values = [result]
            columns = [prefix+"RSI"]
            df = Util().BuildDataFrame(columns,values).copy()
        return df

    #Standard - fastperiod=12, slowperiod=26, signalperiod=9   
    def GetMACD(self,dfQuote,prefix):
        prefix = prefix+"_"
        if 'Norm_Adjusted_Close' in dfQuote.columns:
            print "Calculating Moving Average Convergence/Divergence (MACD)..."
            prices = dfQuote['Norm_Adjusted_Close'].tolist()
            macd, macdsignal, macdhist = talib.MACD(dfQuote['Norm_Adjusted_Close'].values)
            values = [macd,macdsignal,macdhist]
            columns = [prefix+"MACD",prefix+"MACD_SIGNAL",prefix+"MACD_HIST"]
            df = Util().BuildDataFrame(columns,values).copy()
        return df

      
    def GetStochastic(self,dfQuote,prefix):
        if 'Norm_Adjusted_Close' in dfQuote.columns:
            print "Calculating Sthocastic Indicator..."
            prices = dfQuote['Norm_Adjusted_Close'].tolist()
            slowk, slowd = talib.STOCH(dfQuote['High'].values,dfQuote['Low'].values,dfQuote['Norm_Adjusted_Close'].values)
            values = [slowk,slowd]
            columns = [prefix+"SLOWK",prefix+"SLOWD"]
            df = Util().BuildDataFrame(columns,values).copy()
        return df

    def GetIndicators(self,dfQuotes,outputFolder="",writeInFile = False):
        dfs = [dfQuotes]
        dfs.append(self.GetSMA(dfQuotes.copy(),15,"Short"))
        dfs.append(self.GetSMA(dfQuotes.copy(),30,"Middle"))
        dfs.append(self.GetSMA(dfQuotes.copy(),50,"Long"))
        dfs.append(self.GetEMA(dfQuotes.copy(),15,"Short"))
        dfs.append(self.GetEMA(dfQuotes.copy(),30,"Middle"))
        dfs.append(self.GetEMA(dfQuotes.copy(),50,"Long"))
        dfs.append(self.GetMomentum(dfQuotes.copy(),"Std"))
        dfs.append( self.GetRSI(dfQuotes.copy(),"Std"))
        dfs.append(self.GetMACD(dfQuotes.copy(),"Std"))
        dfs.append(self.GetStochastic(dfQuotes.copy(),"Std"))
        dfs.append(self.GetBoillingerBands(dfQuotes.copy(),10,1.9,"Short"))
        dfs.append(self.GetBoillingerBands(dfQuotes.copy(),20,2,"Middle"))
        dfs.append(self.GetBoillingerBands(dfQuotes.copy(),50,2.1,"Long"))
        dfResult = pd.concat(dfs,axis=1)
        if(writeInFile):
            Util().WriteDataFrame(dfResult,outputFolder,dfQuotes['Ticker'][0]+".csv")
        return dfResult

def main():
    inputFolder = "C:\Users\Augus\Desktop\TesteDonwloader\Data\Historical\Quotes\Normalized"
    outputFolder = "C:\Users\Augus\Desktop\TesteDonwloader\Data\Historical\Indicators"
    indicators = TechnicalIndicators()
    files = Util().GetFilesFromFolder(inputFolder,"csv")
    for file in files:
        df = pd.read_csv(file)
        indicators.GetIndicators(df,outputFolder,True)

if  __name__ =='__main__': main() 



import pandas as pd
import os 
import ntpath
import csv
import time
import io
import argparse
import math
import numpy as np
import talib

class TechnicalIndicators:
    def GetFilesFromFolder(self,folder,fileExtension):

        fileExtension = fileExtension if fileExtension.find('.') == 0 else "." + fileExtension
        fileExtension = fileExtension.lower()
        print "Getting {} files from {}".format(fileExtension,folder)
        files = [os.path.join(root, name)
             for root, dirs, files in os.walk(folder)
                for name in files
                    if name.lower().endswith(fileExtension)]

        print "{} files found".format(len(files))
        return files
    
    #ShortTerm - 10 days, 1.9 std
    #Standard - 20 days, 2 std
    #LongTerm - 50 days, 2.1 std
    def GetBoillingerBands(self,inputfolder,period,std,prefix,outputfolder):
        files = self.GetFilesFromFolder(inputfolder,'csv')
        print "{} files found".format(len(files))
        path = ""
        for file in files:
            dfQuote = pd.read_csv(file)
            if 'Adjusted_Close' in dfQuote.columns:
                print "Calculating BBands file {}".format(file)
                upperband, middleband, lowerband = np.nan_to_num(talib.BBANDS(dfQuote['Adjusted_Close'].values,period,std))
                self.WriteIndicator(dfQuote,prefix,"Upper_BBand",upperband,file,outputfolder)
                self.WriteIndicator(dfQuote,prefix,"Mid_BBand",middleband,file,outputfolder)
                path = self.WriteIndicator(dfQuote,prefix,"Lower_BBand",lowerband,file,outputfolder)
        return path
    
    #Short Term - 15 days
    #Standard - 30 days
    #Long Term - 60 days
    def GetSMA(self,inputfolder,period,prefix,outputfolder):
        files = self.GetFilesFromFolder(inputfolder,'csv')
        print "{} files found".format(len(files))
        path = ""
        for file in files:
            dfQuote = pd.read_csv(file)
            if 'Adjusted_Close' in dfQuote.columns:
                print "Calculating SMA for file {}".format(file)
                prices = dfQuote['Adjusted_Close'].tolist()
                result = np.nan_to_num(talib.SMA(dfQuote['Adjusted_Close'].values,period))
                path = self.WriteIndicator(dfQuote,prefix,"SMA",result,file,outputfolder)
        return path

    #Short Term - 15 days
    #Standard - 30 days
    #Long Term - 60 days
    def GetEMA(self,inputfolder,period,prefix,outputfolder):
        files = self.GetFilesFromFolder(inputfolder,'csv')
        print "{} files found".format(len(files))
        path = ""
        for file in files:
            dfQuote = pd.read_csv(file)
            if 'Adjusted_Close' in dfQuote.columns:
                print "Calculating EMA for file {}".format(file)
                prices = dfQuote['Adjusted_Close'].tolist()
                result = np.nan_to_num(talib.EMA(dfQuote['Adjusted_Close'].values,period))
                path = self.WriteIndicator(dfQuote,prefix,"EMA",result,file,outputfolder)
        return path

    def GetMomentum(self,inputfolder,prefix,outputfolder):
        files = self.GetFilesFromFolder(inputfolder,'csv')
        print "{} files found".format(len(files))
        path = ""
        for file in files:
            dfQuote = pd.read_csv(file)
            if 'Adjusted_Close' in dfQuote.columns:
                print "Calculating Momentum for file {}".format(file)
                prices = dfQuote['Adjusted_Close'].tolist()
                result = np.nan_to_num(talib.MOM(dfQuote['Adjusted_Close'].values))
                path = self.WriteIndicator(dfQuote,prefix,"MOM",result,file,outputfolder)
        return path

    def GetRSI(self,inputfolder,prefix,outputfolder):
        files = self.GetFilesFromFolder(inputfolder,'csv')
        print "{} files found".format(len(files))
        path = ""
        for file in files:
            dfQuote = pd.read_csv(file)
            if 'Adjusted_Close' in dfQuote.columns:
                print "Calculating Momentum for file {}".format(file)
                prices = dfQuote['Adjusted_Close'].tolist()
                result = np.nan_to_num(talib.RSI(dfQuote['Adjusted_Close'].values))
                path = self.WriteIndicator(dfQuote,prefix,"RSI",result,file,outputfolder)
        return path

    #Standard - fastperiod=12, slowperiod=26, signalperiod=9   
    def GetMACD(self,inputfolder,prefix,outputfolder):
        files = self.GetFilesFromFolder(inputfolder,'csv')
        print "{} files found".format(len(files))
        path = ""
        for file in files:
            dfQuote = pd.read_csv(file)
            if 'Adjusted_Close' in dfQuote.columns:
                print "Calculating MACD for file {}".format(file)
                prices = dfQuote['Adjusted_Close'].tolist()
                macd, macdsignal, macdhist = np.nan_to_num(talib.MACD(dfQuote['Adjusted_Close'].values))
                path = self.WriteIndicator(dfQuote,prefix,"MACD",macd,file,outputfolder)
                path = self.WriteIndicator(dfQuote,prefix,"MACD_SIGNAL",macdsignal,file,outputfolder)
                path = self.WriteIndicator(dfQuote,prefix,"MACD_HIST",macdhist,file,outputfolder)
        return path

      
    def GetStochastic(self,inputfolder,prefix,outputfolder):
        files = self.GetFilesFromFolder(inputfolder,'csv')
        print "{} files found".format(len(files))
        path = ""
        for file in files:
            dfQuote = pd.read_csv(file)
            if 'Adjusted_Close' in dfQuote.columns:
                print "Calculating MACD for file {}".format(file)
                prices = dfQuote['Adjusted_Close'].tolist()
                slowk, slowd = np.nan_to_num(talib.STOCH(dfQuote['High'].values,dfQuote['Low'].values,dfQuote['Adjusted_Close'].values))
                path = self.WriteIndicator(dfQuote,prefix,"STOCH_SLOWK",slowk,file,outputfolder)
                path = self.WriteIndicator(dfQuote,prefix,"STOCH_SLOWD",slowd,file,outputfolder)
               
        return path

    def CreateFolder(self,path):
        if not os.path.exists(path):
            os.makedirs(path)

    ##WriteIndicator
    def WriteIndicator(self,df,prefix,indicator,values,filename,outputfolder):
        self.CreateFolder(outputfolder)
        outputPath = os.path.join(outputfolder,"Data")
        self.CreateFolder(outputPath)
        outputPath = os.path.join(outputPath,"Historical")
        self.CreateFolder(outputPath)
        outputPath = os.path.join(outputPath,"Indicators")
        self.CreateFolder(outputPath)
        outputfileName= str(ntpath.basename(filename))
        outputfolder = os.path.join(outputPath,outputfileName)
        columnName = prefix + "_"+indicator
        print "Writing {} values in {} file...".format(indicator,outputfileName)
        df[columnName] = values
        ##df =  df.apply(pd.to_numeric, errors='ignore')
        df.to_csv(outputfolder,index=False)
        print "Done!"
        return outputPath
def main():
    inputFolder = "C:\Users\Augus\Desktop\TesteDonwloader\Data\Historical\Quotes\Normalized"
    outputFolder = "C:\Users\Augus\Desktop\TesteDonwloader"
    indicators = TechnicalIndicators()
    inputFolder = indicators.GetSMA(inputFolder,15,"Short",outputFolder)
    indicators.GetSMA(inputFolder,30,"Middle",outputFolder)
    indicators.GetSMA(inputFolder,50,"Long",outputFolder)
    indicators.GetEMA(inputFolder,15,"Short",outputFolder)
    indicators.GetEMA(inputFolder,30,"Middle",outputFolder)
    indicators.GetEMA(inputFolder,50,"Long",outputFolder)
    indicators.GetMomentum(inputFolder,"Std",outputFolder)
    indicators.GetRSI(inputFolder,"Std",outputFolder)
    indicators.GetMACD(inputFolder,"Std",outputFolder)
    indicators.GetStochastic(inputFolder,"Std",outputFolder)
    indicators.GetBoillingerBands(inputFolder,10,1.9,"Short",outputFolder)
    indicators.GetBoillingerBands(inputFolder,20,2,"Middle",outputFolder)
    indicators.GetBoillingerBands(inputFolder,50,.1,"Long",outputFolder)

if  __name__ =='__main__': main() 



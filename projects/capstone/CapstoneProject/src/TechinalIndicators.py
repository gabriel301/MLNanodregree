import pandas as pd
import os 
import argparse
import numpy as np
import talib
import ntpath
from Util import Util

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
        files = Util().GetFilesFromFolder(inputfolder,'csv')
        print "{} files found".format(len(files))
        path = ""
        for file in files:
            dfQuote = pd.read_csv(file)
            if 'Norm_Adjusted_Close' in dfQuote.columns:
                print "Calculating BBands file {}".format(file)
                upperband, middleband, lowerband = talib.BBANDS(dfQuote['Norm_Adjusted_Close'].values,period,std)
                self.WriteIndicator(dfQuote,prefix,"Upper_BBand",upperband,file,outputfolder)
                self.WriteIndicator(dfQuote,prefix,"Mid_BBand",middleband,file,outputfolder)
                path = self.WriteIndicator(dfQuote,prefix,"Lower_BBand",lowerband,file,outputfolder)
        return path
    
    #Short Term - 15 days
    #Standard - 30 days
    #Long Term - 60 days
    def GetSMA(self,inputfolder,period,prefix,outputfolder):
        files = Util().GetFilesFromFolder(inputfolder,'csv')
        print "{} files found".format(len(files))
        path = ""
        for file in files:
            dfQuote = pd.read_csv(file)
            if 'Norm_Adjusted_Close' in dfQuote.columns:
                print "Calculating SMA for file {}".format(file)
                prices = dfQuote['Norm_Adjusted_Close'].tolist()
                result = talib.SMA(dfQuote['Norm_Adjusted_Close'].values,period)
                path = self.WriteIndicator(dfQuote,prefix,"SMA",result,file,outputfolder)
        return path

    #Short Term - 15 days
    #Standard - 30 days
    #Long Term - 60 days
    def GetEMA(self,inputfolder,period,prefix,outputfolder):
        files = Util().GetFilesFromFolder(inputfolder,'csv')
        print "{} files found".format(len(files))
        path = ""
        for file in files:
            dfQuote = pd.read_csv(file)
            if 'Norm_Adjusted_Close' in dfQuote.columns:
                print "Calculating EMA for file {}".format(file)
                prices = dfQuote['Norm_Adjusted_Close'].tolist()
                result = talib.EMA(dfQuote['Norm_Adjusted_Close'].values,period)
                path = self.WriteIndicator(dfQuote,prefix,"EMA",result,file,outputfolder)
        return path

    def GetMomentum(self,inputfolder,prefix,outputfolder):
        files = Util().GetFilesFromFolder(inputfolder,'csv')
        print "{} files found".format(len(files))
        path = ""
        for file in files:
            dfQuote = pd.read_csv(file)
            if 'Norm_Adjusted_Close' in dfQuote.columns:
                print "Calculating Momentum for file {}".format(file)
                prices = dfQuote['Norm_Adjusted_Close'].tolist()
                result = talib.MOM(dfQuote['Norm_Adjusted_Close'].values)
                path = self.WriteIndicator(dfQuote,prefix,"MOM",result,file,outputfolder)
        return path

    def GetRSI(self,inputfolder,prefix,outputfolder):
        files = Util().GetFilesFromFolder(inputfolder,'csv')
        print "{} files found".format(len(files))
        path = ""
        for file in files:
            dfQuote = pd.read_csv(file)
            if 'Norm_Adjusted_Close' in dfQuote.columns:
                print "Calculating Momentum for file {}".format(file)
                prices = dfQuote['Norm_Adjusted_Close'].tolist()
                result = talib.RSI(dfQuote['Norm_Adjusted_Close'].values)
                path = self.WriteIndicator(dfQuote,prefix,"RSI",result,file,outputfolder)
        return path

    #Standard - fastperiod=12, slowperiod=26, signalperiod=9   
    def GetMACD(self,inputfolder,prefix,outputfolder):
        files = Util().GetFilesFromFolder(inputfolder,'csv')
        print "{} files found".format(len(files))
        path = ""
        for file in files:
            dfQuote = pd.read_csv(file)
            if 'Norm_Adjusted_Close' in dfQuote.columns:
                print "Calculating MACD for file {}".format(file)
                prices = dfQuote['Norm_Adjusted_Close'].tolist()
                macd, macdsignal, macdhist = talib.MACD(dfQuote['Norm_Adjusted_Close'].values)
                path = self.WriteIndicator(dfQuote,prefix,"MACD",macd,file,outputfolder)
                path = self.WriteIndicator(dfQuote,prefix,"MACD_SIGNAL",macdsignal,file,outputfolder)
                path = self.WriteIndicator(dfQuote,prefix,"MACD_HIST",macdhist,file,outputfolder)
        return path

      
    def GetStochastic(self,inputfolder,prefix,outputfolder):
        files = Util().GetFilesFromFolder(inputfolder,'csv')
        print "{} files found".format(len(files))
        path = ""
        for file in files:
            dfQuote = pd.read_csv(file)
            if 'Norm_Adjusted_Close' in dfQuote.columns:
                print "Calculating MACD for file {}".format(file)
                prices = dfQuote['Norm_Adjusted_Close'].tolist()
                slowk, slowd = talib.STOCH(dfQuote['High'].values,dfQuote['Low'].values,dfQuote['Norm_Adjusted_Close'].values)
                path = self.WriteIndicator(dfQuote,prefix,"STOCH_SLOWK",slowk,file,outputfolder)
                path = self.WriteIndicator(dfQuote,prefix,"STOCH_SLOWD",slowd,file,outputfolder)
               
        return path

    def CreateFolder(self,path):
        if not os.path.exists(path):
            os.makedirs(path)

 
    def WriteIndicator(self,df,prefix,indicator,values,filename,outputfolder):
        Util().CreateFolder(outputfolder)
        outputPath = os.path.join(outputfolder,"Data")
        Util().CreateFolder(outputPath)
        outputPath = os.path.join(outputPath,"Historical")
        Util().CreateFolder(outputPath)
        outputPath = os.path.join(outputPath,"Indicators")
        Util().CreateFolder(outputPath)
        outputfileName= str(ntpath.basename(filename))
        outputfolder = os.path.join(outputPath,outputfileName)
        columnName = prefix + "_"+indicator
        print "Writing {} values in {} file...".format(indicator,outputfileName)
        df[columnName] = values
        df.fillna(method='bfill',inplace=True)
        df.to_csv(outputfolder,index=False)
        print "Done!"
        return outputPath

    def GetIndicators(self,inputFolder,outputFolder):
        inputFolder = self.GetSMA(inputFolder,15,"Short",outputFolder)
        self.GetSMA(inputFolder,30,"Middle",outputFolder)
        self.GetSMA(inputFolder,50,"Long",outputFolder)
        self.GetEMA(inputFolder,15,"Short",outputFolder)
        self.GetEMA(inputFolder,30,"Middle",outputFolder)
        self.GetEMA(inputFolder,50,"Long",outputFolder)
        self.GetMomentum(inputFolder,"Std",outputFolder)
        self.GetRSI(inputFolder,"Std",outputFolder)
        self.GetMACD(inputFolder,"Std",outputFolder)
        self.GetStochastic(inputFolder,"Std",outputFolder)
        self.GetBoillingerBands(inputFolder,10,1.9,"Short",outputFolder)
        self.GetBoillingerBands(inputFolder,20,2,"Middle",outputFolder)
        self.GetBoillingerBands(inputFolder,50,.1,"Long",outputFolder)

def main():
    inputFolder = "C:\Users\Augus\Desktop\TesteDonwloader\Data\Historical\Quotes\Normalized"
    outputFolder = "C:\Users\Augus\Desktop\TesteDonwloader"
    indicators = TechnicalIndicators()

   
    indicators.GetIndicators(inputFolder,outputFolder)

if  __name__ =='__main__': main() 



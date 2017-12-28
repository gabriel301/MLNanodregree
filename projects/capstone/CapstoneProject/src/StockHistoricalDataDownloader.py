# -*- coding: utf-8 -*-
import urllib
import re
import pandas as pd
import os 
import ntpath
import csv
import time
import io
import requests
import argparse
import datetime
import numpy as np
from operator import itemgetter
from Util import Util

class StockHistoricalDataDownloader:
    
    def GetHistoricalDataFromAlphaVantage(self,stockSymbols,outputfolder,identifier,replace):
        total = len(stockSymbols)
        count=1
        apiKey = "2LZWQ360LNACRFVZ"
        outputPath = os.path.join(outputfolder,"Data/Download/Historical/AlphaVantage")
        Util().CreateFolder(outputPath)
        notFoundSymbols = []
        if(identifier):
                identifier = str(identifier) if str(identifier).find('.') == 0 else "." + str(identifier)
                identifier = identifier.upper()
        else:
            identifier = ""

        for symbol in stockSymbols:            
            symbolKey = str(symbol) + str(identifier).upper()
            outputfileName= symbolKey+".csv"
            outputFile = os.path.join(outputPath,outputfileName)
            if not replace:
                if(os.path.exists(outputFile)):
                    print "Skipping Symbol {} because a file already exists".format(symbol)
                    count = count+1
                    continue

            print "Getting data for Symbol {} ({} of {}) from AlphaVantage".format(symbol,str(count),str(total))
            
            url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&outputsize=full&apikey={}&datatype=csv".format(symbolKey,apiKey)
            response = urllib.urlopen(url)
            if(response.headers.type == "application/x-download"):
                file = response.read()        
                df = pd.read_csv(io.StringIO(file.decode('utf-8')))
                cols = df.columns.tolist()
                a, b = cols.index('close'), cols.index('adjusted_close')
                cols[b], cols[a] = cols[a], cols[b]
                df = df[cols]
                df.columns = ['Date','Open','High','Low','Close','Adjusted_Close','Volume','a','b']
                df.drop(axis=1,labels=['a','b'],inplace=True)
                df.replace(0, np.nan,inplace=True)
                df['Ticker'] = symbol
                df = df[['Date','Ticker','Open','High','Low','Close','Adjusted_Close','Volume']]
                print "Writing Info File...\n"
                df.to_csv(outputFile,index=False)
                print "File created at {}\n".format(outputPath)
            else:
                print "Information not found for symbol {}\n".format(symbol)
                notFoundSymbols.append(symbol)
            count = count +1

        outputfileName= "_NotFoundList.csv"
        outputFile = os.path.join(outputPath,outputfileName)
        df2 = pd.DataFrame(notFoundSymbols, columns=["Symbol"])
        print "Writing Not Found Symbols File...\n"
        df2.to_csv(outputFile,index=False)
        print "File created at {}\n".format(outputPath)
        return outputPath

    def GetHistoricalDataFromYahoo(self,stockSymbols,outputfolder,identifier,replace):
        total = len(stockSymbols)
        count=1
        outputPath = os.path.join(outputfolder,"Data/Download/Historical/Yahoo")
        Util().CreateFolder(outputPath)
    
        notFoundSymbols = []
        attemps = 1
        for symbol in stockSymbols:
            if(identifier):
                identifier = str(identifier) if str(identifier).find('.') == 0 else "." + str(identifier)
                identifier = identifier.upper()
            else:
                identifier = ""
            symbolKey = symbol + str(identifier).upper()

            outputfileName= symbolKey+".csv"
            outputFile = os.path.join(outputPath,outputfileName)
            if not replace:
                if(os.path.exists(outputFile)):
                    print "Skipping Symbol {} because a file already exists".format(symbol)
                    count = count +1
                    continue

            while(attemps <= 3):
                print "Getting data for Symbol {} ({} of {}) from Yahoo. Attempt {} of 3 ".format(symbol,str(count),str(total),str(attemps))
                download = self.CallYahooPage(symbolKey)
                if(download.status_code == 200):                       
                    decoded_content = download.content.decode("utf-8")
                    df = pd.read_csv(io.StringIO(decoded_content))
                    df.replace('null', np.nan,inplace=True)
                    df.columns = ['Date','Open','High','Low','Close','Adjusted_Close','Volume']
                    df['Ticker'] = symbol
                    df = df[['Date','Ticker','Open','High','Low','Close','Adjusted_Close','Volume']]
                    print "Writing Info File...\n"
                    df.to_csv(outputFile,index=False)
                    print "File created at {}\n".format(outputPath)
                    break
                elif (download.status_code == 401 and attemps < 3):
                    print "Yahoo Returned code 401. Waiting {} seconds before try again.".format(pow(attemps+1,4))
                    time.sleep(pow(attemps+1,4))
                    attemps = attemps + 1
                else:
                    print "Information not found for symbol {}. HTML Status: {}. Reason: {}\n".format(symbol,download.status_code,download.reason)
                    notFoundSymbols.append([symbol,download.status_code,download.reason])
                    break
            count = count +1
            attemps = 1

        outputfileName= "_NotFoundList.csv"
        outputFile = os.path.join(outputPath,outputfileName)
        df2 = pd.DataFrame(notFoundSymbols, columns=["Symbol","HTML Response Status","Reason"])
        print "Writing Not Found Symbols File...\n"
        df2.to_csv(outputFile,index=False)
        print "File created at {}\n".format(outputPath)
        return outputPath

    def CallYahooPage(self,symbol):
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        symbolKey = str(symbol)  
    
        epoch = int(time.time())
        url = "https://br.financas.yahoo.com/quote/{}/history?period1=0&period2={}&interval=1d&filter=history&frequency=1d".format(symbolKey,epoch)
        s = requests.session()
        html = s.get(url,headers = header).content
        crumbResult = re.search("\"crumb\":\"(.[^{}]*?)\"",html)
        if(crumbResult is not None):
            crumb = unicode(crumbResult.group(1), "utf-8")
        urlD = "https://query1.finance.yahoo.com/v7/finance/download/{}?period1=0&period2={}&interval=1d&events=history&crumb={}".format(symbolKey,epoch,crumb)

        download = s.get(urlD,headers = header)

        return download


    def ReadSymbols(self,filename):
            df = pd.read_csv(filename)
            listSymbols = df.values.T.tolist()
            return listSymbols[0]


    def GetDateInterval(self, stocksFolder,startdate,enddate):
        datesSet = set()
        filesInfo = []
        files = Util().GetFilesFromFolder(stocksFolder,"csv")
        filesInfo = Util().GetFileSizes(files)
        filesInfo = sorted(filesInfo,key=itemgetter(0),reverse = True)
        filesInfo = filesInfo[:5]
        for item in filesInfo:          
                df = pd.read_csv(item[1])
                if 'Date' in df.columns:
                    print "Getting Dates from {}...".format(item[1])
                    datesSet.update((set(df.values.T.tolist()[0])))
        listDates = list(datesSet)
        dt_dates = [datetime.datetime.strptime(date, "%Y-%m-%d") for date in listDates]
        if(startdate):
            dt_dates = [date for date in dt_dates if date >= startdate]
        if(enddate):
            dt_dates = [date for date in dt_dates if date <= enddate]
        listDates = [datetime.datetime.strftime(date, "%Y-%m-%d") for date in dt_dates]
        listDates = sorted(listDates,key=lambda d: map(int, d.split('-')))
        print "{} dates loaded.".format(len(listDates))
        return listDates

    def GetCleanDataframe(self,inputfolder,outputfolder):
        outputPath = os.path.join(outputfolder,"Data/Historical/Quotes/Cleaned")
        Util().CreateFolder(outputPath)
        files = Util().GetFilesFromFolder(inputfolder,'csv')
        total = len(files)
        count = 1
        for stockfile in files:           
            dfHistorical = pd.read_csv(stockfile)
            if 'Date' in dfHistorical.columns:
                print "Cleaning data from file {} ({} of {})".format(stockfile,count,total)
                dfCleaned =  dfHistorical
                dfCleaned.fillna(method='ffill',inplace=True)
                dfCleaned.fillna(method='bfill',inplace=True)
                dfCleaned['date2'] = dfCleaned.Date.astype('datetime64[ns]')
                dfCleaned.sort_values('date2',inplace = True)
                dfCleaned.drop('date2', axis=1, inplace=True)
                outputfileName = str(ntpath.basename(stockfile))
                outputFile = os.path.join(outputPath,outputfileName)
                dfCleaned.to_csv(outputFile,index=False)
                count = count + 1
                print "File created at {}".format(outputFile)
        return outputPath

    #Normalize prices to start from 1
    def GetNormalizedDataframe(self,inputfolder,outputfolder):
        outputPath = os.path.join(outputfolder,"Data/Historical/Quotes/Normalized")
        Util().CreateFolder(outputPath)
        files = Util().GetFilesFromFolder(inputfolder,'csv')
        total = len(files)
        count = 1
        for stockfile in files:           
            dfHistorical = pd.read_csv(stockfile)
            if 'Date' in dfHistorical.columns:
                print "Normalizing data from file {} ({} of {})".format(stockfile,count,total)
                dfHistorical["Norm_High"] = dfHistorical["High"]/dfHistorical["High"][0]
                dfHistorical["Norm_Low"] = dfHistorical["Low"]/dfHistorical["Low"][0]
                dfHistorical["Norm_Adjusted_Close"] = dfHistorical["Adjusted_Close"]/dfHistorical["Adjusted_Close"][0]
                outputfileName = str(ntpath.basename(stockfile))
                outputFile = os.path.join(outputPath,outputfileName)
                dfHistorical.to_csv(outputFile,index=False)
                count = count + 1
                print "File created at {}".format(outputFile)
        return outputPath

    def DownloadData(self,symbols,datasource,identifier,replace,outputfolder):
       
        if(datasource.lower() == 'y' ):
            folderHistorical = self.GetHistoricalDataFromYahoo(symbols,outputfolder,identifier,replace)
        else:
            folderHistorical = self.GetHistoricalDataFromAlphaVantage(symbols,outputfolder,identifier,replace)
    
        quotesFolder = self.GetCleanDataframe(folderHistorical,outputfolder)
        normalizedFolder = self.GetNormalizedDataframe(quotesFolder,outputfolder)

        return normalizedFolder

def main():
    
    epilog = "Sample Usage: symbols outputFolder"
    parser = argparse.ArgumentParser(description='Given Stock Symbols, gets historical stock price data from web for those symbols',
                                     epilog=epilog, add_help=True)

    parser.add_argument('symbols', help='Stock Companies Symbols separeted by comma')
    parser.add_argument('-o','--outputfolder', help='Folder that all historical stock prices will be downloaded.',const='./',
                        default='./',
                        action='store',
                        nargs='?')
    parser.add_argument('-r','--replace', help='Replace files if exists',action="store_true")
    parser.add_argument('-i','--identifier', 
                        help='Exchange identifier. For instance, for Brazilian Exchange Bovespa, the identifier is SA'
                        ,const=None,
                        default=None,
                        action='store',
                        nargs='?')
    parser.add_argument('-s','--startdate', 
                        help='Start date in format yyyy-mm-dd for querying historical data. If not set, data will be queried from 1970-01-01'
                        ,const=None,
                        default=None,
                        action='store',
                        nargs='?')

    parser.add_argument('-e','--enddate', 
                        help='End date in format yyyy-mm-dd for querying historical data. If not set, data will be queried until the current date'
                        ,const=None,
                        default=None,
                        action='store',
                        nargs='?')

    parser.add_argument('-d','--datasource', 
                        help='Source from data to historical data to download. Letter y for Yahoo Finance, a for Alphavantage (default)'
                        ,const='y',
                        default='y',
                        action='store',
                        nargs='?')
    args=parser.parse_args()

    if args.symbols == None:
        print "There are no symbols for querying"
        return
    if(args.identifier):
        args.identifier = args.identifier.upper()
    
    if args.startdate:
       startdate = datetime.datetime.strptime(args.startdate, "%Y-%m-%d")
    else:
        startdate = None

    if args.enddate:
       enddate = datetime.datetime.strptime(args.enddate, "%Y-%m-%d")
    else:
        enddate = None
    
    stocks = StockHistoricalDataDownloader()
    symbols = str(args.symbols).split(",")
    if(args.datasource.lower() == 'y' ):
        folderHistorical = stocks.GetHistoricalDataFromYahoo(symbols,args.outputfolder,args.identifier,args.replace)
    else:
        folderHistorical = stocks.GetHistoricalDataFromAlphaVantage(symbols,args.outputfolder,args.identifier,args.replace)
    
    
    quotesFolder = stocks.GetCleanDataframe(folderHistorical,args.outputfolder)
    normalizedFolder = stocks.GetNormalizedDataframe(quotesFolder,args.outputfolder)
    print "Done!"
if  __name__ =='__main__': main() 

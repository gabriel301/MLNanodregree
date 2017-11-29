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
from operator import itemgetter
import math
import numpy as np
class StockHistoricalData:

    def GetSectorInformationFromYahoo(self,stockSymbols,outputfolder,identifier,replace):
        self.CreateFolder(outputfolder)
        outputPath = os.path.join(outputfolder,"Download")
        self.CreateFolder(outputPath)
        outputPath = os.path.join(outputfolder,"Info")
        self.CreateFolder(outputPath)
        outputPath = os.path.join(outputPath,"Sectors")
        self.CreateFolder(outputPath)
        outputFile = os.path.join(outputPath,"SectorData.csv")
        if not replace:
                if(os.path.exists(outputFile)):
                    print "Skipping file {} because a file already exists".format(outputFile)
                    return outputPath
        
        symbolsInfo = []
        header = ['CODE','COMPANY','SECTOR','INDUSTRY']
        #symbolsInfo.append(header)
        total = len(stockSymbols)
        count=1
        attemps = 1
        if(identifier):
            identifier = str(identifier) if str(identifier).find('.') == 0 else "." + str(identifier)
            identifier = identifier.upper()

        for symbol in stockSymbols:           
            while(attemps <= 3):
                print "Getting Sector Data for Symbol {} ({} of {}). Attempt {} of 3".format(symbol,str(count),str(total),str(attemps))
                symbolKey = str(symbol) + ".SA"
                url = "https://finance.yahoo.com/quote/{}/profile?p={}".format(symbolKey,symbolKey)
                #f = urllib.urlopen(url)
                #htmlPage = f.read()
                s = requests.session()
                try:
                    htmlPage = s.get(url,timeout = 10).content
                except:
                    print "Could not get information for symbol {}. Trying again.".format(symbol)
                    attemps = attemps +1
                sector = re.search("\"sector\":\"(.*?)\"",htmlPage)
                industry = re.search("\"industry\":\"(.*?)\"",htmlPage)
                name = re.search("\"longName\":\"(.*?)\"",htmlPage)
                if(sector is not None and industry is not None):
                    symbolsInfo.append([symbol,unicode(name.group(1), "utf-8"),unicode(sector.group(1), "utf-8"),unicode(industry.group(1), "utf-8")])
                    break;
                elif (attemps < 3):
                    print "Could not get information for symbol {}. Trying again.".format(symbol)
                    attemps = attemps +1
                else:
                    print "Could not get information for symbol {}".format(symbol)
                    symbolsInfo.append([symbol,"","",""])
                    break
            count = count + 1
            attemps = 1
        
        print "Writing Info File...\n"
        df = pd.DataFrame(symbolsInfo, columns=header)
        df.to_csv(outputFile,index=False,encoding='utf-8')
        print "File created at {}\n".format(outputPath)
        return outputPath
    
    def GetHistoricalDataFromAlphaVantage(self,stockSymbols,outputfolder,identifier,replace):
        total = len(stockSymbols)
        count=1
        apiKey = ""
        self.CreateFolder(outputfolder)
        outputPath = os.path.join(outputfolder,"Download")
        self.CreateFolder(outputPath)
        outputPath = os.path.join(outputPath,"Historical")
        self.CreateFolder(outputPath)
        outputPath = os.path.join(outputPath,"AlphaVantage")
        self.CreateFolder(outputPath)
        notFoundSymbols = []
        if(identifier):
                identifier = str(identifier) if str(identifier).find('.') == 0 else "." + str(identifier)
                identifier = identifier.upper()

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
                print "Writing Info File...\n"
                df.to_csv(outputFile,index=False)
                #writer.writerows(file)
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

    def GetFinancialDataFromYahoo (self,symbols,outputfolder,identifier,replace):
        self.CreateFolder(outputfolder)
        outputPath = os.path.join(outputfolder,"Download")
        self.CreateFolder(outputPath)
        outputPath = os.path.join(outputPath,"Financial")
        self.CreateFolder(outputPath)
               
        outputFile = os.path.join(outputPath,"FinancialData.csv")
        if not replace:
                if(os.path.exists(outputFile)):
                    print "Skipping file {} because a file already exists".format(outputFile)
                    return outputPath
        
        if(identifier):
            identifier = str(identifier) if str(identifier).find('.') == 0 else "." + str(identifier)
            identifier = identifier.upper()

        symbols = [str(symbol) + str(identifier).upper() for symbol in symbols]
        symbolQuery = [','.join(symbols)]
        url = "http://finance.yahoo.com/d/quotes.csv?s={}&f=sns6j1ej4".format(symbolQuery)
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        s = requests.session()
        print "Getting Financial Data..."
        download = s.get(url,headers = header)
        decoded_content = download.content.decode("utf-8")
        df = pd.read_csv(io.StringIO(decoded_content))
        df.columns = ['CODE','COMPANY NAME','REVENUE','MARKET CAP','EPS','EBITDA']
        if(identifier):
            df['CODE'] = df['CODE'].str[:-len(identifier)]

        print "Writing Info File...\n"
        df.to_csv(outputFile,index=False)
        print "File created at {}\n".format(outputPath)

        return outputPath

    def GetHistoricalDataFromYahoo(self,stockSymbols,outputfolder,identifier,replace):
        total = len(stockSymbols)
        count=1

        self.CreateFolder(outputfolder)
        outputPath = os.path.join(outputfolder,"Download")
        self.CreateFolder(outputPath)
        outputPath = os.path.join(outputPath,"Historical")
        self.CreateFolder(outputPath)
        outputPath = os.path.join(outputPath,"Yahoo")
        self.CreateFolder(outputPath)
    
        notFoundSymbols = []
        attemps = 1
        for symbol in stockSymbols:
            if(identifier):
                identifier = str(identifier) if str(identifier).find('.') == 0 else "." + str(identifier)
                identifier = identifier.upper()

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

    def CreateFolder(self,path):
        if not os.path.exists(path):
            os.makedirs(path)

    def ReadSymbols(self,filename):
            df = pd.read_csv(filename)
            listSymbols = df.values.T.tolist()
            return listSymbols[0]

    #Get all files in a folder which have a certain extension
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

    def GetFileSizes(self,fileList):
        fileInfo = []
    
        for filename in fileList:
            print "Getting size information from {}...".format(filename)
            size = math.ceil((float(os.path.getsize(filename))/1024))
            fileInfo.append([size,filename])
        return fileInfo

    def GetDateInterval(self, stocksFolder,startdate,enddate):
        datesSet = set()
        filesInfo = []
        #for folder in stocksFolder:
            #files = self.GetFilesFromFolder(folder,"csv")
            #if(len(filesInfo)==0):
                #filesInfo = self.GetFileSizes(files)
            #else:
                #filesInfo.extend(self.GetFileSizes(files))
        files = self.GetFilesFromFolder(stocksFolder,"csv")
        filesInfo = self.GetFileSizes(files)
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

    def GetCleanDataframe(self,intervalDates,inputfolder,outputfolder):
        self.CreateFolder(outputfolder)
        outputPath = os.path.join(outputfolder,"Data")
        self.CreateFolder(outputPath)
        outputPath = os.path.join(outputPath,"Historical")
        self.CreateFolder(outputPath)
        outputPath = os.path.join(outputPath,"Quotes")
        self.CreateFolder(outputPath)
        dfDates = pd.DataFrame(intervalDates,columns = ['Date'])
        files = self.GetFilesFromFolder(inputfolder,'csv')
        total = len(files)
        count = 1
        for stockfile in files:           
            dfHistorical = pd.read_csv(stockfile)
            if 'Date' in dfHistorical.columns:
                print "Clean data from file {} ({} of {})".format(stockfile,count,total)
                dfCleaned = pd.merge(dfDates, dfHistorical, on='Date', how='left')
                dfCleaned.fillna(method='ffill',inplace=True)
                dfCleaned.fillna(method='bfill',inplace=True)
                outputfileName = str(ntpath.basename(stockfile))
                outputFile = os.path.join(outputPath,outputfileName)
                dfCleaned.to_csv(outputFile,index=False)
                count = count + 1
                print "File created at {}".format(outputFile)
        return outputPath

def main():
    
    epilog = "Sample Usage: inputFolder outputFolder"
    parser = argparse.ArgumentParser(description='Given a folder which contains CSV files with Stock Symbols, gets historical stock price data from web for those symbols',
                                     epilog=epilog, add_help=True)

    parser.add_argument('inputfolder', help='Folder that contains all CSV symbols files')
    parser.add_argument('outputfolder', help='Folder that all historical stock prices will be downloaded.')
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
                        ,const='a',
                        default='a',
                        action='store',
                        nargs='?')
    args=parser.parse_args()

    if not os.path.exists(args.inputfolder):
        print "Input Folder does not exist."
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
    
    stocks = StockHistoricalData()
    files = stocks.GetFilesFromFolder(args.inputfolder,"csv")
    for symbolFile in files:
        symbols = stocks.ReadSymbols(symbolFile)
        if(args.datasource.lower() == 'y' ):
            folderHistorical = stocks.GetHistoricalDataFromYahoo(symbols,args.outputfolder,args.identifier,args.replace)
        else:
            folderHistorical = stocks.GetHistoricalDataFromAlphaVantage(symbols,args.outputfolder,args.identifier,args.replace)
        sectorFolder = stocks.GetSectorInformationFromYahoo(symbols,args.outputfolder,args.identifier,args.replace)
        financialFolder= stocks.GetFinancialDataFromYahoo(symbols,args.outputfolder,args.identifier,args.replace)
    
    datesInterval = stocks.GetDateInterval(folderHistorical,startdate,enddate)
    quotesFolder = stocks.GetCleanDataframe(datesInterval,folderHistorical,args.outputfolder)
    #print datesInterval
    print "Done!"
if  __name__ =='__main__': main() 

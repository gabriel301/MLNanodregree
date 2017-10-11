import urllib
import re
import pandas as pd
import os 
import ntpath
import csv
import time
import io
import requests
import datetime

def ReadSymbols(filename):
    df = pd.read_csv(filename)
    listSymbols = df.values.T.tolist()
    return listSymbols[0]

def GetDataFromAlphaVantage(stockSymbols,outputfolder):
    total = len(stockSymbols)
    count=1
    apiKey = "2LZWQ360LNACRFVZ"
    CreateFolder(outputfolder)
    outputPath = os.path.join(outputfolder,"Data")
    CreateFolder(outputPath)
    outputPath = os.path.join(outputPath,"AlphaVantage")
    CreateFolder(outputPath)
    notFoundSymbols = []

    for symbol in stockSymbols:
        print "Getting data for Symbol {} ({} of {}) from AlphaVantage".format(symbol,str(count),str(total))
        symbolKey = str(symbol) + ".SA"
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&outputsize=full&apikey={}&datatype=csv".format(symbolKey,apiKey)
        response = urllib.urlopen(url)
        if(response.headers.type == "application/x-download"):
            file = response.read()
            outputfileName= symbol+".csv"
            outputFile = os.path.join(outputPath,outputfileName)
            df = pd.read_csv(io.StringIO(file.decode('utf-8')))
            cols = df.columns.tolist()
            a, b = cols.index('close'), cols.index('adjusted_close')
            cols[b], cols[a] = cols[a], cols[b]
            df = df[cols]
            df.columns = ['Date','Open','High','Low','Close','Adjusted_Close','Volume','a','b']
            df.drop(axis=1,labels=['a','b'],inplace=True)
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

def GetDataFromYahoo(stockSymbols,outputfolder):
    total = len(stockSymbols)
    count=1

    CreateFolder(outputfolder)
    outputPath = os.path.join(outputfolder,"Data")
    CreateFolder(outputPath)
    outputPath = os.path.join(outputPath,"Yahoo")
    CreateFolder(outputPath)
    
    notFoundSymbols = []
    attemps = 1
    for symbol in stockSymbols:
        while(attemps <= 3):
            print "Getting data for Symbol {} ({} of {}) from Yahoo. Attempt {} of 3 ".format(symbol,str(count),str(total),str(attemps))
            download = CallYahooPage(symbol + ".SA" )
            if(download.status_code == 200):                       
                outputfileName= symbol+".csv"
                outputFile = os.path.join(outputPath,outputfileName)
                decoded_content = download.content.decode("utf-8")
                df = pd.read_csv(io.StringIO(decoded_content))
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

def CallYahooPage(symbol):
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

def CreateFolder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def GetCompaniesSymbolsFromBovespa(fileName,outputfolder):
    print "Reading file {}...\n".format(fileName)
    #Read the file
    df = pd.read_csv(fileName)

    print "Filtering Data...\n"
    #Filters only stock prices of interest
    df = df[(df['BDI CODE'] == 2) & (df['TYPE OF MARKET']==10)]

    #Filters only papers of interest
    specList = ['ON','PN','DRN']
    pattern = '|'.join(specList)
    df = df[df['PAPER SPECIFICATION'].str.contains(pattern)]

    #Replaces all paper types for simpler ones
    for spec in specList:
        df['PAPER SPECIFICATION'] = df['PAPER SPECIFICATION'].apply(lambda x: re.sub('.*'+spec+'.*',spec,x))

    outputfileName= str(ntpath.basename(fileName)).lower().replace(".csv","_filtered.csv")
    CreateFolder(outputfolder)
    outputPath = os.path.join(outputfolder,"Filtered")
    CreateFolder(outputPath)
    outputPath = os.path.join(outputPath,outputfileName)

    print "Writing filtered file"
    df.to_csv(outputPath,index=False)
    print "File created at {}\n".format(outputPath)

    print "Getting Symbols...\n"
    #Get all stock symbols and write into a file
    df2 = df[['PAPER NEGOTIATION CODE','PAPER SPECIFICATION']]
    df2 = df2.groupby(['PAPER NEGOTIATION CODE','PAPER SPECIFICATION']).size().reset_index()
    df2.drop(df2.columns[2],axis=1,inplace=True)
    outputPath = os.path.join(outputfolder,"Symbols")
    CreateFolder(outputPath)
    outputfileName= str(ntpath.basename(fileName)).lower().replace(".csv","_symbols.csv")
    outputPath = os.path.join(outputPath,outputfileName)
    
    print "Writing file...\n"
    df2.to_csv(outputPath,index=False)
    print "File created at {}\n".format(outputPath)
    return outputPath
  
def main():
    input = "C:\\Users\\Augus\\Desktop\\Bovespa\\csv\\cotahist_a2017.csv"
    output = "C:\\Users\\Augus\\Desktop\\BovespaTeste"
    symbolsOutputFile = GetCompaniesSymbolsFromBovespa(input,output)
    symbols = ReadSymbols(symbolsOutputFile)
    GetDataFromYahoo(symbols,output)
    GetDataFromAlphaVantage(symbols,output)


if  __name__ =='__main__': main() 

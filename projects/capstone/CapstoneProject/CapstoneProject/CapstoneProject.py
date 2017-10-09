import urllib
import re
import pandas as pd
import os 
import ntpath
import csv
import time

def ReadSymbols(filename):
    df = pd.read_csv(filename)
    listSymbols = df.values.T.tolist()
    return listSymbols[0]

def GetDataFromAlphaVantage(stockSymbols,outputfolder):
    total = len(stockSymbols)
    count=1
    apiKey = "2LZWQ360LNACRFVZ"
    outputPath = os.path.join(outputfolder,"Data")
    
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
    outputPath = os.path.join(outputPath,"AlphaVantage")
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)

    for symbol in stockSymbols:
        print "Getting data for Symbol {} ({} of {})".format(symbol,str(count),str(total))
        symbolKey = str(symbol) + ".SA"
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&outputsize=full&apikey={}&datatype=csv".format(symbolKey,apiKey)
        response = urllib.urlopen(url)
        if(response.headers.type == "application/x-download"):
            file = response.read()
            outputfileName= symbol+".csv"
            outputFile = os.path.join(outputPath,outputfileName)
            print "Writing Info File...\n"
            f = open(outputFile, "wb")
            f.write(file)
            #writer.writerows(file)
            print "File created at {}\n".format(outputPath)
        else:
            print "Information not found for symbol {}\n".format(symbol)
        count = count +1
def GetHistoricalDataFromAlpha(stocks,outputfolder):
    return

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
    outputPath = os.path.join(outputfolder,"Filtered")
    outputPath = os.path.join(outputPath,outputfileName)
    if not os.path.exists(os.path.dirname(outputPath)):
        os.makedirs(os.path.dirname(outputPath))

    print "Writing filtered file"
    df.to_csv(outputPath,index=False)
    print "File created at {}\n".format(outputPath)

    print "Getting Symbols...\n"
    #Get all stock symbols and write into a file
    df2 = df[['PAPER NEGOTIATION CODE','PAPER SPECIFICATION']]
    df2 = df2.groupby(['PAPER NEGOTIATION CODE','PAPER SPECIFICATION']).size().reset_index()
    df2.drop(df2.columns[2],axis=1,inplace=True)
    outputPath = os.path.join(outputfolder,"Symbols")
    outputfileName= str(ntpath.basename(fileName)).lower().replace(".csv","_symbols.csv")
    outputPath = os.path.join(outputPath,outputfileName)
    if not os.path.exists(os.path.dirname(outputPath)):
        os.makedirs(os.path.dirname(outputPath))
    
    
    print "Writing file...\n"
    df2.to_csv(outputPath,index=False)
    print "File created at {}\n".format(outputPath)
    return outputPath
  
def main():
    input = "C:\\Users\\Augus\\Desktop\\Bovespa\\csv\\cotahist_a2017.csv"
    output = "C:\\Users\\Augus\\Desktop\\Bovespa"
    symbolsOutputFile = GetCompaniesSymbolsFromBovespa(input,output)
    symbols = ReadSymbols(symbolsOutputFile)
    GetDataFromAlphaVantage(symbols,output)


if  __name__ =='__main__': main() 

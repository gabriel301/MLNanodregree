import urllib
import re
import pandas as pd
import os 
import ntpath
import csv
import time

def ReadSymbols(filename):
    df = pd.read_csv(filename,header=None)
    listSymbols = df.values.T.tolist()
    return listSymbols[0]

def GetSectors(stockSymbols,filename,outputfolder):
    symbolsInfo = []
    notFoundInfo = []
    header = ['SYMBOL','SECTOR','INDUSTRY']
    symbolsInfo.append(header)
    total = len(stockSymbols)
    count=1
    for symbol in stockSymbols:
        print "Getting data for Symbol {} ({} of {})".format(symbol,str(count),str(total))
        symbolKey = str(symbol) + ".SA"
        #time.sleep(5)
        url = "https://finance.yahoo.com/quote/{}/profile?p={}".format(symbolKey,symbolKey)
        f = urllib.urlopen(url)
        htmlPage = f.read()
        sector = re.search("\"sector\":\"(.*?)\"",htmlPage)
        industry = re.search("\"industry\":\"(.*?)\"",htmlPage)
        if(sector is not None and industry is not None):
            symbolsInfo.append([symbol,unicode(sector.group(1), "utf-8"),unicode(industry.group(1), "utf-8")])
        else:
            print "Information not found for symbol {}".format(symbol)
            symbolsInfo.append([symbol,"",""])
            #notFoundInfo.append(symbol)
        count = count + 1
        #if(count%10==0):
            #print "Waiting 10 seconds before continue..."
            #time.sleep(20)

    outputfileName= str(ntpath.basename(filename)).lower().replace(".csv","_sectors.csv")
    outputPath = os.path.join(outputfolder,outputfileName)
    print "Writing Info File...\n"
    f = open(outputPath, "wb")
    writer = csv.writer(f)
    writer.writerows(symbolsInfo)
    print "File created at {}\n".format(outputPath)

    #outputfileName= str(ntpath.basename(filename)).lower().replace(".csv","_sectors_notfound.csv")
    #outputPath = os.path.join(outputfolder,outputfileName)
    #print "Writing Not Found Info File...\n"
    #f = open(outputPath, "wb")
    #writer = csv.writer(f)
    #writer.writerows(notFoundInfo)
    #print "File created at {}\n".format(outputPath)

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
    outputPath = os.path.join(outputfolder,outputfileName)
    print "Writing filtered file"
    df.to_csv(outputPath,index=False)
    print "File created at {}\n".format(outputPath)

    print "Getting Symbols...\n"
    #Get all stock symbols and write into a file
    df2 = df[['PAPER NEGOTIATION CODE','PAPER SPECIFICATION']]
    df2 = df2.groupby(['PAPER NEGOTIATION CODE','PAPER SPECIFICATION']).size().reset_index()
    df2.drop(df2.columns[2],axis=1,inplace=True)
    outputfileName= str(ntpath.basename(fileName)).lower().replace(".csv","_symbols.csv")
    outputPath = os.path.join(outputfolder,outputfileName)
    print "Writing file...\n"
    df2.to_csv(outputPath,index=False)
    print "File created at {}\n".format(outputPath)
    return outputPath
  
def main():
    input = "C:\\Users\\Augus\\Desktop\\Bovespa\\csv\\cotahist_a2017.csv"
    output = "C:\\Users\\Augus\\Desktop"
    symbolsOutputFile = GetCompaniesSymbolsFromBovespa(input,output)
    #symbols = ReadSymbols(symbolsOutputFile)
    #GetSectors(symbols,input,output)


if  __name__ =='__main__': main() 

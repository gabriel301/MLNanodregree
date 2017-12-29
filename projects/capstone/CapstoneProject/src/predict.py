# -*- coding: utf-8 -*-
import argparse
import pandas as pd
from TechinalIndicators import TechnicalIndicators
from Util import Util
from StockHistoricalDataDownloader import StockHistoricalDataDownloader
from Model import Model
import datetime
import warnings
import shutil
import os
warnings.filterwarnings("ignore")
def main():
    
    epilog = "Sample Usage: symbols days"
    parser = argparse.ArgumentParser(description='Given Stock Symbols and a number of days, gets historical stock price data from web for those symbols, train and predict their prices',
                                     epilog=epilog, add_help=True)

    parser.add_argument('symbols', help='Stock Companies Symbols separeted by comma')
    parser.add_argument('days', help='How many days ahead to predict')
    
    parser.add_argument('-r','--replace', help='Replace files if exists',action="store_true")
    parser.add_argument('-k','--keepfiles', help='Keep generated files',action="store_true",default = None)
    parser.add_argument('-i','--identifier', 
                        help='Exchange identifier. For instance, for Brazilian Exchange Bovespa, the identifier is SA'
                        ,const=None,
                        default=None,
                        action='store',
                        nargs='?')
    parser.add_argument('-s','--startdate', 
                        help='Start date in format yyyy-mm-dd for querying historical data. If not set, all data available until ENDDATE  will be used to train the model'
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
                        help='Source from data to historical data to download. Letter y for Yahoo Finance (default), letter a for Alphavantage'
                        ,const='y',
                        default='y',
                        action='store',
                        nargs='?')
    parser.add_argument('-o','--outputfolder', help='Folder that all historical stock prices will be downloaded.If not set, current folder will be used'
                        ,const='./',
                        default='./',
                        action='store',
                        nargs='?')
    parser.add_argument('-m','--model', help='Which model use to predict values. Linear, ElasticNet (default), Ridge, Huber, Lasso'
                        ,const='ElasticNet',
                        default='ElasticNet',
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

    models = ['Linear', 'ElasticNet', 'Ridge', 'Huber', 'Lasso']

    if not args.model in models:
        print "This model is not supported. Suppoted models: {}".format(', '.join(models))
        return
    days = int(args.days)

    if days < 1:
        print "Parameter days must be greater than zero."
        return

    symbols = str(args.symbols).split(",")
    downloadFolder = StockHistoricalDataDownloader().DownloadData(symbols,args.datasource,args.identifier,args.replace,args.outputfolder)
    files = Util().GetFilesFromFolder(downloadFolder,"csv")
    dfs = []
    for file in files:
        df = pd.read_csv(file)
        print "Calculating Techinical Indicators for file {}".format(file)
        dfIndicator  = TechnicalIndicators().GetIndicatorsFromDF(df.copy(),args.outputfolder,True,True)
        dfs.append(dfIndicator.copy())
    for dataframe in dfs:
        ticker = dataframe['Ticker'][0]
        prediction = Model().TrainAndPredict(args.model,dataframe,startdate,enddate,days)
        print 'Predicted price for {} in the next {} days: {}'.format(ticker,days,prediction)
    
    #if args.clean:
    
    if not args.keepfiles:
        print "Cleaning files..."
        dataFolder = os.path.join(args.outputfolder,'Data')
        historicalFolder = os.path.join(dataFolder,'Historical')
        downloadFolder = os.path.join(dataFolder,'Download')
        if(os.path.exists(historicalFolder)):
            shutil.rmtree(historicalFolder)
        if(os.path.exists(downloadFolder)):
            shutil.rmtree(downloadFolder)

if  __name__ =='__main__': main() 


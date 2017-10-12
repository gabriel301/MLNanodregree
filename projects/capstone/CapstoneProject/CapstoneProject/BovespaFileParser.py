# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 18:44:36 2017

@author: Augus
"""
import re
import sys
import time
import os 
import ntpath
import argparse
import pandas as pd

class BovespaFileParser:
    def __init__(self):
        self.filename = ""
        self.fileData = []
   
    def progress(self,count, total, status=''):
        self.count = count
        self.total = total
        self.status = status
        bar_len = 60
        filled_len = int(round(bar_len * self.count / float(self.total)))

        percents = round(100.0 * self.count / float(self.total), 1)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)

        sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', self.status))
        sys.stdout.flush() 
        if self.count == self.total:
            print"\n"

    def ParseFolder(self,inputFolder,outputFolder):
        textFiles = self.GetFilesFromFolder(inputFolder,"txt")

        total = len(textFiles)
        count = 1
        self.CreateFolder(outputFolder)
        outputPath = os.path.join(outputFolder,"Parsed")
        self.CreateFolder(outputPath)

        for textFile in textFiles:
            sys.stdout.write("Parsing File %s of %s\n" % (str(count),str(total)))
            
            self.ParseFile(textFile,outputPath)
            count = count+1
          
        return outputPath

    def ParseFile(self,filename,outputFolder):
        sys.stdout.write("Parsing File: %s\n"% (filename))
        self.fileData = open(filename,'r').readlines()
        self.filename = str(ntpath.basename(filename)).lower().replace(".txt",".csv")
        outputFile = os.path.join(outputFolder,self.filename)
        line = self.fileData[0]
        headerchunks = [[0,2],[2,15],[15,23],[23,31]]
        linechunks = [[0,2],[2,10],[10,12],[12,24],[24,27],[27,39],[39,49],[49,52],[52,56],[56,69],[69,82],[82,95],[95,108],
                      [108,121],[121,134],[134,147],[147,152],[152,170],[170,188],[188,201],[201,202],[202,210],[210,217],[217,230],
                      [230,242],[242,245]]
        trailerchunks = [[0,2],[2,15],[15,23],[23,31],[31,42]]

        header = [line[int(headerchunks[i][0]):int(headerchunks[i][1])] for i in xrange(0,len(headerchunks),1)]
        header[3] = re.sub(r'([0-9]{4})([0-9]{2})([0-9]{2})',r'\1-\2-\3',header[3])
        header = [','.join(header)]
        columnNames = ['TYPE OF REGISTER','DATE OF EXCHANGE','BDI CODE','PAPER NEGOTIATION CODE','TYPE OF MARKET',
                       'ABBREVIATED NAME OF THE COMPANY','PAPER SPECIFICATION','FORWARD MARKET TERM IN DAYS',
                       'REFERENCE CURRENCY','MARKET PAPER OPENING FLOOR PRICE','MARKET PAPER HIGHEST FLOOR PRICE',
                       'MARKET PAPER LOWEST FLOOR PRICE', 'MARKET PAPER AVERAGE FLOOR PRICE','MARKET PAPER LAST NEGOTIATED PRICE',
                       'MARKET PAPER BEST PURCHASE OFFER PRICE','MARKET PAPER BEST SALES OFFER PRICE','NUMBER OF TRADES CONDUCTED WITH THE MARKET PAPER',
                       'TOTAL QUANTITY OF TITLES TRADED WITH THIS MARKET PAPER', 'TOTAL VOLUME OF TITLES NEGOTIATED WITH THIS MARKET PAPER',
                       'STRIKE PRICE FOR THE OPTIONS MARKET OR CONTRACT AMOUNT FOR THE SECONDARY FORWARD MARKET', 'STRIKE PRICE OR CONTRACT AMOUNT FOR OPTIONS OR SECONDARY FORWARD MARKETS CORRECTION INDICATOR',
                       'MATURITY DATE FOR OPTIONS OR SECONDARY FORWARD MARKET','PAPER QUOTATION FACTOR','STRIKE PRICE IN POINTS FOR OPTIONS REFERENCED IN US DOLLARS OR CONTRACT AMOUNT IN POINTS FOR SECONDARY FORWARD',
                       'PAPER CODE IN THE IS IN SYSTEM OR PAPER INTERNAL CODE','PAPER DISTRIBUTION NUMBER']
        columnNames = [','.join(columnNames)]
        table = []     
        #table.append(header)
        table.append(columnNames)
        print "Reading File...\n"
        fileSize = int(len(self.fileData))
        self.progress(0,fileSize)  
        #time.sleep(0.1)
        count = 1
        self.progress(1,fileSize,"Reading File")
        for x in xrange(1,len(self.fileData)-1,1):
            line = self.fileData[x]
            data = [line[int(linechunks[i][0]):int(linechunks[i][1])] for i in xrange(0,len(linechunks),1)]
            data =  [x.strip(' ') for x in data]
            data[1] = re.sub(r'([0-9]{4})([0-9]{2})([0-9]{2})',r'\1-\2-\3',data[1])
            formated = ['{0:.2f}'.format(float(re.sub(r'(^[0-9]{11})',r'\1.',data[j]))) for j in xrange(9,16)] 
            data[9:16] = formated
            data[18] = '{0:.2f}'.format(float(re.sub(r'(^[0-9]{16})',r'\1.',data[18])))
            data[19] = '{0:.2f}'.format(float(re.sub(r'(^[0-9]{11})',r'\1.',data[19])))
            data[21] = re.sub(r'([0-9]{4})([0-9]{2})([0-9]{2})',r'\1-\2-\3',data[21])
            data[23] = '{0:.2f}'.format(float(re.sub(r'(^[0-9]{7})',r'\1.',data[23])))
           
            data = [','.join(data)]
            table.append(data)
            self.progress(count+1,fileSize,"Reading File")
            count = count+1
           
        line = self.fileData[len(self.fileData)-1]
        trailer = [line[int(trailerchunks[i][0]):int(trailerchunks[i][1])] for i in xrange(0,len(trailerchunks),1)]
        trailer[3] = re.sub(r'([0-9]{4})([0-9]{2})([0-9]{2})',r'\1-\2-\3',trailer[3])
        trailer = [','.join(trailer)]
        #table.append(trailer)
 
        self.progress(fileSize,fileSize,"Reading File")

        print "Writing File...\n"
        tableSize = int(len(table))
        self.progress(0,tableSize,"Writing File")
        newFile = open(outputFile,'w')  
        count = 0
        for x in xrange(0,len(table),1):
            newFile.writelines(table[x])
            newFile.write("\n")
            self.progress(count+1,tableSize,"Writing File")
            count = count+1
        newFile.close()
        sys.stdout.flush() 
        return outputFile

    def CreateFolder(self,path):
        if not os.path.exists(path):
            os.makedirs(path)       
        
    
    def FilterSymbolsByStockType(self,inputfolder,outputfolder):

        files = self.GetFilesFromFolder(inputfolder,"csv")

        self.CreateFolder(outputfolder)
        outputPath = os.path.join(outputfolder,"Filtered")
        self.CreateFolder(outputPath)
        outputfolder = outputPath
        totalFiles = len(files)
        cont = 1
        for fileName in files:
            print "Filtering file {} of {}".format(cont,totalFiles)
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
            cont = cont +1
        return outputfolder

    def GetSymbolsAndStockType(self,inputfolder,outputfolder):
        
        self.CreateFolder(outputfolder)
        outputPath = os.path.join(outputfolder,"Symbols")
        self.CreateFolder(outputPath)
        outputfolder = outputPath
        files = self.GetFilesFromFolder(inputfolder,"csv")
        totalFiles = len(files)
        cont = 1
        for fileName in files:
            print "Getting Symbols and Stock Types from file {} of {}".format(cont,totalFiles)
            print "Reading file {}...\n".format(fileName)
            df = pd.read_csv(fileName)
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
            cont = cont+1
        return outputfolder

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

def main():
    parser=argparse.ArgumentParser()

    parser.add_argument('--inputfolder', help='Folder that contains all Bovespa Files.')
    parser.add_argument('--outputfolder', help='Folder that all parsed files will be placed.')

    args=parser.parse_args()
    
    if(args.inputfolder == None):
        print "Please specify a valid input folder."
        return
    if(args.outputfolder == None):
        print "Please specify a valid output folder."
        return

    bovespa = BovespaFileParser()

    parsedFolder = bovespa.ParseFolder(args.inputfolder,args.outputfolder)
    filteredFolder =  bovespa.FilterSymbolsByStockType(parsedFolder,args.outputfolder)
    symbolsFolder = bovespa.GetSymbolsAndStockType(filteredFolder,args.outputfolder)
        


if  __name__ =='__main__': main()    
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
import shutil

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

    def ParseFolder(self,inputFolder,outputFolder,merge):
        textFiles = self.GetFilesFromFolder(inputFolder,"txt")

        total = len(textFiles)
        count = 1
        self.CreateFolder(outputFolder)
        outputPath = os.path.join(outputFolder,"Parsed")
        self.CreateFolder(outputPath)
        if(merge == True):
            outputPath = os.path.join(outputPath,"Temp")
            self.CreateFolder(outputPath)    

        for textFile in textFiles:
            sys.stdout.write("Parsing File %s of %s\n" % (str(count),str(total)))           
            self.ParseFile(textFile,outputPath,merge)         
            count = count+1

        return outputPath
        
        

    def ParseFile(self,filename,outputFolder,merge):
        sys.stdout.write("Parsing File: %s\n"% (filename))
        self.fileData = open(filename,'r').readlines()
        self.filename = str(ntpath.basename(filename)).lower().replace(".txt",".csv")
        outputFile = os.path.join(outputFolder,self.filename)
        line = self.fileData[0]
        #This 'chucks' are the size of each columns, in characters. When reading a line, the code splits the line into 
        #these characters intervals in order to separate the data in columns (described in HistoricalQuotations_B3.pdf file)
        headerchunks = [[0,2],[2,15],[15,23],[23,31]]
        linechunks = [[0,2],[2,10],[10,12],[12,24],[24,27],[27,39],[39,49],[49,52],[52,56],[56,69],[69,82],[82,95],[95,108],
                      [108,121],[121,134],[134,147],[147,152],[152,170],[170,188],[188,201],[201,202],[202,210],[210,217],[217,230],
                      [230,242],[242,245]]
        trailerchunks = [[0,2],[2,15],[15,23],[23,31],[31,42]]

        #Split header data in columns
        header = [line[int(headerchunks[i][0]):int(headerchunks[i][1])] for i in xrange(0,len(headerchunks),1)]
        #Format the header date in yyyy-mm-dd format
        header[3] = re.sub(r'([0-9]{4})([0-9]{2})([0-9]{2})',r'\1-\2-\3',header[3])
        #Add commas as delimiters
        header = [','.join(header)]
        #Columns are described in HistoricalQuotations_B3.pdf file
        columnNames = ['TYPE OF REGISTER','DATE OF EXCHANGE','BDI CODE','PAPER NEGOTIATION CODE','TYPE OF MARKET',
                       'ABBREVIATED NAME OF THE COMPANY','PAPER SPECIFICATION','FORWARD MARKET TERM IN DAYS',
                       'REFERENCE CURRENCY','MARKET PAPER OPENING FLOOR PRICE','MARKET PAPER HIGHEST FLOOR PRICE',
                       'MARKET PAPER LOWEST FLOOR PRICE', 'MARKET PAPER AVERAGE FLOOR PRICE','MARKET PAPER LAST NEGOTIATED PRICE',
                       'MARKET PAPER BEST PURCHASE OFFER PRICE','MARKET PAPER BEST SALES OFFER PRICE','NUMBER OF TRADES CONDUCTED WITH THE MARKET PAPER',
                       'TOTAL QUANTITY OF TITLES TRADED WITH THIS MARKET PAPER', 'TOTAL VOLUME OF TITLES NEGOTIATED WITH THIS MARKET PAPER',
                       'STRIKE PRICE FOR THE OPTIONS MARKET OR CONTRACT AMOUNT FOR THE SECONDARY FORWARD MARKET', 'STRIKE PRICE OR CONTRACT AMOUNT FOR OPTIONS OR SECONDARY FORWARD MARKETS CORRECTION INDICATOR',
                       'MATURITY DATE FOR OPTIONS OR SECONDARY FORWARD MARKET','PAPER QUOTATION FACTOR','STRIKE PRICE IN POINTS FOR OPTIONS REFERENCED IN US DOLLARS OR CONTRACT AMOUNT IN POINTS FOR SECONDARY FORWARD',
                       'PAPER CODE IN THE IS IN SYSTEM OR PAPER INTERNAL CODE','PAPER DISTRIBUTION NUMBER']
        
        #Add commas as delimiters of columns names
        columnNames = [','.join(columnNames)]
        #List to store the data from file
        table = []     
        #table.append(header)
        table.append(columnNames)
        print "Reading File...\n"
        fileSize = int(len(self.fileData))

        #Set properties for the progress bar
        self.progress(0,fileSize)  
        #time.sleep(0.1)
        count = 1
        self.progress(1,fileSize,"Reading File")
        #Runs for each line of the file, excepts the header and trailer
        for x in xrange(1,len(self.fileData)-1,1):
            line = self.fileData[x]
            #Splits the data into the chunks intervals
            data = [line[int(linechunks[i][0]):int(linechunks[i][1])] for i in xrange(0,len(linechunks),1)]
            
            #Trim data
            data =  [x.strip(' ') for x in data]

            #Format quote data as yyyy-mm-dd
            data[1] = re.sub(r'([0-9]{4})([0-9]{2})([0-9]{2})',r'\1-\2-\3',data[1])

            #Format data as a float number
            formated = ['{0:.2f}'.format(float(re.sub(r'(^[0-9]{11})',r'\1.',data[j]))) for j in xrange(9,16)] 
            data[9:16] = formated
            data[18] = '{0:.2f}'.format(float(re.sub(r'(^[0-9]{16})',r'\1.',data[18])))
            data[19] = '{0:.2f}'.format(float(re.sub(r'(^[0-9]{11})',r'\1.',data[19])))
            data[21] = re.sub(r'([0-9]{4})([0-9]{2})([0-9]{2})',r'\1-\2-\3',data[21])
            data[23] = '{0:.2f}'.format(float(re.sub(r'(^[0-9]{7})',r'\1.',data[23])))
           
            #Adds commas as delimiters for all columns
            data = [','.join(data)]

            #Inserts the parsed line into the table
            table.append(data)
            self.progress(count+1,fileSize,"Reading File")
            count = count+1
           
        line = self.fileData[len(self.fileData)-1]

        #Parses the trailer in the same way as the header
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

        #Writes all lines into a new csv file
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
        
    
    def FilterSymbolsByStockType(self,inputfolder,outputfolder,merge):

        files = self.GetFilesFromFolder(inputfolder,"csv")

        self.CreateFolder(outputfolder)
        outputPath = os.path.join(outputfolder,"Filtered")
        self.CreateFolder(outputPath)
        if(merge == True):
            outputPath = os.path.join(outputPath,"Temp")
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
            #Filters only stock prices codes of interest
            df = df[(df['BDI CODE'] == 2) & (df['TYPE OF MARKET']==10)]

            #Filters only papers of interest
            specList = ['ON','PN']
            pattern = '|'.join(specList)
            df = df[df['PAPER SPECIFICATION'].str.contains(pattern)]
            
            #Replaces all paper types for simpler ones (EG: PNB -> PN, PN EJ N2 -> PN, ON ED NM -> ON etc)
            for spec in specList:
                df['PAPER SPECIFICATION'] = df['PAPER SPECIFICATION'].apply(lambda x: re.sub('.*'+spec+'.*',spec,x))


            outputfileName= str(ntpath.basename(fileName)).lower().replace(".csv","_filtered.csv")
            
            outputPath = os.path.join(outputfolder,outputfileName)

            print "Writing filtered file"
            df.to_csv(outputPath,index=False)
            print "File created at {}\n".format(outputPath)
            cont = cont +1
        return outputfolder

    def GetSymbolsAndStockType(self,inputfolder,outputfolder,merge):
        
        self.CreateFolder(outputfolder)
        outputPath = os.path.join(outputfolder,"Symbols")
        self.CreateFolder(outputPath)
        if(merge == True):
            outputPath = os.path.join(outputPath,"Temp")
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
            df2 = df[['PAPER NEGOTIATION CODE','ABBREVIATED NAME OF THE COMPANY','PAPER SPECIFICATION']]
            df2 = df2.groupby(['PAPER NEGOTIATION CODE','ABBREVIATED NAME OF THE COMPANY','PAPER SPECIFICATION']).size().reset_index()
            #drops column '0' generated by the group by
            df2.drop(df2.columns[3],axis=1,inplace=True)
        
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

    def MergeFiles(self,inputfolder,outputFolder,outputfilename,tempFiles):
            files = self.GetFilesFromFolder(inputfolder,"csv")
            self.CreateFolder(outputFolder)  
            outputFile = os.path.join(outputFolder,outputfilename)
            if(os.path.exists(outputFile)):
                try:
                    os.remove(outputFile)
                except:
                    print "The existing file {} could not be deleted. Hence, all new content will be appended to this file".format(outputFile)
            total = len(files)
            countFile = 1
            print "Merging files at {}...\n".format(inputfolder)
            for file in files:
                print "Merging file {} ({} of {})".format(file,countFile,total)
                table = open(file,'r').readlines()
                table = filter(None, (line.rstrip('\n') for line in table))
                if(os.path.exists(outputFile)):
                    table.pop(0)

                newFile = open(outputFile,'a')
                tableSize = int(len(table))
                self.progress(0,tableSize,"Writing File")                  
                count = 0
                for x in xrange(0,len(table),1):
                    newFile.writelines(table[x])
                    newFile.write("\n")
                    self.progress(count+1,tableSize,"Writing File")
                    count = count+1
                countFile = countFile + 1
            if(tempFiles != True):
                try:
                    if(os.path.exists(inputfolder)):
                        shutil.rmtree(inputfolder)
                except:
                    print "Could not delete temp folder at {}".format(inputfolder)

    def MergeSymbolFiles(self,inputfolder,outputFolder,outputfilename,tempFiles):
        listSymbols = []
        files = self.GetFilesFromFolder(inputfolder,"csv")
        self.CreateFolder(outputFolder)  
        outputFile = os.path.join(outputFolder,outputfilename)
        if(os.path.exists(outputFile)):
            try:
                os.remove(outputFile)
            except:
                print "The existing file {} could not be deleted. Hence, all new content will be appended to this file".format(outputFile)
        total = len(files)
        countFile = 1
        print "Merging files at {}...\n".format(inputfolder)
        for file in files:
            print "Merging file {} ({} of {})".format(file,countFile,total)
            table = open(file,'r').readlines()
            table = filter(None, (line.rstrip('\n') for line in table))
            if(len(listSymbols)==0):
                listSymbols = table 
            else:
                diff = list(set(table) - set(listSymbols))
                table = diff
                listSymbols.append(table)

            newFile = open(outputFile,'a')
            tableSize = int(len(table))
            self.progress(0,tableSize,"Writing File")                  
            count = 0
            for x in xrange(0,len(table),1):
                newFile.writelines(table[x])
                newFile.write("\n")
                self.progress(count+1,tableSize,"Writing File")
                count = count+1
            countFile = countFile + 1
        if(tempFiles != True):
            try:
                if(os.path.exists(inputfolder)):
                    shutil.rmtree(inputfolder)
            except:
                print "Could not delete temp folder at {}".format(inputfolder)

    def IncludeCompanyInfo(self,inputFolder,InfoFile,outputFolder,merge):
        files = self.GetFilesFromFolder(inputFolder,"csv")
        self.CreateFolder(outputFolder)
        outputPath = os.path.join(outputFolder,"Info")
        self.CreateFolder(outputPath)
        if(merge == True):
            outputPath = os.path.join(outputPath,"Temp")
            self.CreateFolder(outputPath) 
        
        total = len(files)
        countFile = 1
        print "Merging files at {}... with file {}\n".format(inputFolder,InfoFile)
        for symbolFile in files:
            print "Reading symbols file {}...".format(symbolFile)
            dfSymbols= pd.read_csv(symbolFile)

            #Gets only the letters of the ticker. Eg. PETR3 and PETR4 becomes PETR.
            #It is necessary because the info file does not contains the tickers numbers
            dfSymbols['CODE'] = dfSymbols['PAPER NEGOTIATION CODE'].str[:4]
            print "Reading info file {}...".format(InfoFile)

            #Setting the delimiter as semi-collons because the info file contains subsectors and 
            #segments names separeted by commas
            dfInfo = pd.read_csv(InfoFile,delimiter = ';')
            dfInfo.drop('COMPANY',axis=1,inplace=True)
            print "Merging Files..."

            #Merge (inner join) at codes columns 
            dfResult = pd.merge(dfSymbols, dfInfo, on='CODE', how='left')

            #Drops CODE column because there are already the ticker column with almost the same information
            dfResult.drop('CODE',axis=1,inplace=True)
            print "Writing Merged File..."
            outputfileName = str(ntpath.basename(symbolFile)).lower().replace(".csv","_info.csv")
            outputfileName = os.path.join(outputPath,outputfileName)
            dfResult.to_csv(outputfileName,index=False)
            print "File created at {}".format(outputfileName)

        return outputPath


def main():
    
    epilog = "Sample Usage: inputFolder outputFolder"
    parser = argparse.ArgumentParser(description='Parses, Filters and Get Stock Symbols from Bovespa Text Files to CSV Files',
                                     epilog=epilog, add_help=True)

    parser.add_argument('inputfolder', help='Folder that contains all Bovespa Text Files to be parsed.')
    parser.add_argument('outputfolder', help='Folder that all parsed files will be placed.')
    parser.add_argument('-m','--merge', help='Parsed files should be merged into a single file.',action="store_true")
    parser.add_argument('-t','--tempfiles', help='If merge is set, do not remove temp files generated after merging.',action="store_true")
    parser.add_argument('-i','--infofile', 
                        help='When getting symbols, include company information from the specified file in this parameter'
                        ,const=None,
                        default=None,
                        action='store',
                        nargs='?')
    args=parser.parse_args()
   
    if not os.path.exists(args.inputfolder):
        print "Input Folder does not exist."
        return
   
    bovespa = BovespaFileParser()
    outputFolders = []
    symbolFolders = []
    folder = bovespa.ParseFolder(args.inputfolder,args.outputfolder,args.merge)
    outputFolders.append(folder)
    folder =  bovespa.FilterSymbolsByStockType(folder,args.outputfolder,args.merge)
    outputFolders.append(folder)
    folder = bovespa.GetSymbolsAndStockType(folder,args.outputfolder,args.merge)
    symbolFolders.append(folder)

    if(args.infofile):
        folder = bovespa.IncludeCompanyInfo(folder,args.infofile,args.outputfolder,args.merge)
        symbolFolders.append(folder)

    if(args.merge):
        for folder in outputFolders:
            outfolder = os.path.abspath(os.path.join(folder, os.pardir))
            filename = os.path.basename(outfolder) + "_Merged.csv"
            bovespa.MergeFiles(folder,outfolder,filename,args.tempfiles)
        for folder in symbolFolders:
            outfolder = os.path.abspath(os.path.join(folder, os.pardir))
            filename = os.path.basename(outfolder) + "_Merged.csv"
            bovespa.MergeSymbolFiles(folder,outfolder,filename,args.tempfiles)

    print "Done!"
if  __name__ =='__main__': main()    
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

    def ReadFolders(self,inputFolder,outputFolder):
        textFiles = [os.path.join(root, name)
             for root, dirs, files in os.walk(inputFolder)
                for name in files
                    if name.lower().endswith((".txt"))]
        total = len(textFiles)
        count = 1
        for textFile in textFiles:
            sys.stdout.write("File %s of %s\n" % (str(count),str(total)))
            sys.stdout.write("Current File: %s\n"% (textFile))
            #self.filename = textFile
            self.ReadFile(textFile,outputFolder)
            count = count+1
            sys.stdout.flush() 


    def ReadFile(self,filename,outputFolder):
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
        table.append(header)
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
        table.append(trailer)
 
        self.progress(fileSize,fileSize,"Reading File")

        print "Writing File...\n"
        tableSize = int(len(table))
        self.progress(0,tableSize,"Writing File")
        newFile = open(outputFile,'w')  
        count = 0
        for x in xrange(0,len(table),1):
         newFile.writelines(table[x])
         newFile.write("\n")
         #time.sleep(0.1)
         self.progress(count+1,tableSize,"Writing File")
         count = count+1
        newFile.close()

        
        
        
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
    bovespa.ReadFolders(args.inputfolder,args.outputfolder)
    
        


if  __name__ =='__main__': main()    
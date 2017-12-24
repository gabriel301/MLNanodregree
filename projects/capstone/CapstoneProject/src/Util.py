import os 
import ntpath
import math
import datetime
import pandas as pd
from sklearn.model_selection import train_test_split

class Util:

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

    def CreateFolder(self,path):
        if not os.path.exists(path):
            os.makedirs(path)

    def FilterDataFrameByDate(self,df,startdate,enddate):      
        if 'Date' in df.columns:
            datesSet = set()
            print "Filtering Dataframe by Date"
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
            dfDates = pd.DataFrame(listDates,columns = ['Date'])
            dfFiltered = pd.merge(dfDates, df, on='Date', how='left')
            return dfFiltered

    def WritePrediction(self, df, outputfolder,modelname,filename):
        Util().CreateFolder(outputfolder)
        outputPath = os.path.join(outputfolder,"Data")
        Util().CreateFolder(outputPath)
        outputPath = os.path.join(outputPath,"Predictions")
        Util().CreateFolder(outputPath)
        if modelname:
            outputPath = os.path.join(outputPath,modelname)
            Util().CreateFolder(outputPath)
        outputfileName= str(ntpath.basename(filename))
        outputfolder = os.path.join(outputPath,outputfileName)
        print "Writing Predictions..."
        df.to_csv(outputfolder,index=False)
        print "Done!"

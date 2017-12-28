# -*- coding: utf-8 -*-
import os 
import ntpath
import math
import datetime
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

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

    def BuildDataFrame(self,columnNames,values,include_index=False,fillna=True,normalize = False):
        df = pd.DataFrame.from_items(zip(columnNames, values))
        if(fillna):
            df.fillna(method='ffill',inplace=True)
            df.fillna(method='bfill',inplace=True)
        if(normalize):
            df = self.Normalize(df.copy(),columnNames)
        return df

    def WriteDataFrame(self, df, outputfolder,filename,include_index=False):
        Util().CreateFolder(outputfolder)
        outputfileName= str(ntpath.basename(filename))
        outputPath = os.path.join(outputfolder,outputfileName)
        print "Writing Dataframe..."
        df.to_csv(outputPath,index=include_index)
        print "File Created at {}".format(outputPath)

    def Normalize(self, df, columnNames, start = 0, end = 1):
        scale = MinMaxScaler(feature_range=(start, end))
        scaled = scale.fit_transform(df)
        #dict = {'scale': scale.scale_}
        dfResult = pd.DataFrame(scaled,columns = columnNames)
        #dfResult = pd.concat([df,pd.DataFrame(dict)],axis=1)
        return dfResult
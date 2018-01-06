# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import math
from sklearn.metrics import make_scorer
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import TimeSeriesSplit
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression,Ridge,HuberRegressor,Lasso,ElasticNet
from Util import Util
from TechinalIndicators import TechnicalIndicators
import os 
class Model:
  
    def GetTrainPredictData(self,df,featureColumns,targetColumn,trainSize=0.9,recordsToPredict = 1):
       
        dfFeatures = df[featureColumns].shift(-recordsToPredict).dropna() ## Drops last row in order to predict the next price using the previous indicators
        dfTarget = df[targetColumn].shift(recordsToPredict).dropna() #Shift the dataset to "align" with feature datase
        trainRows = int(trainSize*dfFeatures.shape[0])
        X_train = dfFeatures.iloc[0:trainRows,:]
        y_train = dfTarget.iloc[0:trainRows,:]
        X_test = dfFeatures.iloc[trainRows:,:]
        y_test = dfTarget.iloc[trainRows:,:]
        return  X_train, X_test, y_train, y_test

    #Performs grid search for the chosen model
    def fit_model(self,model,params,X, y):

        timeSeriesSplitObj = TimeSeriesSplit(n_splits=10)
        #cv_sets = ShuffleSplit(n_splits = 10, test_size = 0.20, random_state = 0).get_n_splits(X.shape[0])
        #cv_sets = TimeSeriesSplit(n_splits=10).get_n_splits(X.shape[0])
        scoring_fnc = make_scorer(r2_score)

        grid = GridSearchCV(estimator=model,param_grid=params,scoring=scoring_fnc,cv=TimeSeriesSplit(n_splits=10))

        grid = grid.fit(X, y.ravel())

        return grid.best_estimator_,grid.best_params_,grid.best_score_


    def test_model(self,model,X_test,y_test):
        score = model.score(X_test,y_test)
        return score

    def build_params(self):
        models = {}
        models['Linear'] = {'normalize': [True, False],'fit_intercept': [True, False],'n_jobs':[-1]}
        models['Ridge'] = {'alpha': [0.01,0.02,0.0095,0.015], 'normalize': [True, False],'fit_intercept': [True, False], 'random_state':[0]}
        models['Huber'] = {'alpha': [0.01,0.02,0.0095,0.015], 'epsilon': [1.1,1.35,1.5,1.75],'fit_intercept': [False]}
        models['Lasso'] = {'alpha': [0.01,0.02,0.0095,0.015], 'normalize': [True, False],'fit_intercept': [True, False], 'random_state':[0],'selection':['cyclic','random']}
        models['ElasticNet'] = {'alpha': [1.0,1.1, 1.5,1.75], 'normalize': [True, False],'fit_intercept': [True, False], 'random_state':[0],'selection':['cyclic','random'],'l1_ratio':[0.25,0.5,1]}
        
        return models

    def build_models(self,predict = False):
        models = {}
        if not predict:
            models['Linear'] = LinearRegression()
            models['Ridge'] = Ridge()
            models['Huber'] = HuberRegressor()
            models['Lasso'] = Lasso()
            models['ElasticNet'] = ElasticNet()            
        return models

    #Estimar o preço pra T+1 com base em T-N+1 (fazer um shift de um dia no dataframe)
    #Com esse dado, calcular os indicadores e fazer o processo novamente, movendo mais um dia pra frente no dataframe
    #Fazer isso até chegar no dia desejado
    def GetBestEstimatorsShiftStrategy(self,df,recordsToPredict,outputfolder="",writeInFile=True):
        print "Days to Predict: {}".format(recordsToPredict)
        models = self.build_models()
        params = self.build_params()
        scores = {}
        metrics = {}
        featureColumns = list(df.columns.values)
        dfMetrics = pd.DataFrame(columns=['Model','R2 Training Score','R2 Test Score','MSE Train Score','MSE Test Score','Max Relative Error Percentage','Min Relative Error Percentage','Mean Relative Error Percentage','Std Relative Error Percentage','Q1 Relative Error Percentage','Q2 Relative Error Percentage','Q3 Relative Error Percentage','IQR Relative Error Percentage','Params'])
        dfResult = pd.DataFrame(columns=['Date','Actual'])
        X_train, X_test, y_train, y_test = self.GetTrainPredictData(df.copy(),featureColumns,['Norm_Adjusted_Close'],0.8,recordsToPredict)
        dfResult['Actual'] = X_test['Adjusted_Close']
        dfResult['Date'] = X_test['Date']
        featureColumns = featureColumns[11:]
        X_train = X_train[featureColumns]
        X_test = X_test[featureColumns]
        for key in models:
            print "Tuning {} model...".format(key)
            Xtrain, ytrain = X_train, y_train
            b_estimator, b_params, b_score = self.fit_model(models.get(key),params.get(key),Xtrain.values,ytrain.values)
            models[key] = b_estimator
            params[key] = b_params
            scores[key] = b_score                    
            pred = b_estimator.predict(X_test)
            reScaled = pred*df['Adjusted_Close'][0]
            dfResult[key] = reScaled
            dfResult[key + " Relative Error Percentage"] = ((reScaled - dfResult['Actual'].values)/dfResult['Actual'].values)*100
            metrics['Model'] = key
            metrics['R2 Training Score'] = b_estimator.score(X_train.values,y_train.values)
            metrics['R2 Test Score'] = b_estimator.score(X_test.values,y_test)
            metrics['MSE Train Score'] = mean_squared_error(y_train,b_estimator.predict(X_train.values))
            metrics['MSE Test Score'] = mean_squared_error(y_test,pred)
            metrics['Params'] = str(params[key])
            metrics['Max Relative Error Percentage'] = dfResult[key + " Relative Error Percentage"].values.max()
            metrics['Min Relative Error Percentage'] = dfResult[key + " Relative Error Percentage"].values.min()
            metrics['Mean Relative Error Percentage'] = dfResult[key + " Relative Error Percentage"].values.mean()
            metrics['Std Relative Error Percentage'] = dfResult[key + " Relative Error Percentage"].values.std()
            metrics['Q1 Relative Error Percentage'] = dfResult[key + " Relative Error Percentage"].quantile(0.25)
            metrics['Q2 Relative Error Percentage'] = dfResult[key + " Relative Error Percentage"].quantile(0.50)
            metrics['Q3 Relative Error Percentage'] = dfResult[key + " Relative Error Percentage"].quantile(0.75)
            metrics['IQR Relative Error Percentage'] = metrics['Q3 Relative Error Percentage'] - metrics['Q1 Relative Error Percentage']
            dfMetrics = dfMetrics.append(metrics,ignore_index=True)
            print "R2 Training Score {}".format(metrics['R2 Training Score'])
            print "R2 Test Score {}".format(metrics['R2 Test Score'])
            print "MSE Train Score {}".format(metrics['MSE Train Score'])
            print "MSE Test Score {}".format(metrics['MSE Test Score'])

        if(writeInFile):
            Util().WriteDataFrame(dfResult,os.path.join(outputfolder,"Predictions",str(df["Ticker"][0])),str(df["Ticker"][0])+" "+str(recordsToPredict)+" days"+".csv")    
            Util().WriteDataFrame(dfMetrics,os.path.join(outputfolder,"Benchmarks",str(df["Ticker"][0])),"Scores "+str(df["Ticker"][0])+" "+str(recordsToPredict)+" days"+".csv")
        return models, params
    
    def GetBestEstimatorNexDayStrategy(self,df,recordsToPredict=1,outputfolder="",writeInFile=True):
        models,params = Model().GetBestEstimatorsShiftStrategy(df,1,writeInFile=False)
        scores = {}
        metrics = {}
        featureColumns = list(df.columns.values)
        dfMetrics = pd.DataFrame(columns=['Model','R2 Test Score','MSE Test Score','Max Relative Error Percentage','Min Relative Error Percentage','Mean Relative Error Percentage','Std Relative Error Percentage','Q1 Relative Error Percentage','Q2 Relative Error Percentage','Q3 Relative Error Percentage','IQR Relative Error Percentage','Params'])
        dfResult = pd.DataFrame(columns=['Date','Actual'])
        X_train, X_test, y_train, y_test = self.GetTrainPredictData(df.copy(),featureColumns,['Norm_Adjusted_Close'],0.8,1)
        dfResult['Actual'] = (y_test.iloc[:,0]*df['Adjusted_Close'][0]).values[-recordsToPredict:]
        dfResult['Date'] = X_test['Date'].values[-recordsToPredict:]
        featureColumns = featureColumns[9:]
        pricesIndicator = X_test['Norm_Adjusted_Close'].values[-120:] #Get the prices for the last 120 days in order to calculate indicators
        X_train = X_train[featureColumns]
        X_test = X_test[featureColumns]
        y_test = y_test[-recordsToPredict:]
         
        #Predicts for the first day and broadcast the prediction for the other days
        #Tem que ter um numero minimo de dados pra conseguir calcuar os indicadores (pelo menos uns 50 ou 100 registros pra trás)
        for key in models:
            print "Predicting next {} prices using Next Day Strategy for model {} and stock {}".format(dfResult.shape[0],key,df['Ticker'][0])
            #Predicts for the first day and broadcast the prediction for the other days
            model = models[key]
            features = TechnicalIndicators().GetIndicators(pricesIndicator,"")
            predictons = []
            pred = model.predict(features.tail(1))
            pricesIndicator = np.append(pricesIndicator,pred[0])
            pricesIndicator = np.delete(pricesIndicator, [0])
            predictons.append(pred[0])
            for i in range(1,dfResult.shape[0]):
                features = TechnicalIndicators().GetIndicators(pricesIndicator,"")
                pred = model.predict(features.tail(1))
                pricesIndicator = np.append(pricesIndicator,pred[0])
                pricesIndicator = np.delete(pricesIndicator, [0]) 
                predictons.append(pred[0])
            reScaled = np.asarray(predictons)*df['Adjusted_Close'][0]
            dfResult[key] = reScaled
            dfResult[key + " Relative Error Percentage"] = ((reScaled - dfResult['Actual'].values)/dfResult['Actual'].values)*100
            metrics['Model'] = key
            #metrics['R2 Training Score'] = model.score(X_train,y_train)
            metrics['R2 Test Score'] = r2_score(y_test.values,predictons)
            #metrics['MSE Train Score'] = mean_squared_error(y_train,model.predict(X_train))
            metrics['MSE Test Score'] = mean_squared_error(y_test.values,predictons)
            metrics['Params'] = str(params[key])
            metrics['Max Relative Error Percentage'] = dfResult[key + " Relative Error Percentage"].values.max()
            metrics['Min Relative Error Percentage'] = dfResult[key + " Relative Error Percentage"].values.min()
            metrics['Mean Relative Error Percentage'] = dfResult[key + " Relative Error Percentage"].values.mean()
            metrics['Std Relative Error Percentage'] = dfResult[key + " Relative Error Percentage"].values.std()
            metrics['Q1 Relative Error Percentage'] = dfResult[key + " Relative Error Percentage"].quantile(0.25)
            metrics['Q2 Relative Error Percentage'] = dfResult[key + " Relative Error Percentage"].quantile(0.50)
            metrics['Q3 Relative Error Percentage'] = dfResult[key + " Relative Error Percentage"].quantile(0.75)
            metrics['IQR Relative Error Percentage'] = metrics['Q3 Relative Error Percentage'] - metrics['Q1 Relative Error Percentage']
            dfMetrics = dfMetrics.append(metrics,ignore_index=True)
            #print "R2 Training Score {}".format(metrics['R2 Training Score'])
            print "R2 Test Score {}".format(metrics['R2 Test Score'])
            #print "MSE Train Score {}".format(metrics['MSE Train Score'])
            print "MSE Test Score {}".format(metrics['MSE Test Score'])

        if(writeInFile):
            Util().WriteDataFrame(dfResult,outputfolder,str(df["Ticker"][0])+" "+str(recordsToPredict)+" days"+".csv")    
            Util().WriteDataFrame(dfMetrics,outputfolder,"Scores "+str(df["Ticker"][0])+" "+str(recordsToPredict)+" days"+".csv")
        return models, params


    def TrainAndPredict(self,modelName,df,startdate,enddate,periodToPredict):
        print 'Training {} Regressor...'.format(modelName)
        scale = df['Adjusted_Close'][0]
        dfFiltered = Util().FilterDataFrameByDate(df.copy(),startdate,enddate)
        featureColumns = list(df.columns.values)
        featureColumns = featureColumns[9:]
        model = self.build_models().get(modelName)
        params = self.build_params().get(modelName)
        X_train, X_test, y_train, y_test = self.GetTrainPredictData(dfFiltered.copy(),featureColumns,['Norm_Adjusted_Close'],0.8,periodToPredict)
        b_estimator, _ ,_ = self.fit_model(model,params,X_train.values,y_train.values)
        valueToPredict = dfFiltered[featureColumns].iloc[-1].values
        print 'Predicting...'
        prediction = b_estimator.predict(valueToPredict)
        reScaled = prediction * scale
        return reScaled[0]

def main():
    files = Util().GetFilesFromFolder('C:\Users\Augus\Desktop\Data\Indicators\Normalized','csv')
    intervals = [1,7,15,30,60,120]
    for file in files:
        print "File: {}".format(file)
        df = pd.read_csv(file)
        for interval in intervals:
            #Model().GetBestEstimatorNexDayStrategy(df.copy(),interval,'C:\Users\Augus\Desktop\TesteDonwloader\Data\Predictions\Next Day Strategy')
            Model().GetBestEstimatorsShiftStrategy(df.copy(),interval,'C:\Users\Augus\Desktop\Data\Only Normalized Indicators')
            


if  __name__ =='__main__': main() 
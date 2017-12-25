from sklearn.metrics import make_scorer
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression,Ridge,HuberRegressor,Lasso,ElasticNet
from sklearn.neighbors import KNeighborsRegressor
from Util import Util
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.decomposition import PCA
import math
from TechinalIndicators import TechnicalIndicators
class Model:
  
    def GetTrainPredictData(self,df,featureColumns,targetColumn,trainSize=0.8,recordsToPredict = 1):
       
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

        cv_sets = ShuffleSplit(n_splits = 10, test_size = 0.20, random_state = 0).get_n_splits(X.shape[0])
        scoring_fnc = make_scorer(r2_score)

        grid = GridSearchCV(estimator=model,param_grid=params,scoring=scoring_fnc,cv=cv_sets)

        grid = grid.fit(X, y.ravel())

        return grid.best_estimator_,grid.best_params_,grid.best_score_


    def test_model(self,model,X_test,y_test):
        score = model.score(X_test,y_test)
        return score

    def build_params(self):
        models = {}
        models['Linear'] = {'normalize': [True, False],'fit_intercept': [True, False],'n_jobs':[-1]}
        models['Ridge'] = {'alpha': [0.00015,0.0002,0.0001,0.00009], 'normalize': [True, False],'fit_intercept': [True, False], 'random_state':[0]}
        models['Huber'] = {'alpha': [0.01,0.001,0.0001], 'epsilon': [1.1,1.35,1.5],'fit_intercept': [False]}
        models['Lasso'] = {'alpha': [0.00009,0.0002,0.0001,0.00015], 'normalize': [True, False],'fit_intercept': [True, False], 'random_state':[0],'selection':['cyclic','random']}
        models['ElasticNet'] = {'alpha': [1.0,1.1, 1.5], 'normalize': [True, False],'fit_intercept': [True, False], 'random_state':[0],'selection':['cyclic','random'],'l1_ratio':[0.25,0.5,1]}
        models['KNNRegresor'] = {'n_neighbors': [3, 5, 7,10], 'weights': ['uniform', 'distance'],'p': [1, 2], 'n_jobs': [-1],'algorithm': ['ball_tree', 'kd_tree']}
        
        return models

    def build_models(self):
        models = {}
        models['Linear'] = LinearRegression()
        #models['Ridge'] = Ridge()
        #models['Huber'] = HuberRegressor()
        #models['Lasso'] = Lasso()
        #models['ElasticNet'] = ElasticNet()
        #models['KNNRegresor'] = KNeighborsRegressor()
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
        dfMetrics = pd.DataFrame(columns=['Model','R2 Training Score','R2 Test Score','MSE Train Score','MSE Test Score','Max % Diff','Min % Diff','Mean % Diff','Std % Diff','Q1 % Diff','Q2 % Diff','Q3 % Diff','IQR % Diff','Params'])
        dfResult = pd.DataFrame(columns=['Date','Actual'])
        X_train, X_test, y_train, y_test = self.GetTrainPredictData(df.copy(),featureColumns,['Norm_Adjusted_Close'],0.8,recordsToPredict)
        dfResult['Actual'] = X_test['Adjusted_Close']
        dfResult['Date'] = X_test['Date']
        featureColumns = featureColumns[9:]
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
            dfResult[key + " % diff"] = ((reScaled - dfResult['Actual'].values)/dfResult['Actual'].values)*100
            metrics['Model'] = key
            metrics['R2 Training Score'] = b_estimator.score(X_train.values,y_train.values)
            metrics['R2 Test Score'] = b_estimator.score(X_test.values,y_test)
            metrics['MSE Train Score'] = mean_squared_error(y_train,b_estimator.predict(X_train.values))
            metrics['MSE Test Score'] = mean_squared_error(y_test,pred)
            metrics['Params'] = str(params[key])
            metrics['Max % Diff'] = dfResult[key + " % diff"].values.max()
            metrics['Min % Diff'] = dfResult[key + " % diff"].values.min()
            metrics['Mean % Diff'] = dfResult[key + " % diff"].values.mean()
            metrics['Std % Diff'] = dfResult[key + " % diff"].values.std()
            metrics['Q1 % Diff'] = dfResult[key + " % diff"].quantile(0.25)
            metrics['Q2 % Diff'] = dfResult[key + " % diff"].quantile(0.50)
            metrics['Q3 % Diff'] = dfResult[key + " % diff"].quantile(0.75)
            metrics['IQR % Diff'] = metrics['Q3 % Diff'] - metrics['Q1 % Diff']
            dfMetrics = dfMetrics.append(metrics,ignore_index=True)
            print "R2 Training Score {}".format(metrics['R2 Training Score'])
            print "R2 Test Score {}".format(metrics['R2 Test Score'])
            print "MSE Train Score {}".format(metrics['MSE Train Score'])
            print "MSE Test Score {}".format(metrics['MSE Test Score'])

        if(writeInFile):
            Util().WriteDataFrame(dfResult,outputfolder,str(df["Ticker"][0])+" "+str(recordsToPredict)+" days"+".csv")    
            Util().WriteDataFrame(dfMetrics,outputfolder,"Scores "+str(df["Ticker"][0])+" "+str(recordsToPredict)+" days"+".csv")
        return models, params
    
    def GetBestEstimatorNexDayStrategy(self,df,recordsToPredict=1,outputfolder="",writeInFile=True):
        models,params = Model().GetBestEstimatorsShiftStrategy(df,1,writeInFile=False)
        scores = {}
        metrics = {}
        featureColumns = list(df.columns.values)
        dfMetrics = pd.DataFrame(columns=['Model','R2 Test Score','MSE Test Score','Max % Diff','Min % Diff','Mean % Diff','Std % Diff','Q1 % Diff','Q2 % Diff','Q3 % Diff','IQR % Diff','Params'])
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
            print "Predicting next {} prices using Next Day Strategy for model {}".format(dfResult.shape[0],key)
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
            dfResult[key + " % diff"] = ((reScaled - dfResult['Actual'].values)/dfResult['Actual'].values)*100
            metrics['Model'] = key
            #metrics['R2 Training Score'] = model.score(X_train,y_train)
            metrics['R2 Test Score'] = r2_score(y_test.values,predictons)
            #metrics['MSE Train Score'] = mean_squared_error(y_train,model.predict(X_train))
            metrics['MSE Test Score'] = mean_squared_error(y_test.values,predictons)
            metrics['Params'] = str(params[key])
            metrics['Max % Diff'] = dfResult[key + " % diff"].values.max()
            metrics['Min % Diff'] = dfResult[key + " % diff"].values.min()
            metrics['Mean % Diff'] = dfResult[key + " % diff"].values.mean()
            metrics['Std % Diff'] = dfResult[key + " % diff"].values.std()
            metrics['Q1 % Diff'] = dfResult[key + " % diff"].quantile(0.25)
            metrics['Q2 % Diff'] = dfResult[key + " % diff"].quantile(0.50)
            metrics['Q3 % Diff'] = dfResult[key + " % diff"].quantile(0.75)
            metrics['IQR % Diff'] = metrics['Q3 % Diff'] - metrics['Q1 % Diff']
            dfMetrics = dfMetrics.append(metrics,ignore_index=True)
            #print "R2 Training Score {}".format(metrics['R2 Training Score'])
            print "R2 Test Score {}".format(metrics['R2 Test Score'])
            #print "MSE Train Score {}".format(metrics['MSE Train Score'])
            print "MSE Test Score {}".format(metrics['MSE Test Score'])

        if(writeInFile):
            Util().WriteDataFrame(dfResult,outputfolder,str(df["Ticker"][0])+" "+str(recordsToPredict)+" days"+".csv")    
            Util().WriteDataFrame(dfMetrics,outputfolder,"Scores "+str(df["Ticker"][0])+" "+str(recordsToPredict)+" days"+".csv")
        return models, params


    def GetPCs(self,df):
        print "PCA..."
        #Re-Scaling and Normalizing data
        for column in df.columns:
            df[column] = (df[column] - df[column].min())/(df[column].max() - df[column].min())
            df[column] = stats.boxcox(df[column].values + 0.000001)[0]
        pca = PCA(11)
        pca = pca.fit(df,1)
        ratio = pca.explained_variance_ratio_
        variance = pca.explained_variance_
        #float_formatter = lambda x: "%.2f" % x
        #np.set_printoptions(formatter={'float_kind':float_formatter})
        reduced_data = pca.transform(df)
        reduced_df = pd.DataFrame(reduced_data, columns = ['Indicators_PC'])
        
        return reduced_df

def main():
    files = Util().GetFilesFromFolder('C:\Users\Augus\Desktop\TesteDonwloader\Data\Historical\Indicators','csv')
    intervals = [1,7,15,30,60,120]
    for file in files:
        print "File: {}".format(file)
        df = pd.read_csv(file)
        for interval in intervals:
            Model().GetBestEstimatorNexDayStrategy(df.copy(),interval,'C:\Users\Augus\Desktop\TesteDonwloader\Data\Predictions\Next Day Strategy')
            #Model().GetBestEstimatorsShiftStrategy(df.copy(),interval,'C:\Users\Augus\Desktop\TesteDonwloader\Data\Predictions\Shift Strategy')
            


if  __name__ =='__main__': main() 
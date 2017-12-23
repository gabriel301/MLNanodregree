from sklearn.metrics import make_scorer
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression,Ridge,HuberRegressor,Lasso,ElasticNet
from sklearn.neighbors import KNeighborsRegressor,RadiusNeighborsRegressor
from Util import Util
import pandas as pd
import numpy as np

class Model:
    
    def GetTrainPredictData(self,df,trainSize,recordsToPredict):
        #Selecting the features (Only the Techinical Indicators)
        dfDropped = df.drop(df.ix[:,'Date':'Close'].head(0).columns, axis=1)
        dfDropped.drop("Volume",axis=1,inplace = True)
        X_predict = dfDropped.copy()
        X_predict["Adjusted_Close"] =  X_predict["Adjusted_Close"].shift(-recordsToPredict)
        X_train, X_test, y_train, y_test = train_test_split(dfDropped.drop("Adjusted_Close",axis=1).values,dfDropped['Adjusted_Close'].values, train_size=trainSize, random_state = 0)
        return  X_train, X_test, y_train, y_test,X_predict

    #Performs grid search for the chosen model
    def fit_model(self,model,params,X, y):

        cv_sets = ShuffleSplit(n_splits = 10, test_size = 0.20, random_state = 0).get_n_splits(X.shape[0])
        scoring_fnc = make_scorer(r2_score)

        grid = GridSearchCV(estimator=model,param_grid=params,scoring=scoring_fnc,cv=cv_sets)

        grid = grid.fit(X, y)

        return grid.best_estimator_,grid.best_params_,grid.best_score_


    def test_model(self,model,X_test,y_test):
        score = model.score(X_test,y_test)
        return score

    def build_params(self):
        models = {}
        models['Linear'] = {'normalize': [True, False],'fit_intercept': [True, False],'n_jobs':[-1]}
        #models['Ridge'] = {'alpha': [0.1, 0.01,0.001], 'normalize': [True, False],'fit_intercept': [True, False], 'random_state':[0]}
        #models['Huber'] = {'alpha': [0.1, 0.01,0.001], 'epsilon': [1.0,1.35,1.5],'fit_intercept': [True, False]}
        #models['Lasso'] = {'alpha': [0.1, 0.01,0.001], 'normalize': [True, False],'fit_intercept': [True, False], 'random_state':[0],'selection':['cyclic','random']}
        #models['ElasticNet'] = {'alpha': [1.0,0.1, 0.01], 'normalize': [True, False],'fit_intercept': [True, False], 'random_state':[0],'selection':['cyclic','random'],'l1_ratio':[0,0.5,1]}
        #models['KNNRegresor'] = {'n_neighbors': [3, 5, 7,10], 'weights': ['uniform', 'distance'],'p': [1, 2], 'n_jobs': [-1],'algorithm': ['ball_tree', 'kd_tree']}
        #models['RadiusKNNRegresor'] = {'radius': [1.0,0.5,2.0], 'weights': ['uniform', 'distance'],'p': [1, 2], 'n_jobs': [-1],'algorithm': ['ball_tree', 'kd_tree']}
        return models

    def build_models(self):
        models = {}
        models['Linear'] = LinearRegression()
        #models['Ridge'] = Ridge()
        #models['Huber'] = HuberRegressor()
        #models['Lasso'] = Lasso()
        #models['ElasticNet'] = ElasticNet()
        #models['KNNRegresor'] = KNeighborsRegressor()
        #models['RadiusKNNRegresor'] = RadiusNeighborsRegressor()

        return models

    #Estimar o preço pra T+1 com base em T-N+1 (fazer um shift de um dia no dataframe)
    #Com esse dado, calcular os indicadores e fazer o processo novamente, movendo mais um dia pra frente no dataframe
    #Fazer isso até chegar no dia desejado
    def GetBestEstimators(self,df,recordsToPredict):
        models = self.build_models()
        params = self.build_params()
        scores = {}
        X_train, X_test, y_train, y_test, X_predict = self.GetTrainPredictData(df,0.8,recordsToPredict)
        for key in models:
            print "Tuning {} model...".format(key)
            b_estimator, b_params, b_score = self.fit_model(models.get(key),params.get(key),X_train,y_train)
            models[key] = b_estimator
            params[key] = b_params
            scores[key] = b_score
            pred = b_estimator.predict(X_predict)
            print pred


def main():
    file = Util().GetFilesFromFolder('C:\Users\Augus\Desktop\TesteDonwloader\Data\Historical\Indicators','csv')
    df = pd.read_csv(file[0])
    Model().GetBestEstimators(df,1)

if  __name__ =='__main__': main() 
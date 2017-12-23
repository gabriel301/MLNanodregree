from sklearn.metrics import make_scorer
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression,Ridge,HuberRegressor,Lasso,ElasticNet
from sklearn.neighbors import KNeighborsRegressor
from Util import Util
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.decomposition import PCA

class Model:
    
    def GetTrainPredictData(self,df,featureColumns,targetColumn,trainSize=0.8,recordsToPredict = 0):
       
        dfFeatures = df[featureColumns].shift(-recordsToPredict).dropna() ## Drops last row in order to predict the next price using the previous indicators
        dfTarget = df[targetColumn].shift(recordsToPredict).dropna() #Shift the dataset to "align" with feature datase
        X_predict = dfFeatures.copy()
        X_train, X_test, y_train, y_test = train_test_split(dfFeatures.values,dfTarget.values, train_size=trainSize, random_state = 0)
        return  X_train, X_test, y_train, y_test, X_predict

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
        models['Ridge'] = {'alpha': [0.1, 0.01,0.001], 'normalize': [True, False],'fit_intercept': [True, False], 'random_state':[0]}
        models['Huber'] = {'alpha': [0.1, 0.01,0.001], 'epsilon': [1.1,1.35,1.5],'fit_intercept': [False]}
        models['Lasso'] = {'alpha': [0.1, 0.01,0.001], 'normalize': [True, False],'fit_intercept': [True, False], 'random_state':[0],'selection':['cyclic','random']}
        models['ElasticNet'] = {'alpha': [1.0,1.1, 1.5], 'normalize': [True, False],'fit_intercept': [True, False], 'random_state':[0],'selection':['cyclic','random'],'l1_ratio':[0.5,1]}
        models['KNNRegresor'] = {'n_neighbors': [3, 5, 7,10], 'weights': ['uniform', 'distance'],'p': [1, 2], 'n_jobs': [-1],'algorithm': ['ball_tree', 'kd_tree']}
        
        return models

    def build_models(self):
        models = {}
        models['Linear'] = LinearRegression()
        models['Ridge'] = Ridge()
        models['Huber'] = HuberRegressor()
        models['Lasso'] = Lasso()
        models['ElasticNet'] = ElasticNet()
        models['KNNRegresor'] = KNeighborsRegressor()
        return models

    #Estimar o preço pra T+1 com base em T-N+1 (fazer um shift de um dia no dataframe)
    #Com esse dado, calcular os indicadores e fazer o processo novamente, movendo mais um dia pra frente no dataframe
    #Fazer isso até chegar no dia desejado
    def GetBestEstimators(self,df,recordsToPredict):
        models = self.build_models()
        params = self.build_params()
        scores = {}
        featureColumns = list(df.columns.values)
        featureColumns = featureColumns[8:]
        X_train, X_test, y_train, y_test, X_predict = self.GetTrainPredictData(df.copy(),featureColumns,['Adjusted_Close'],0.8,recordsToPredict)
        for key in models:
            print "Tuning {} model...".format(key)
            Xtrain, ytrain = X_train, y_train
            b_estimator, b_params, b_score = self.fit_model(models.get(key),params.get(key),Xtrain,ytrain)
            models[key] = b_estimator
            params[key] = b_params
            scores[key] = b_estimator.score(X_test,y_test)
            pred = b_estimator.predict(X_test)
            print "Prediction: " + str(pred[len(pred)-1] * 6.39371)
            print "Real: " + str(y_test[len(y_test)-1] * 6.39371)
            print "Score: " + str(scores[key])

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
        float_formatter = lambda x: "%.2f" % x
        np.set_printoptions(formatter={'float_kind':float_formatter})
        reduced_data = pca.transform(df)
        reduced_df = pd.DataFrame(reduced_data, columns = ['Indicators_PC'])
        
        return reduced_df

def main():
    file = Util().GetFilesFromFolder('C:\Users\Augus\Desktop\TesteDonwloader\Data\Historical\Indicators','csv')
    df = pd.read_csv(file[0])
    Model().GetBestEstimators(df,1)


if  __name__ =='__main__': main() 
import numpy as np
import pandas as pd
from sklearn import cross_validation
from sklearn.grid_search import GridSearchCV
from sklearn import tree
from sklearn import ensemble
from sklearn import svm
from datetime import datetime
from sklearn import linear_model
from sklearn.kernel_ridge import KernelRidge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.neighbors import KNeighborsRegressor
import data as stock


class trainer:
	def __init__(self, ticker):
		self.data = None
		self.ticker = ticker
		self.clf = None
		self.clf_score = None

	def training(self,start_date,end_date):
		data = stock.getData(self.ticker,start_date,end_date,"default","default")
		data.drop(['Close','Low'], axis = 1, inplace = True)
		self.data = data
		# dates = self.data.index.values
		# delta = datetime.strptime("2010-01-01", "%Y-%m-%d")
		# X = [datetime.strptime(str(date), "%Y-%m-%d 00:00:00") for date in self.data.index]
		# X = [(date-delta).days for date in X]
		# X = pd.DataFrame(X,index=[x for x in self.data.index],columns=['days'])
		X = self.data[self.data.columns[:-1]]
		Y = self.data[self.data.columns[-1]]
		X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, Y, test_size=0.25, random_state=0)
		clf = ensemble.AdaBoostRegressor(tree.DecisionTreeRegressor(max_depth = 50),random_state=0,n_estimators=50)
		parameters = {'base_estimator__max_depth': (5,10,20,50),'n_estimators':(5,10,20,50),'learning_rate':(0.5,0.8,1)}
		grid_obj = GridSearchCV(clf,parameters)
		grid_obj = grid_obj.fit(X_train,y_train)
		clf = grid_obj.best_estimator_
		print grid_obj.best_estimator_
		clf.fit(X_train, y_train)
		self.clf_score = clf.score(X_test,y_test)
		self.clf = clf
		return clf

	def getClf(self):
		return self.clf

	def getClf_score(self):
		return self.clf_score

class predictor:
	def __init__(self, ticker, clf):
		self.ticker = ticker
		self.clf = clf
		self.pred_result = None

	def predicting(self,dates):
		datas = [0] * len(dates)
		data = stock.getData(self.ticker,'2010-01-01','2020-12-31',"default","default")
		for i, date in enumerate(dates):
			temp = data.ix[date]
			datas[i] = [temp[0],temp[1],temp[4]]
		predicts = self.clf.predict(datas)
		self.pred_result = predicts
		return predicts

	def getPred_result(self):
		return self.pred_result
import numpy as np
import pandas as pd
from sklearn import cross_validation
from sklearn.grid_search import GridSearchCV
from sklearn import tree
from sklearn import ensemble

class trainer:
	def __init__(self, ticker, data):
		self.data = data
		self.ticker = ticker
		self.clf_list = None

	def training(self):
		feature_cols = self.data.columns[0]
		target_cols = list(self.data.columns[0:])
		dates = self.data.index.values
		X = [0 for x in dates]
		for i, x in enumerate(self.data.index):
			X[i] = str(x).split('-')
			X[i][2] = X[i][2][0] + X[i][2][1]
			for j in range(3):
				X[i][j] = int(X[i][j])
		X = pd.DataFrame(X,index=[x for x in self.data.index],columns=['year','month','day'])
		clf_list = [0 for x in self.data.columns]
		for i, x in enumerate(self.data.columns):
			Y = self.data[self.data.columns[i]]
			X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, Y, test_size=0.2, random_state=0)
			clf = ensemble.AdaBoostRegressor(tree.DecisionTreeRegressor(max_depth=100),random_state=0,n_estimators=100)
			clf.fit(X_train, y_train)
			print clf.score(X_test,y_test)
			clf.fit(X,Y)
			clf_list[i] = clf
		# parameters = {'n_estimators': (1,100),'base_estimator__max_depth': (1,100)}
		# grid_obj = GridSearchCV(clf,parameters)
		# grid_obj = grid_obj.fit(X_train,y_train)
		# clf = grid_obj.best_estimator_
		# clf.fit(X_train, y_train)
		# print clf.score(X_test,y_test)
		self.clf_list = clf_list
		return clf_list
	def getClf_list(self):
		return self.clf_list

class predictor:
	def __init__(self, ticker, clf_list):
		self.ticker = ticker
		self.clf_list = clf_list
		self.pred_result = None

	def predicting(self,dates):
		predicts = []
		for clf in self.clf_list:
			predict = clf.predict(dates)
			print predict
			predicts.append(predict)
		self.pred_result = predicts
		return predicts
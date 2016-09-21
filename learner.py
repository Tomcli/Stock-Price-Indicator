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
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib
from collections import Counter
import data as stock


class trainer:
	def __init__(self, ticker):
		self.data = None
		self.ticker = ticker
		self.clf = None
		self.clf_score = None

	def training(self,start_date,end_date,best_est,graph,data_pre):
		data = stock.getData(self.ticker,start_date,end_date,"default","default")
		if start_date.replace(' ','') == 'default':
			data = data.tail(600)
		adj_close = data['Adjusted Close']
		data.drop(['Close','Low'], axis = 1, inplace = True)
		if not data_pre == 'off':
			data = self.data_preprocessing(data)
		else:
			print 'Warning: Data preprocessing is off.'
		self.data = data
		X = self.data[self.data.columns[:-1]]
		Y = self.data[self.data.columns[-1]]
		X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, Y, test_size=0.25, random_state=0)
		clf = ensemble.BaggingRegressor(tree.DecisionTreeRegressor(max_depth = 50),random_state=0,n_estimators=50)
		parameters = {'base_estimator__max_depth': (5,10,20,50),'n_estimators':(5,10,20,50)}#,'learning_rate':(0.5,0.8,1)
		grid_obj = GridSearchCV(clf,parameters)
		grid_obj = grid_obj.fit(X_train,y_train)
		clf = grid_obj.best_estimator_
		if best_est == 'on':
			print grid_obj.best_estimator_
		clf.fit(X_train, y_train)
		self.clf_score = clf.score(X_test,y_test)
		self.clf = clf
		if graph == 'on': #show plot if the estimated graph condition is on
			plot = plt.figure()
			matplotlib.style.use('ggplot')
			regressor = clf.predict(X)
			#reference from sklearn: http://scikit-learn.org/stable/auto_examples/ensemble/plot_adaboost_regression.html
			plt1, = plt.plot(adj_close, c = 'r', label = 'Actual adjusted close') 
			plt2, = plt.plot(data.index, regressor, c = 'g' , label = "Predicted adjusted close")
			plt.xlabel("Date")
			plt.ylabel("Adjusted close")
			plt.title("Adjusted close for " + self.ticker)
			r2 = mpatches.Patch(label='R2 score: {:.4f}'.format(self.clf_score)) #reference from matplotlib legend guide
			plt.legend(handles = [r2,plt1,plt2]) 
			plt.show()
			plt.close(plot)
		return clf

	def getClf(self):
		return self.clf

	def getClf_score(self):
		return self.clf_score

	def data_preprocessing(self, data):
		# log_data = data
		non_outliers = []
		#print log_data.shape
		data['difference'] = data['Open'] - data['Adjusted Close']
		#print data.shape
		#for feature in data.keys(): #code from previous assignment.
			# if feature == 'Volume':
			# 	continue
		Q1 = np.percentile(data['difference'],25)
		Q3 = np.percentile(data['difference'],75)
		step = 1.5*(Q3 - Q1)
		data = data[((data['difference'] >= Q1 - step) & (data['difference'] <= Q3 + step))] #exclude all the outliers from the data
		# m = non_outliers[3]
		# for i in range(3):
		# 	m = m.merge(non_outliers[i])
		#print log_data.shape
		#data = np.exp(log_data)
		#print data[data.columns[:4]].shape
		return data[data.columns[:4]]

class predictor:
	def __init__(self, ticker, clf):
		self.ticker = ticker
		self.clf = clf
		self.pred_result = None
		self.act_result = None

	def predicting(self,dates):
		datas = [0] * len(dates)
		result = []
		data = stock.getData(self.ticker,'default','default',"default","default")
		for i, date in enumerate(dates):
			temp = data.ix[date]
			datas[i] = [temp[0],temp[1],temp[4]]
			result.append(temp[5])
		predicts = self.clf.predict(datas)
		self.pred_result = predicts
		self.act_result = result
		return predicts

	def pred_curr(self,inputs):
		predict = self.clf.predict([inputs])
		return predict

	def getPred_result(self):
		return self.pred_result

	def getAct_result(self):
		return self.act_result

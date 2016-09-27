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
		self.clf = None #Trained regressor
		self.clf_score = None #Regressor R2 score

	def training(self,start_date,end_date,best_est,graph,data_pre):
		"""
		Train the data based on the given parameters. Plot graph and show best estimator if the user is ask for.
		Most of the commented codes are for testing. Please ignore or delete them.
		"""
		#Query and preprocess the data
		data = stock.getData(self.ticker,start_date,end_date,"default","default") #query the data
		# if start_date.replace(' ','') == 'default':
		data.drop(['Close','Low'], axis = 1, inplace = True) #drop the two unnecessary features
		data = data.tail(600) #In general, 600 samples is the best for bagging regressor.
		datas = []
		# for i in range(1,11):
		# 	datas.append(data.tail(i*200))
		if not data_pre == 'off':
			data = self.data_preprocessing(data)
			# for i, da in enumerate(datas): #testing code for refinement
			# 	datas[i] = self.data_preprocessing(da)
		else: #don't preprocess the data if Data preprocessing is off
			print 'Warning: Data preprocessing is off.'
		adj_close = data['Adjusted Close']
		self.data = data
		#clfs = []
		#for i, da in enumerate(datas):
		#Choose training and testing set using Cross-validation
		X = self.data[self.data.columns[:-1]]
		Y = self.data[self.data.columns[-1]]
		X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, Y, test_size=0.25, random_state=0)
		clf = ensemble.BaggingRegressor(tree.DecisionTreeRegressor(max_depth = 50),random_state=0,n_estimators=50)
		#clf = ensemble.BaggingRegressor(KNeighborsRegressor(n_neighbors=10),random_state=0,n_estimators=50)
		#Tune parameters using grid search
		parameters = {'base_estimator__max_depth': (5,10,20,50),'n_estimators':(5,10,20,50)}
		#parameters = {'base_estimator__n_neighbors': (3,5,8,10,15),'n_estimators':(5,10,20,50)}
		grid_obj = GridSearchCV(clf,parameters)
		grid_obj = grid_obj.fit(X_train,y_train)
		clf = grid_obj.best_estimator_
		if best_est == 'on': #if Show best_estimator is on, print out the best estimator
			print grid_obj.best_estimator_
		clf.fit(X_train, y_train)
		self.clf_score = clf.score(X_test,y_test) #Store R2 score
		#print "Error rate for {}: {:.4f}% with {} data(DC)".format(self.ticker,(1 - self.clf_score) * 100, (i+1)*200)
		self.clf = clf
		#clfs.append(clf)

		if graph == 'on': #show plot if show estimated graph condition is on
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

		#Testing code: plots for Exploratory Visualization
		#plot = plt.figure()
		# plt.plot(adj_close, self.data['Open'],'ro', c = 'r', label = 'Open price for ' + self.ticker) 
		# plt.plot(adj_close, self.data['High'],'ro',c = 'g', label = 'Highest price for ' + self.ticker) 
		# plt.plot(adj_close, self.data['Volume'], 'ro', c = 'k', label = 'Volume for ' + self.ticker) 
		# plt.xlabel("Adjusted close price for " + self.ticker)
		# plt.ylabel("Open and highest price for " + self.ticker)
		# plt.legend()
		# plt.show()
		# plt.close(plot)

		return clf

	def getClf(self):
		return self.clf

	def getClf_score(self):
		return self.clf_score

	def data_preprocessing(self, data):
		"""
		Preprocess the data based on the difference of the open price and adjusted close price.
		"""
		non_outliers = []
		data['difference'] = data['Open'] - data['Adjusted Close']
		#Calculate outliers using interquartile range
		Q1 = np.percentile(data['difference'],25)
		Q3 = np.percentile(data['difference'],75)
		step = 1.5*(Q3 - Q1)
		data = data[((data['difference'] >= Q1 - step) & (data['difference'] <= Q3 + step))] #exclude all the outliers from the data
		return data[data.columns[:4]]

class predictor:
	def __init__(self, ticker, clf):
		self.ticker = ticker
		self.clf = clf #Train Regressor
		self.pred_result = None
		self.act_result = None

	def predicting(self,dates):
		"""
		Make a prediction based on the given dates.
		"""
		datas = [0] * len(dates)
		result = []
		data = stock.getData(self.ticker,'default','default',"default","default") #query all the possible data from quandl
		for i, date in enumerate(dates): #for all the given dates, get their open, high, and volume and make predictions with the regressor
			temp = data.ix[date]
			datas[i] = [temp[0],temp[1],temp[4]]
			result.append(temp[5])
		predicts = self.clf.predict(datas)
		self.pred_result = predicts #Store the array with all the predictions to self.pred_result
		self.act_result = result #Store the array with all the actual results to self.act_result for comparison
		return predicts

	def pred_curr(self,inputs):
		"""
		Make a prediction based on the given values for each feature.
		"""
		predict = self.clf.predict([inputs])
		return predict

	def getPred_result(self):
		return self.pred_result

	def getAct_result(self):
		return self.act_result

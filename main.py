import numpy as np
import pandas as pd
from sklearn import tree
from sklearn import ensemble
from IPython.display import display # Allows the use of display() for DataFrames
import matplotlib.pyplot as plt
import matplotlib
import data as stock
from parse import *
from sklearn import cross_validation
from sklearn.metrics import f1_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import make_scorer

class training:
	def __init__(self,data):
		self.data = data

	def train(self):
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
		Y = self.data[self.data.columns[0]]
		X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, Y, test_size=0.25, random_state=0)
		clf = ensemble.BaggingRegressor(tree.DecisionTreeRegressor(max_depth=100),random_state=0,n_estimators=100)
		clf.fit(X_train, y_train)
		print clf.score(X_test,y_test)
		# parameters = {'n_estimators': (1,100),'base_estimator__max_depth': (1,100)}
		# grid_obj = GridSearchCV(clf,parameters)
		# grid_obj = grid_obj.fit(X_train,y_train)
		# clf = grid_obj.best_estimator_
		# clf.fit(X_train, y_train)
		# print clf.score(X_test,y_test)



def run():
	file = open("input.txt", "r")
	inputs = file.read()
	ticker = search('Ticker symbols:{}\n',inputs)
	start_date = search('Start_date:{}\n',inputs)
	end_date = search('End_date:{}\n',inputs)
	tickers = ticker[0].split(",") #put all the ticker symbols into a list
	tickers = [tick.replace(' ','') for tick in tickers] #remove all the spaces for ticker symbols
	data = []
	for tick in tickers:
		print "This is the data for " + tick
		data = stock.getData(tick,start_date[0],end_date[0],"default","default")
		#print data
	train = training(data)
	train.train()
	file.close()
	

if __name__ == '__main__':
    run()
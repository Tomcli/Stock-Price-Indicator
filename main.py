import numpy as np
import pandas as pd
from IPython.display import display # Allows the use of display() for DataFrames
import matplotlib.pyplot as plt
import matplotlib
import data as stock
import learner
from parse import *
from datetime import datetime

def run():
	file = open("input.txt", "r")
	inputs = file.read()
	#parsing
	ticker = search('Ticker symbols:{}\n',inputs)
	tickers = ticker[0].split(",") #put all the ticker symbols into a list
	tickers = [tick.replace(' ','') for tick in tickers] #remove all the spaces for ticker symbols
	start_date = search('Start_date:{}\n',inputs)
	end_date = search('End_date:{}\n',inputs)
	pred_date = search('Predict_date:{}\n',inputs)
	pred_dates = pred_date[0].split(",")
	pred_dates = [date.replace(' ','') for date in pred_dates]
	#training and predicting
	trainers = [0] * len(tickers)
	predictors = [0] * len(tickers)
	recent = [[741.86,742.0,2980700],[732.01,737.75,1594900],[762.89,773.8,1305100]]
	for i, tick in enumerate(tickers):
		print "This is the data for " + tick
		#target_data = data.shift(-1, freq='B')
		#data = data.ix[1:]
		#target_data = target_data[:-1]
		trainers[i] = learner.trainer(tick)
		trainers[i].training(start_date[0],end_date[0])
		print trainers[i].getClf_score()
		print 'predict'
		predictors[i] = learner.predictor(tick, trainers[i].getClf())
		results = predictors[i].predicting(pred_dates)
		for (i,), result in np.ndenumerate(results):
			print 'predicted adjusted close value for {} is {:.4f}'.format(pred_dates[i], result)
		print " "
	file.close()
	

if __name__ == '__main__':
    run()
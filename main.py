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
	dev_mode = search('Developer Mode:{}\n',inputs)
	ticker = search('Ticker symbols:{}\n',inputs)
	tickers = ticker[0].split(",") #put all the ticker symbols into a list
	tickers = [tick.replace(' ','') for tick in tickers] #remove all the spaces for ticker symbols
	start_date = search('Start_date:{}\n',inputs)
	end_date = search('End_date:{}\n',inputs)
	pred_date = search('Predict_date:{}\n',inputs)
	pred_dates = pred_date[0].split(",")
	pred_dates = [date.replace(' ','') for date in pred_dates]
	# pred_value = search('Predict_value:{}\n',inputs)  #These 7 lines of code are debugging code for parsing pred_value
	# pred_values = pred_value[0].split(";")			#pred_value are used for testing by putting your own open, high, and volume
	# pred_values_ = []
	# for values in pred_values:
	# 	temp = search('({:f},{:f},{:d})',values)
	# 	pred_values_.append([temp[x] for x in range(3)])
	# print pred_values_
	if dev_mode[0] == 'True':
		start_date = start_date[0]
		end_date = end_date[0]
	else:
		start_date = 'default'
		end_date = 'default'
	#training and predicting
	trainers = [0] * len(tickers)
	predictors = [0] * len(tickers)
	for i, tick in enumerate(tickers):
		print "This is the data for " + tick
		trainers[i] = learner.trainer(tick)
		trainers[i].training(start_date,end_date)
		print trainers[i].getClf_score()
		print 'predict'
		predictors[i] = learner.predictor(tick, trainers[i].getClf())
		results = predictors[i].predicting(pred_dates)
		act_result = predictors[i].getAct_result()
		for (i,), result in np.ndenumerate(results):
			print 'Predicted adjusted close value for {} is {:.4f}'.format(pred_dates[i], result)
			print 'Actual adjusted close value for {} is {:.4f}'.format(pred_dates[i], act_result[i])
		print " "
	file.close()
	

if __name__ == '__main__':
    run()
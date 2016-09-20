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
	#parsing inputs from input.txt
	ticker = search('Ticker symbols:{}\n',inputs)
	tickers = ticker[0].split(",") #put all the ticker symbols into a list
	tickers = [tick.replace(' ','') for tick in tickers] #remove all the spaces for ticker symbols
	recomm = search('Recommendation:{}\n',inputs)
	recomm = recomm[0].replace(' ','')
	graph = search('Show estimated graph:{}\n',inputs)
	graph = graph[0].replace(' ','')
	dev_mode = search('Developer Mode:{}\n',inputs)
	dev_mode = dev_mode[0].replace(' ','')
	best_est = search('Show best_estimator:{}\n',inputs)
	best_est = best_est[0].replace(' ','')
	start_date = search('Start_date:{}\n',inputs)
	start_date = start_date[0].replace(' ','')
	end_date = search('End_date:{}\n',inputs)
	end_date = end_date[0].replace(' ','')
	pred_date = search('Predict_date:{}\n',inputs)
	pred_dates = pred_date[0].split(",")
	pred_dates = [date.replace(' ','') for date in pred_dates]
	# pred_value = search('Predict_value:{}\n',inputs)  #Ignore this since these 7 lines of debugging code are for parsing pred_value
	# pred_values = pred_value[0].split(";")			#pred_value is used for testing by putting your own open, high, and volume
	# pred_values_ = []
	# for values in pred_values:
	# 	temp = search('({:f},{:f},{:d})',values)
	# 	pred_values_.append([temp[x] for x in range(3)])
	# print pred_values_
	if dev_mode == 'on':
		print 'Developer mode on' 
	else: #if developer mode is off, set the developer inputs to default
		start_date = 'default'
		end_date = 'default'
		best_est = 'off'
	#training and predicting
	trainers = [0] * len(tickers)
	predictors = [0] * len(tickers)
	for i, tick in enumerate(tickers):
		print "Training for " + tick + "..."
		trainers[i] = learner.trainer(tick)
		trainers[i].training(start_date,end_date,best_est,graph)
		print "Error rate for {}: {:.4f}%".format(tick,(1 - trainers[i].getClf_score()) * 100)
		print "This is the result for " + tick + ":"
		predictors[i] = learner.predictor(tick, trainers[i].getClf())
		if dev_mode == 'on':
			results = predictors[i].predicting(pred_dates)
			act_result = predictors[i].getAct_result()
			for (i,), result in np.ndenumerate(results):
				print 'Predicted adjusted close value for {} is {:.4f}'.format(pred_dates[i], result)
				print 'Actual adjusted close value for {} is {:.4f}'.format(pred_dates[i], act_result[i])
		else:
			cur_data = stock.getCurrent(tick)
			print 'Today\'s data for {} is queried at {}'.format(tick, cur_data[4][:23])
			result = predictors[i].pred_curr(cur_data[0:3])
			print 'Predicted adjusted close value for today is {:.2f}'.format(float(result))
			if recomm == 'yes':
				print 'Curreny price for {} is {}'.format(tick, cur_data[3])
				print 'Recommendation:: Sell {} if price is greater than {:.2f}. Buy {} if price is lower than {:.2f}.'.format(
						tick,float(result) * 1.05, tick,float(result) * 0.95)
		print " "
	file.close()
	

if __name__ == '__main__':
    run()
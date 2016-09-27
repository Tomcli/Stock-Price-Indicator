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
	file = open("input.txt", "r") #get all the user inputs from input.txt
	inputs = file.read()

	#parsing inputs from input.txt
	ticker = search('Ticker symbols:{}\n',inputs)
	tickers = ticker[0].split(",") #put all the ticker symbols into a list
	tickers = [tick.replace(' ','') for tick in tickers] #remove all the unnecessary spaces

	recomm = search('Recommendation:{}\n',inputs)
	recomm = recomm[0].replace(' ','')

	manual = search('Manual inputs:{}\n',inputs)
	manual = manual[0].replace(' ','')

	manual_data = search('Stock data:{}\n',inputs)
	manual_data = manual_data[0].split(";")
	manual_data_ =[]
	for data in manual_data:
	 	temp = search('({},{:f},{:f},{:d})',data)
	 	manual_data_.append([temp[x] for x in range(4)])

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

	pred_by_date = search('Prediction by date:{}\n',inputs)
	pred_by_date = pred_by_date[0].replace(' ','')

	pred_date = search('Predict_date:{}\n',inputs)
	pred_dates = pred_date[0].split(",")
	pred_dates = [date.replace(' ','') for date in pred_dates]

	data_pre = search('Data preprocessing:{}\n',inputs)
	data_pre = data_pre[0].replace(' ','')

	# pred_value = search('Predict_value:{}\n',inputs)  #Ignore this since these 7 lines of debugging code are for parsing pred_value
	# pred_values = pred_value[0].split(";")			#pred_value is used for testing by putting your own open, high, and volume
	# pred_values_ = []
	# for values in pred_values:
	# 	temp = search('({:f},{:f},{:d})',values)
	# 	pred_values_.append([temp[x] for x in range(3)])
	# print pred_values_


	#Finish parsing
	if dev_mode == 'on':
		print 'Developer mode on' 
	else: #if developer mode is off, set the developer inputs to default
		start_date = 'default'
		end_date = 'default'
		best_est = 'off'
		graph = 'off'
		pred_by_date = 'off'
		data_pre = 'on'

	#training and predicting
	trainers = [0] * len(tickers) #put all the trainer and predictor objects into lists
	predictors = [0] * len(tickers)
	for i, tick in enumerate(tickers): #train and predict for every ticker symbol
		#training data
		print "Training for " + tick + "..."
		trainers[i] = learner.trainer(tick) #trainer is a class that trains all the data
		#train based on start_data and end_data, and decide whether or not to enable plots and preprocess data
		trainers[i].training(start_date, end_date, best_est, graph, data_pre) 
		print "Error rate for {}: {:.4f}%".format(tick,(1 - trainers[i].getClf_score()) * 100) #error rate is perecentage of (1 - R2 score)
		
		#predicting adjusted close
		print "This is the result for " + tick + ":"
		#predictor is a class that predicts the adjusted close price based on the trained regressor
		predictors[i] = learner.predictor(tick, trainers[i].getClf()) 
		if pred_by_date == 'on': #if Prediction by date is on, do prediction based on the given date
			results = predictors[i].predicting(pred_dates)
			act_result = predictors[i].getAct_result()
			for (i,), result in np.ndenumerate(results): #iterate through a numpy array
				print 'Predicted adjusted close value for {} is {:.4f}'.format(pred_dates[i], result)
				print 'Actual adjusted close value for {} is {:.4f}'.format(pred_dates[i], act_result[i])
		else: #if Prediction by date is off, predict the adjusted close price for today (most recent query from yahoo-finance)
			cur_data = stock.getCurrent(tick)
			print 'Today\'s data for {} is queried at {}'.format(tick, cur_data[4][:23]) #print out the queried time
			result = predictors[i].pred_curr(cur_data[0:3])
			print 'Predicted adjusted close value for today is {:.2f}'.format(float(result))
			if recomm == 'yes': #if recommendation is yes, give recomendations to buy or sell based on the predicted price with 1.5*error rate boundary 
				error = (1 - trainers[i].getClf_score())
				print 'Real time price for {} is {}'.format(tick, cur_data[3])
				print 'Recommendation: Sell {} if the price is greater than {:.2f}. Buy {} if the price is lower than {:.2f}.'.format(
						tick,float(result) * (1 + (1.5*error)), tick,float(result) * (1 - (1.5*error)))

		if manual == 'yes': #if Manual inputs is yes, predict the adjusted close price based on the given values
			for data in manual_data_:
				if data[0] == tick:
					print 'Your manual input for {} is ({},{},{})'.format(data[0],data[1],data[2],data[3])
					pred_result = predictors[i].pred_curr(cur_data[1:4])
					print 'Predicted adjusted close value for this manual input is {:.2f}'.format(float(pred_result))
		print " "

	file.close()
	

if __name__ == '__main__':
    run()
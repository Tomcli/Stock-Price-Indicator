import numpy as np
import pandas as pd
from IPython.display import display # Allows the use of display() for DataFrames
import matplotlib.pyplot as plt
import matplotlib
import data as stock
import learner
from parse import *


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
	pred_dates_ = [str(date).split('-') for date in pred_dates]
	#training and predicting
	trainers = [0] * len(tickers)
	predictors = [0] * len(tickers)
	for i, tick in enumerate(tickers):
		print "This is the data for " + tick
		data = stock.getData(tick,start_date[0],end_date[0],"default","default")
		trainers[i] = learner.trainer(tick,data)
		trainers[i].training()
		print 'predict'
		predictors[i] = learner.predictor(tick, trainers[i].getClf_list())
		predictors[i].predicting(pred_dates_)
		#print data
	file.close()
	

if __name__ == '__main__':
    run()
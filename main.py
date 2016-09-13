import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeRegressor
from IPython.display import display # Allows the use of display() for DataFrames
import matplotlib.pyplot as plt
import matplotlib
import data as stock
from parse import *


def run():
	file = open("input.txt", "r")
	inputs = file.read()
	ticker = search('Ticker symbols:{}\n',inputs)
	start_date = search('Start_date:{}\n',inputs)
	end_date = search('End_date:{}\n',inputs)
	tickers = ticker[0].split(",")
	print tickers
	for tick in tickers:
		tick_ = tick.replace(' ','')
		print "This is the data for " + tick_
		data = stock.getData(tick_,start_date[0],end_date[0],"monthly","default")
		print data
	file.close()
	

if __name__ == '__main__':
    run()
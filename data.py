import quandl
from yahoo_finance import Share
quandl.ApiConfig.api_key = 'K4JB2eKifGbx8RxUR9sc' #This is a public API key.

def getData(ticker,start,end,collapses,trans):
	"""
	Query the data based on the parameters and Return the query.
	"""
	quandlTicker = "YAHOO/" + ticker
	data = []
	if start.replace(' ','') == 'default':
		start = ''
	if end.replace(' ','') == 'default': 
		end = ''
	try:
		data = quandl.get(quandlTicker, start_date=start, end_date=end, collapse=collapses,transform=trans)
	except:
		print ("Query error: please change your inputs in input.txt(possibly invaild Ticker symbols, "
			"Start_date, End_date, or Predict_date) or check your API key.")
	return data

def getCurrent(ticker):
	"""
	Return the most recent stock data through yahoo_finance.
	"""
	stock = Share(ticker)
	stock.refresh() #refresh the query
	open_ = stock.get_open()
	volume = stock.get_volume()
	high = stock.get_days_high()
	price = stock.get_price()
	time = stock.get_trade_datetime()
	low = stock.get_days_low()
	return(open_,high,volume,price,time,low)
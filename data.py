import quandl
from yahoo_finance import Share
quandl.ApiConfig.api_key = 'YOURAPIKEY' #This is a private API key.

def getData(ticker,start,end,collapses,trans):
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
	stock = Share(ticker)
	stock.refresh() #refresh the query
	open_ = stock.get_open()
	volume = stock.get_volume()
	high = stock.get_days_high()
	price = stock.get_price()
	time = stock.get_trade_datetime()
	return(open_,high,volume,price,time)
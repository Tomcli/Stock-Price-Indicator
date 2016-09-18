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
		#data = quandl.get("WIKI/FB", start_date="2014-01-01", end_date="2014-12-31", collapse="monthly", transform="diff")
		#data = quandl.get_table("ZACKS/FC", ticker="MSFT")
	except:
		print ("Query error: please change your inputs in input.txt(possibly invaild Ticker symbols, "
			"Start_date, End_date, or Predict_date) or check your API key.")
	return data
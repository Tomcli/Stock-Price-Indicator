import quandl
quandl.ApiConfig.api_key = 'YOURAPIKEY'

def getData(ticker,start,end,collapses,trans):
	quandlTicker = "WIKI/" + ticker
	data = []
	try:
		data = quandl.get(quandlTicker, start_date=start, end_date=end, collapse=collapses,transform=trans)
		#data = quandl.get("WIKI/FB", start_date="2014-01-01", end_date="2014-12-31", collapse="monthly", transform="diff")
		#data = quandl.get_table("ZACKS/FC", ticker="MSFT")
	except:
		print "There is no data with this data range, please change your ticker symbols/start_date/end_date."
	return data
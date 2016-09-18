# Stock Price Indicator

This is a python script for predicting stock's adjused close price using data from _Quandl_. This script will take your current stock open price, highest price, and volume to make a prediction for the adjusted close price of the day. 

## Important

- Authentication: Replace `quandl.ApiConfig.api_key = 'YOURAPIKEY'` to your own Quandl API Key in **data.py**.
- Libraries: Must have `quandl`, `yahoo-finance`, `parse`, `numpy`, `pandas`, and `matplotlib` installed to your python interpreter.

## Installation

1. Download and unzip this package. 
2. Replace authentication key to your own Quandl API Key at line 3 in **data.py** .
3. Install `quandl`, `yahoo-finance`, `parse`, `numpy`, `pandas`, and `matplotlib` to your python. You can use `pip install [library]` to install.

## How to use this script##
1. Modify **input.txt** with your stocks' ticker symbol, open price, highest price, and volume for your prediction or leave it as default for recommendation (Please read **Definition for input.txt** for more details).
2. Run `python main.py` in this directory.
3. Use the result to justify your buying and selling.

## Definition for input.txt##
### Main Inputs
- Ticker symbols: Put down all your ticker symbols and separate each of them with `,` (e.g. GOOG,FB)

### Developer Inputs
- Developer Mode: Set it ##True## to enable all the developer inputs. Otherwise set it ##False##
- Start_date: Put down data training starting date with yyyy-mm-dd format or default(all the data from 2013 to 2016)
- End_date: Put down data traing ending date with yyyy-mm-dd format or default(all the data from 2013 to 2016)
- Predict_date: Put down the date you want to predict with yyyy-mm-dd format or default(predict stock prices for the recent week)

### Debug Inputs
Please ignore all the debug inputs since it's for debugging.

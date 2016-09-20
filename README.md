# Stock Price Indicator

This is a python script for predicting stock's adjused close price using data from _Quandl_. This script will take your current stock open price, highest price, and volume to make a prediction for the adjusted close price of the day. 

## Important

- Authentication: Replace `quandl.ApiConfig.api_key = 'YOURAPIKEY'` to your own Quandl API key in **data.py**. Strongly recommend to replace this with your own API key since the current API key in data.py is shared with the public.
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
- Ticker symbols: Put down all your ticker symbols and separate each of them with `,` (e.g. **GOOG,FB**).
- Recommendation: Put down **yes** for recommendations to buy or sell for each trained stock. Otherwise put down **no**..
- Manual inputs: Put down **yes** to enable **Stock data** inputs. Otherwise put down **no**.
- Stock data: Put down the stock data that you want to predict manually with (ticker symbols, open price, current highest price, volume) format and separate each of them with `;` (e.g. **(goog,741.86,742.0,2980700);(fb,126.89,128.80,15691100)**). Be aware that **open price** and **current highest price** need to have 2 decimals(e.g **42.12**) and volume has to be a whole number. Remember to put down **yes** at **Manual inputs** to enable this feature.

### Developer Inputs
- Developer Mode: Set it **on** to enable all the developer inputs. Otherwise set it **off**.
- Show best_estimator: Set it **on** to print out the best estimator and it's parameters. Otherwise set it **off**. 
- Show estimated graph: Set it **on** to plot a graph that compares the predicted data and actual data. Otherwise set it **off**.
- Start_date: Put down data training starting date with yyyy-mm-dd format or default(data from the past three months).
- End_date: Put down data traing ending date with yyyy-mm-dd format or default(data from the past three months).
- Prediction by date: Set it **on** to enable **Predict_date** inputs and disable today's prediction. Otherwise set it **off**.
- Predict_date: Put down the date you want to predict with yyyy-mm-dd format and separate each of them with `,` (e.g. **2015-09-21, 2016-09-15**). Important: Predict dates that are not exist in the quandl database will create an error. Remember to set **Prediction by date** to **on** in order to enable this feature.

### Debugging Inputs
Please ignore all the debugging inputs since it's for debugging.

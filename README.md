# Stock Price Indicator

This is a python script for predicting stock's adjusted close price using data from _Quandl_. This script will take your current stock open price, highest price, and volume to make a prediction for the adjusted close price of the day. 

## Important

- Authentication: Replace `quandl.ApiConfig.api_key = 'YOURAPIKEY'` to your own Quandl API key in **data.py**. Strongly recommend replacing this with your own API key since the current API key in data.py is shared with the public.
- Libraries: Must have `quandl`, `yahoo-finance`, `parse`, `numpy`, `pandas`, and `matplotlib` installed to your python interpreter.
- Installation: The installation instructions are for OS X and Linux users. Windows users need to install a terminal that runs Unix commands.
- Usage: Using this script during nonmarket hours will give you a prediction with data leakage because you are predicting a known adjusted close price. However, you can use manual inputs option to test or estimate using your own open, high, and volume data.
- Known Bug: Since there are limited queries for real-time stock information from Yahoo finance, sometimes it will query the data from previous trade day or even return Null. Therefore, you may want to put down your real time stock information manually(using ##manual inputs##) for accurate predictions.

## Installation

1. Download and unzip this package. 
2. Replace authentication key to your own Quandl API Key at line 3 in **data.py**.
3. Install `quandl`, `yahoo-finance`, `parse`, `numpy`, `pandas`, and `matplotlib` to your python. You can use `pip install [library]` in your terminal to install.

## How to use this script##
1. Modify **input.txt** with your stocks' ticker symbols and leave everything else as default for recommendations or put down your own customized data (Please read **Definition for input.txt** for more details).
2. Open your terminal. Run `python main.py` in this directory. It will take about a minute to predict the adjusted close price.
3. Use the result to justify your buying and selling.

## Definition for input.txt##
### Main Inputs
- Ticker symbols: Put down all your ticker symbols and separate each of them with `,`. (e.g. **GOOG,FB**).
- Recommendation: Put down **yes** for recommendations to buy or sell for each trained stock. (Default: **no**)
- Manual inputs: Put down **yes** to enable **Stock data** inputs. (Default: **no**)
- Stock data: Put down the stock data that you want to predict manually with *(ticker symbols, open price, current highest price, volume)* format and separate each of them with `;`. For example, **(goog,741.86,742.0,2980700);(fb,126.89,128.80,15691100)**). Be aware that **open price** and **current highest price** need to have 2 decimals and volume has to be a whole number. Remember to put down **yes** at **Manual inputs** to enable this feature.
- Data size: Put down the number of data you want to train. The number must be an integer. (Default: **600**)

### Developer Inputs
- Developer Mode: Set it **on** to enable all the developer inputs. (Default: **off**)
- Show best_estimator: Set it **on** to print out the best estimator and it's parameters. (Default: **off**)
- Show estimated graph: Set it **on** to plot a graph that compares the predicted data and actual data. (Default: **off**)
- Start_date: Put down data training starting date with yyyy-mm-dd format or default(data from the past three months).
- End_date: Put down data training ending date with yyyy-mm-dd format or default(data from the past three months).
- Prediction by date: Set it **on** to enable **Predict_date** inputs and disable today's prediction and recommendation. (Default: **off**)
- Predict_date: Put down the date you want to predict with yyyy-mm-dd format and separate each of them with `,`. For example, **2015-09-21, 2016-09-15**. **Important**: Predict dates that do not exist in the quandl database will create an error. Remember to set **Prediction by date** to **on** in order to enable this feature.
- Data preprocessing: Set it **off** to disable data preprocessing. (Default: **on**)


### Debugging Inputs
Please ignore all the debugging inputs since it's for debugging.

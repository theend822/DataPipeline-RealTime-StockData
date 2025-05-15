import requests
import random
import datetime
import os
import json
import config
from config import data_prep_parameters

run_date = datetime.datetime.now().strftime("%Y-%m-%d")
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

##############################################
# pull Apple stock data from Alpha Vantage
##############################################

# API call parameters
symbol = data_prep_parameters['symbol']
interval = data_prep_parameters['interval']
apikey = data_prep_parameters['apikey']
outputsize = data_prep_parameters['outputsize']

url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&outputsize={outputsize}&apikey={apikey}'

r = requests.get(url)
data = r.json()

# focus on the time series stock data only
raw_data = data['Time Series (1min)']

# save timestamp into a list
ts_list = list(raw_data.keys())

##############################################
# now will manually insert bad data
##############################################

# define total number rows with bad data
bad_data_size = 5

# save the randomly selected row index into a list
random_row_index = []
for _ in range(bad_data_size):
    random_row_index.append(random.randint(10, len(raw_data)))

bad_open_price_log = ""
bad_volume_log = ""

# will update the open price to 0 for 3 randomly selected rows
for idx in random_row_index[:2]:
    bad_open_price_log += f"Original data is {raw_data[ts_list[idx]]}\n"
    raw_data[ts_list[idx]]['1. open'] = "0"
    bad_open_price_log += f"updated data is {raw_data[ts_list[idx]]}\n\n\n"

# will update the volume to 0 for 2 randomly selected rows
for idx in random_row_index[3:]:
    bad_volume_log += f"Original data is {raw_data[ts_list[idx]]}\n"
    raw_data[ts_list[idx]]['5. volume'] = "0"
    bad_volume_log += f"Updated data is {raw_data[ts_list[idx]]}\n\n\n"


##############################################
# save data into a json file
##############################################

# /Users/jxy/Desktop/500k/RealTime_DataPipeline/DataPipeline-RealTime-StockData/data_prep/data
# DataPipeline-RealTime-StockData/data_prep/data
data_file = os.path.join("DataPipeline-RealTime-StockData/data_prep/data", f"raw_stock_data_{run_date}.json")
with open(data_file, "w") as f:
    json.dump(raw_data, f, indent=2)

print(f"Data saved to: {data_file}")

##############################################
# log the summary of data after bad data insertion
##############################################

log_file = os.path.join("DataPipeline-RealTime-StockData/data_prep/logging", f"log_{timestamp}.txt")

log_content = f"""

Data Preparation Log
{timestamp}
--------------------------------
total number of rows: {len(raw_data)}
total number of rows with bad data: {bad_data_size}
--------------------------------
OPEN PRICE UPDATES:
------------------
{bad_open_price_log}

VOLUME UPDATES:
------------------
{bad_volume_log}

"""

with open(log_file, "w") as f:
    f.write(log_content)

print(f"Log written to: {log_file}")
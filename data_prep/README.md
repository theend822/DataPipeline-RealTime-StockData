# Data Preparation

To simulate the real time data processing, this standalone data prep step has been created to:
- download real stock data from Alpha Vantage via API call
- randomly insert bad data
- save data into a local folder


Next, the downloaded data will be "sent" to the pipeline row by row, 50 rows per seconds, and then processed by the pipeline. In this way, the offline data is "transformed" into a real time data stream
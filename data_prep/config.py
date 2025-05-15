import os
from dotenv import load_dotenv

load_dotenv()

data_prep_parameters = {
    'symbol': 'AAPL',
    'interval': '1min',
    'apikey': os.getenv("AV_API_KEY"),
    'outputsize': 'full',
}
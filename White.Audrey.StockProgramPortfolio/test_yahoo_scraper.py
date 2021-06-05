import re
import csv
import json
from bs4.element import Script
import requests
from io import StringIO
from bs4 import BeautifulSoup


stock_stats_url = 'https://finance.yahoo.com/quote/{}/key-statistics?p={}'
stock_historical_data_url = 'https://finance.yahoo.com/quote/{}/history?p={}'

amc_symbol = 'AMC'

response = requests.get(stock_stats_url.format(amc_symbol, amc_symbol))

soup = BeautifulSoup(response.text, 'html.parser')

pattern = re.compile(r'\s--\sData\s--\s')

#finds an element that matches pattern in the script
script_data = soup.find('script', text=pattern).contents[0]

#starts
script_data[:500]

#reaches end
print(script_data[-500:])

start = script_data.find('context')-2

script_data[start:2]

json_data = json.loads(script_data[start:-12])

json_data['context'].keys()

print(json_data['context'].keys())
print(json_data)

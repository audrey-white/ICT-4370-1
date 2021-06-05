import math
from datetime import date, datetime

class Stock():
    def __init__(self, symbol, date, open_price, high_value, low_value, closing_price, volume):
        self.symbol = symbol
        self.date = date
        self.open_price = open_price
        self.high_value = high_value
        self.low_value= low_value
        self.closing_price = closing_price
        self.volume = volume
        self.no_shares = 0
        self.total_value = 0

       # Function to calculate total value
    def calculate_Value(self, curr_val, shares):
        try:
            value = curr_val * shares
            self.total_value = value
            return value
        except TypeError:
            print(f'1 or more arguments are not type int')
    
    def set_Share_No(self, val):
        self.no_shares = val

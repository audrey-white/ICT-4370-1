"""
 Author: Audrey White
 Date Created: 06/04/2021
 Functionality:
    The purpose of this program is to calculate how much you would have gained or loss in 2021 so far on my favorite meme stocks.
    You can enter your hypothetical purchase date and number of shares. The program will collect data using an open source api
    called yfinance. This api is based of the deprecated yahoo finance api and is free to use: here is a link to the info.: 
    https://pypi.org/project/yfinance/

    After receiving and formatting data from the url endpoints, the program will enter stock data into a database using SQLite.
    A simple GUI made with tkinter will display where the user has the option to enter a purchase date and number of shares for each stock.
    The program should then create a graph of your gains/losses per stock using matplot lib.
"""


from numpy import result_type
from numpy.lib.function_base import _ureduce
from pandas.core import series
import yfinance as yf
import sqlite3
from sqlite3.dbapi2 import Error
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import style
style.use('seaborn')

from stock import *
from stock_bond_data_functions import *

import tkinter as tk
from tkinter import *
from tkcalendar import *
from tkinter import messagebox
from calendar_popup import *

try:
    amc = yf.download('AMC', start="2021-01-01")
    gme = yf.download('GME', start="2021-01-01")
    bb = yf.download('BB', start="2021-01-01")
    nok = yf.download('NOK', start="2021-01-01")
except error:
    messagebox.showerror('error', 'Cannot access yfinance api endpoint')       

amc_stocks = []
gme_stocks = []
bb_stocks =[]
nok_stocks =[]
stock_list = []


#formats columns of dataframe to include dates, makes date a key
amc['date'] = amc.index
gme['date'] = gme.index
bb['date'] = bb.index
nok['date'] = nok.index

#creates and stores lists of stocks as objects using the Stock class
for row in amc.itertuples():
    temp_stock = Stock('AMC', row.date, row.Open, row.High, row.Low, row.Close, row.Volume)
    stock_list.append(temp_stock)

for row in gme.itertuples():
    temp_stock = Stock('GME', row.date, row.Open, row.High, row.Low, row.Close, row.Volume)
    stock_list.append(temp_stock)

for row in bb.itertuples():
    temp_stock = Stock('BB',row.date, row.Open, row.High, row.Low, row.Close, row.Volume)
    stock_list.append(temp_stock)

for row in nok.itertuples():
    temp_stock = Stock('NOK',row.date, row.Open, row.High, row.Low, row.Close, row.Volume)
    stock_list.append(temp_stock)


#now connects to or creates a database to store the stock info. collected
try:
    conn = sqlite3.connect('White.Audrey.StockProgramPortfolio/meme_stocks.db')
    print('Database was opened\n')

except Error as e:
    print(e)
finally:
    # create cursor
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS stocks(Symbol TEXT, Date TEXT, Open INTEGER, High INTEGER, Low INTEGER, Close INTEGER, Volume INTEGER)')

    #fills in the database with all stock data retrieved from json file and calculates the total stock value for table
    for i in range(len(stock_list)):
         c.execute('INSERT INTO stocks VALUES (?,?,?,?,?,?,?)', (stock_list[i].symbol, str(stock_list[i].date), int(stock_list[i].open_price), int(stock_list[i].high_value), int(stock_list[i].low_value), int(stock_list[i].closing_price), int(stock_list[i].volume)))

    c.execute("SELECT * FROM stocks")
    conn.commit()
    conn.close()


#this setups the simple GUI
root = tk.Tk()
root.geometry('600x600')
e = Entry(root, width=100)
e.pack()
e.insert(0, "Enter your share number")

class DateNotSelectedError(Error):
    """Raised if no date is set for a stock"""
    pass


def getDate(stock):
    global amc_date
    global gme_date
    global bb_date
    global nok_date
    try:
        #CalenderPopup is a custom class I created using tkcalendar
        calendar = CalendarPopup(root,'day', 2021, 1, 1)
        calendar.display()
        print(calendar.result)
        result = calendar.result
        if(stock == 'AMC'): 
            amc_date = str(result)
        elif(stock == 'GME'):
            gme_date = str(result)
        elif(stock == 'BB'):
            bb_date = str(result)
        elif(stock == 'NOK'):
            nok_date = str(result)
        else:
            raise DateNotSelectedError

    except DateNotSelectedError:
        messagebox.showerror('error', 'Date did not set for selected stock')


def userSubmit(stock):
    global amc_shares
    global gme_shares
    global bb_shares
    global nok_shares
    try:
        input = e.get()
        if(stock == 'AMC'): 
            amc_shares = input
        elif(stock == 'GME'):
            gme_shares = input
        elif(stock == 'BB'):
            bb_shares = input
        elif(stock == 'NOK'):
            nok_shares = input
        user_input_label = Label(root, text=input)
        user_input_label.pack()
        int(input)
    except ValueError:
        messagebox.showerror('error', 'Should input integers only for shares')


#setups form buttons for user input
amc_date = ''
amc_shares = 0
amc_date_button = Button(root, text='Enter purchase date for AMC: ', command=lambda *args: getDate('AMC')).pack()
amc_share_button = Button(root, text='Enter number of AMC shares: ', command=lambda *args: userSubmit('AMC')).pack()

gme_date = ''
gme_shares = 0
gme_date_button = Button(root, text='Enter purchase date for Gamestop (GME): ', command=lambda *args: getDate('GME')).pack()
gme_share_button = Button(root, text='Enter number of shares for Gamestop: ', command=lambda *args: userSubmit('GME')).pack()

bb_date = ''
bb_shares = 0
bb_date_button = Button(root, text='Enter purchase date for BlackBerry (BB): ', command=lambda *args: getDate('BB')).pack()
bb_share_button = Button(root, text='Enter number of shares for BlackBerry: ', command=lambda *args: userSubmit('BB')).pack()

nok_date = ''
nok_shares = 0
nok_date_button = Button(root, text='Enter purchase date for Nokia (NOK): ', command=lambda *args: getDate('NOK')).pack()
nok_share_button = Button(root, text='Enter number of shares for Nokia: ', command=lambda *args: userSubmit('NOK')).pack()

#checks to make sure user selected dates for each stock
def closing():
    if(amc_date == '' or gme_date == '' or bb_date == '' or nok_date == ''):
        if messagebox.askokcancel('Quit', 'Must enter date for all the stocks before exiting window, do you want to quit?'):
            root.destroy()
    else:
        root.destroy()

root.protocol("WM_DELETE_WINDOW", closing)
root.mainloop()
user_stocks = []

amc_dates= []
gme_dates= []
bb_dates = []
nok_dates =[]

amc_profits= []
gme_profits=[]
bb_profits=[]
nok_profits=[]

#for loop compares user input stock data with api data, calculates total profit/loss for each stock entry on and after selected dates
for i in range(len(stock_list)):
    
    dt_object = datetime.strptime(str(stock_list[i].date),'%Y-%m-%d %H:%M:%S')
    a_datetime_object = datetime.strptime(amc_date, '%Y-%m-%d')
    g_datetime_object = datetime.strptime(gme_date, '%Y-%m-%d')
    b_datetime_object = datetime.strptime(bb_date, '%Y-%m-%d')
    n_datetime_object = datetime.strptime(nok_date, '%Y-%m-%d')

    if(stock_list[i].symbol == 'AMC' and dt_object >= a_datetime_object):
        temp_stock = Stock('AMC',stock_list[i].date, stock_list[i].open_price, stock_list[i].high_value, stock_list[i].low_value, stock_list[i].closing_price, stock_list[i].volume)
        temp_stock.set_Share_No(amc_shares)
        temp_stock.calculate_Value(int(temp_stock.closing_price), int(temp_stock.no_shares))
        amc_profits.append(temp_stock.total_value)
        amc_stocks.append(temp_stock)
        amc_dates.append(temp_stock.date)
    elif(stock_list[i].symbol == 'GME' and dt_object >= g_datetime_object):
        temp_stock = Stock('GME',stock_list[i].date, stock_list[i].open_price, stock_list[i].high_value, stock_list[i].low_value, stock_list[i].closing_price, stock_list[i].volume)
        temp_stock.set_Share_No(gme_shares)
        temp_stock.calculate_Value(int(temp_stock.closing_price), int(temp_stock.no_shares))
        gme_stocks.append(temp_stock)
        gme_profits.append(temp_stock.total_value)
        gme_dates.append(temp_stock.date)
    elif(stock_list[i].symbol == 'BB' and dt_object >= b_datetime_object):
        temp_stock = Stock('BB',stock_list[i].date, stock_list[i].open_price, stock_list[i].high_value, stock_list[i].low_value, stock_list[i].closing_price, stock_list[i].volume)
        temp_stock.set_Share_No(gme_shares)
        temp_stock.calculate_Value(int(temp_stock.closing_price), int(temp_stock.no_shares))
        bb_stocks.append(temp_stock)
        bb_profits.append(temp_stock.total_value)
        bb_dates.append(temp_stock.date)
    elif(stock_list[i].symbol == 'NOK' and dt_object >= n_datetime_object):
        temp_stock = Stock('NOK',stock_list[i].date, stock_list[i].open_price, stock_list[i].high_value, stock_list[i].low_value, stock_list[i].closing_price, stock_list[i].volume)
        temp_stock.calculate_Value(int(temp_stock.closing_price), int(temp_stock.no_shares))
        nok_stocks.append(temp_stock)
        nok_profits.append(temp_stock.total_value)
        nok_dates.append(temp_stock.date)

    user_stocks.append(temp_stock)


fig, ax = plt.subplots()

plt.title('Calculated Gain/Loss on My Favorite Meme Stocks')
plt.xlabel('Date')
plt.ylabel('Profit/Loss (USD)')

#sorts all the dates for plotting
amc_dates, amc_profits = zip(*sorted(zip(amc_dates,amc_profits),key=lambda amc_dates: amc_dates))
ax.plot(amc_dates, amc_profits, label = 'AMC')
gme_dates, gme_profits = zip(*sorted(zip(gme_dates,gme_profits),key=lambda gme_dates: gme_dates))
ax.plot(gme_dates, gme_profits, label = 'GME')
bb_dates, bb_profits = zip(*sorted(zip(bb_dates,bb_profits),key=lambda bb_dates: bb_dates))
ax.plot(bb_dates, bb_profits, label = 'BB')
nok_dates, nok_profits = zip(*sorted(zip(nok_dates,nok_profits),key=lambda nok_dates: nok_dates))
ax.plot(nok_dates, nok_profits, label = 'NOK')

formatter = mdates.DateFormatter("%Y-%m-%d")
ax.xaxis.set_major_formatter(formatter)
locator = mdates.DayLocator()

plt.legend()
plt.savefig('White.Audrey.StockProgramPortfolio/memeStocksPlot.png')
plt.show()


"""
 Author: Audrey White
 Date Created: 05/23/2021
 Functionality:
                This program reads stock data from a json file. The file is formatted as a list of multiple dictionaries for the data recorded on each stock on different dates.
                First, the program formats the json data into dictionary format. Then it iterates through the stock dictionary and initializes stock objects using the imported
                Stock class. A stock class method is used to set the number of shares based on previous stock data given in the stock program 3. Each stock object is then inserted into a database
                table along with the calculated total stock value. The data is then fetched from the database and is separated by stock symbol and their purchase dates into lists.
                The stock lists dates represent the graphs x-axis values while the stock total values represent the y-axis values for each stock. A copy of the graph is saved in a
                png file. 
"""


import PySimpleGUI as sg
import json
import sqlite3
from sqlite3.dbapi2 import Error
from datetime import datetime
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from yahoo_finance import Share

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import style
style.use('seaborn')

from stock import *
from stock_bond_data_functions import *

#opens stock json file
stock_file = 'White.Audrey.StockProgram4/AllStocks.json'
stock_file = check_to_read_file(stock_file)

d = json.JSONDecoder()
json_list = []
f = stock_file.read()

#this formats the json data to lists
while True:
    try:
      j,n = d.raw_decode(f) 
      json_list.append(j)
    except ValueError:
      break
    f = f[n:]

#turns json data into single dictionary
stock_dict = dict(stocks = json_list)

stock_file.close()
stock_list = []

#creates stock objects from stock dictionary
for i in range(len(stock_dict['stocks'][0])):
    temp_stock = Stock(stock_dict['stocks'][0][i].get('Symbol'), stock_dict['stocks'][0][i].get('Date'), stock_dict['stocks'][0][i].get('Open'), stock_dict['stocks'][0][i].get('High'), stock_dict['stocks'][0][i].get('Low'), stock_dict['stocks'][0][i].get('Close'), stock_dict['stocks'][0][i].get('Volume'))
    temp_stock.set_Share_No()
    stock_list.append(temp_stock)


try:
    conn = sqlite3.connect('White.Audrey.StockProgram4/stocks.db')
    print('Database was opened\n')

except Error as e:
    print(e)
finally:
    # create cursor
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS stocks(Symbol TEXT, Date TEXT, Open INTEGER, High INTEGER, Low INTEGER, Close INTEGER, Volume INTEGER, Total Value INTEGER)')
    #fills in the database with all stock data retrieved from json file and calculates the total stock value for table
    for i in range(len(stock_list)):
         total_value = stock_list[i].calculate_Value(stock_list[i].closing_price, stock_list[i].no_shares)
         c.execute('INSERT INTO stocks VALUES (?,?,?,?,?,?,?,?)', (stock_list[i].symbol, stock_list[i].purchase_date, stock_list[i].open_price, stock_list[i].high_value, stock_list[i].low_value, stock_list[i].closing_price, stock_list[i].volume, total_value))

    c.execute("SELECT * FROM stocks")

    #initializes all stock lists for graph plotting
    google = []
    g_dates = []
    msft = []
    msft_dates = []
    rds_a = []
    rds_dates = []
    aig = []
    aig_dates = []
    fb = []
    fb_dates = []
    m = []
    m_dates = []
    f = []
    f_dates = []
    ibm = []
    ibm_dates = []

    #fectches and stores values of stock total value and dates for each stock
    for row in c.fetchall():
        if(row[0] == 'GOOG'):
            google.append(row[7])
            g_dates.append(row[1])
        elif(row[0] == 'MSFT'):
            msft.append(row[7])
            msft_dates.append(row[1])
        elif(row[0] == 'RDS-A'):
            rds_a.append(row[7])
            rds_dates.append(row[1])
        elif(row[0] == 'AIG'):
            aig.append(row[7])
            aig_dates.append(row[1])
        elif(row[0] == 'FB'):
            fb.append(row[7])
            fb_dates.append(row[1])
        elif(row[0] == 'M'):
            m.append(row[7])
            m_dates.append(row[1])
        elif(row[0] == 'F'):
            f.append(row[7])
            f_dates.append(row[1])
        elif(row[0] == 'IBM'):
            ibm.append(row[7])
            ibm_dates.append(row[1])
            
     
    fig, ax = plt.subplots()

    #formats dates from database
    g_dates = [datetime.strptime(d,"%d-%b-%y").date() for d in g_dates]
    msft_dates = [datetime.strptime(d,"%d-%b-%y").date() for d in msft_dates]
    rds_dates = [datetime.strptime(d,"%d-%b-%y").date() for d in rds_dates]
    aig_dates = [datetime.strptime(d,"%d-%b-%y").date() for d in aig_dates]
    fb_dates = [datetime.strptime(d,"%d-%b-%y").date() for d in fb_dates]
    m_dates = [datetime.strptime(d,"%d-%b-%y").date() for d in m_dates]
    f_dates = [datetime.strptime(d,"%d-%b-%y").date() for d in f_dates]
    ibm_dates = [datetime.strptime(d,"%d-%b-%y").date() for d in ibm_dates]

    #sorts all the dates for plotting
    g_dates, google = zip(*sorted(zip(g_dates,google),key=lambda g_dates: g_dates[0]))
    ax.plot(g_dates, google, label = 'GOOGL')
    msft_dates, msft = zip(*sorted(zip(msft_dates, msft),key=lambda msft_dates: msft_dates[0]))
    ax.plot(msft_dates, msft, label = 'MSFT')
    rds_dates, rds_a = zip(*sorted(zip(rds_dates,rds_a),key=lambda rds_dates: rds_dates[0]))
    ax.plot(rds_dates, rds_a, label = 'RDS-A')
    aig_dates, aig = zip(*sorted(zip(aig_dates,aig),key=lambda aig_dates: aig_dates[0]))
    ax.plot(aig_dates, aig, label = 'AIG')
    fb_dates, fb = zip(*sorted(zip(fb_dates, fb),key=lambda fb_dates: fb_dates[0]))
    ax.plot(fb_dates, fb, label = 'FB')
    m_dates, m = zip(*sorted(zip(m_dates, m),key=lambda m_dates: m_dates[0]))
    ax.plot(m_dates, m, label = 'M')
    f_dates, f = zip(*sorted(zip(f_dates, f),key=lambda f_dates: f_dates[0]))
    ax.plot(f_dates, f, c = 'pink', label = 'F')
    ibm_dates, ibm = zip(*sorted(zip(ibm_dates, ibm),key=lambda ibm_dates: ibm_dates[0]))
    ax.plot(ibm_dates, ibm, label = 'IBM')
 
    formatter = mdates.DateFormatter("%Y-%m-%d")
    ax.xaxis.set_major_formatter(formatter)
    locator = mdates.DayLocator()
    plt.legend()
    plt.savefig('White.Audrey.StockProgram4/simplePlot.png')
    plt.show()
   
conn.commit()
conn.close()


matplotlib.use("TkAgg")

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg

# Define the window layout
layout = [
    [sg.Text("Plot test")],
    [sg.Canvas(key="-CANVAS-")],
    [sg.Button("Ok")],
]

# Create the form and show it without the plot
window = sg.Window(
    "Matplotlib Single Graph",
    layout,
    location=(0, 0),
    finalize=True,
    element_justification="center",
    font="Helvetica 18",
)

# Add the plot to the window
draw_figure(window["-CANVAS-"].TKCanvas, fig)

event, values = window.read()

window.close()
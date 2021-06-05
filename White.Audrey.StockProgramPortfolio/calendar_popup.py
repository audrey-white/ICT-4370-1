from datetime import date
from logging import error
import tkinter as tk
from tkinter import *
from numpy import select
from tkcalendar import *
from tkinter import simpledialog
from tkinter import messagebox



#custom calendar popup class I created using tkcalendar
class CalendarPopup(simpledialog.Dialog):

    def __init__(self, root, mode, year, month, day):
        super(simpledialog.Dialog,self).__init__(root)
        self.root = root
        self.mode = mode
        self.year = year
        self.month = month
        self.day = day
        self.result =''
        root.geometry('400x400')


    def display(self): 
        try:
            self.calendar = Calendar(self, selectmode=self.mode, year=self.year, month=self.month, day=self.day)
            self.calendar.pack(pady=30)
            select_button = Button(self, text='Select date', command=self.select_date)
            select_button.pack(pady=30)
            self.wait_window(self)
        except error:
            messagebox.showerror("error", "Date not selected")
        except TypeError:
             messagebox.showerror("error", "Initial calendar date not formatted properly, must enter yyyy, m, d in constructor")
        
    
    def select_date(self):
        self.result = self.calendar.selection_get()
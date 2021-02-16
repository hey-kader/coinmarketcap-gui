from tkinter import *
from tkinter import ttk

from requests import Request, Session 
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

import json

class App:

    def __init__ (self):
        self.win = Tk()
        self.win.geometry ("1000x500")
        self.win.title ("Cryptocurrency Charts")
        
        self.root_frame = Frame (self.win)
        self.root_frame.pack (fill="both", expand=1)

        self.canvas = Canvas (self.root_frame)
        self.canvas.pack (side=LEFT, fill="both", expand=1)

        self.scroller = ttk.Scrollbar(self.root_frame, orient=VERTICAL, command=self.canvas.yview)
        self.scroller.pack(side=RIGHT, fill=Y)

        self.canvas.configure (yscrollcommand=self.scroller.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")));

        self.data_frame = Frame (self.canvas)
        self.canvas.create_window ((0,0), window=self.data_frame, anchor="nw")

        self.data = self. get_data ()["data"]

        self.slugs = []
        self.tickers = []
        self.prices = []
        self.supply = []
        self.marketcap = []

        for i in range (100):
            self.slugs.append(self.data[i]["slug"])
            self.tickers.append(self.data[i]["symbol"]) 
            self.prices.append(self.data[i]["quote"]["USD"]["price"])
            self.supply.append(self.data[i]["circulating_supply"])
            self.marketcap.append(self.prices[i]*self.supply[i])

        for t in range (100):
            Label (self.data_frame, text=str(t+1)+'. ').grid (row=t, column=0,padx=10)  
            Label (self.data_frame, text=self.slugs[t]).grid (row=t, column=1,padx=5)  
            Label (self.data_frame, text=self.tickers[t]).grid (row=t, column=2,padx=5)  
            Label (self.data_frame, text="Price: " + str(self.prices[t])).grid (row=t, column=3,padx=5)
            Label (self.data_frame, text="Market Cap: " + str(self.marketcap[t])).grid (row=t, column=4,padx=5)
            Label (self.data_frame, text="Supply: " + str(self.supply[t])).grid (row=t, column=5, padx=5) 

        self.win.mainloop ()

    def write_json (self, data):
        with open ("coins.json", "w") as f:
            f.write (str(data["data"]))
            f.close ()

     
    def get_data (self):

        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

        parameters = {
            'start':'1',
            'limit':'5000',
            'convert':'USD'
        }

        headers = {
                
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '62b1b5c3-f6cb-454e-a20e-3cbc95b6621a'
                
        }

        session = Session ()
        session.headers.update (headers)

        try:
            response = session.get (url, params=parameters)
            data = json.loads(response.text)
            self.write_json (data)
            return data

        except(ConnectionError, Timeout, TooManyRedirects) as e:
            print (e)
            return False



def main ():
    a = App ()

if __name__ == '__main__':
    main ()




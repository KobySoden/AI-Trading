import requests
from datetime import date
import json
import os
from dotenv import load_dotenv
import time
import csv

#load environment variables
load_dotenv()
path = os.path.dirname(os.path.abspath(__file__))
path = "/home/koby/Desktop/code/AI-Trading"

BASE_URL = "https://yahoo-finance127.p.rapidapi.com"

headers = {
	"X-RapidAPI-Key": os.environ["X-RapidAPI-Key"],
	"X-RapidAPI-Host": os.environ["X-RapidAPI-Host"]
}

def get_news(ticker):
    url = f"{BASE_URL}/news/{ticker}"
    response = requests.get(url, headers=headers)
    return response.json()

def get_price(ticker):
    url = f"{BASE_URL}/price/{ticker}"
    response = requests.get(url, headers=headers)
    return response.json()


def daily_data(ticker):
    #check if data folder exists
    if not os.path.exists(f"{path}/data/{ticker}"):
        os.makedirs(f"{path}/data/{ticker}")
    
    today = date.today()

    with open(f"{path}/data/{ticker}/{today.isoformat()}--News.json", "w") as f:
        f.write(json.dumps(get_news(ticker)))
    
    #with open(f"{path}/data/{ticker}/{today.isoformat()}--Price.json", "w") as f:
        #f.write(json.dumps(get_price(ticker)))

if __name__ == "__main__":
    #tickers = ["FIVN","AMZN","META","GOOGL","MSFT","TSLA","AMD","INTC","WMT","CRM","JPM","XOM","CVX","RTX","UNH","JNJ","PFE","NKE","BRK-B","PYPL","CAT"]
    
    with open (f"{path}/small-cap-stocks-stocks.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == "Symbol":
                continue
            else:
                print(f"Ticker:{row[1]} Name:{row[2]}")
                ticker = row[1]
                try:
                    daily_data(ticker)
                    with open (f"{path}/logs/api.txt", "a") as f:
                        f.write(f"Log: Sucessfully gathered data for {ticker} {time.time()}\n")
                except:
                    with open (f"{path}/logs/api.txt", "a") as f:
                        f.write(f"Error: Failed to gather data for {ticker} {time.time()}\n")


"""
    for ticker in tickers:
        try:
            daily_data(ticker)
            with open (f"{path}/logs/api.txt", "a") as f:
                f.write(f"Log: Sucessfully gathered data for {ticker} {time.time()}\n")
        except:
            with open (f"{path}/logs/api.txt", "a") as f:
                f.write(f"Error: Failed to gather data for {ticker} {time.time()}\n")

    print(f"Gathered data for {tickers.__len__()} companies")
"""
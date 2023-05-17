import requests
from datetime import date
import json
import os
from dotenv import load_dotenv

#load environment variables
load_dotenv()

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
    if not os.path.exists(f"data/{ticker}"):
        os.makedirs(f"data/{ticker}")
    
    today = date.today()

    with open(f"data/{ticker}/{today.isoformat()}--News.json", "w") as f:
        f.write(json.dumps(get_news(ticker)))

    with open(f"data/{ticker}/{today.isoformat()}--Price.json", "w") as f:
        f.write(json.dumps(get_price(ticker)))

if __name__ == "__main__":
    tickers = ["FIVN","AMZN","META","GOOGL","MSFT","TSLA","AMD","INTC","WMT","CRM","JPM","XOM","CVX","RTX","UNH","JNJ","PFE","NKE","BRK-B","PYPL","CAT"]

    for ticker in tickers:
        daily_data(ticker) # run this once a day

    print(f"Gathered data for {tickers.__len__()} companies")
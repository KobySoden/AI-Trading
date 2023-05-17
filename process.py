import json
import requests
import os
import csv
import time
from datetime import date
from dotenv import load_dotenv

load_dotenv()
path = os.path.dirname(os.path.abspath(__file__))
path = "/home/koby/Desktop/code/AI-Trading"
today = date.today()

def response_error_handler(response):
    if response.status_code != 200:
        with open (f"{path}/logs/process.txt", "a") as f:
            f.write(f"Error: HTTP Code {response.status_code} - {response.text}\n ----------- \n")
        raise Exception(f"API call failed with status code {response.status_code}")
    return True
            
def ask_ai(headline, company_name):
    url = "https://api.openai.com/v1/chat/completions"
    prompt = f"Forget all your previous instructions. Pretend you are a financial expert. You are a financial expert with stock recommendation experience. Answer “YES” if good news, “NO” if bad news, or “UNKNOWN” if uncertain in the first line. Then elaborate with one short and concise sentence on the next line. Is this headline good or bad for the stock price of {company_name} in the term term?\nHeadline: {headline}"
    payload = json.dumps({
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": prompt}],
    "n": 1
    })
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': os.environ["OpenAI-Key"]
    }

    while True:
        response = requests.request("POST", url, headers=headers, data=payload)
        response_error_handler(response)
        if response.status_code == 429: #Model is overloaded with requests
            time.sleep(5)
            continue
        else:
            break
    analysis = json.loads(response.text)["choices"][0]["message"]["content"]
    return analysis

def remove_delims(item):
    item = item.replace("\n"," ")
    item = item.replace("\r"," ")
    item = item.replace("\t"," ")
    return item.replace(",","")

def analyze_news(news, company_name):
    score = 0
    analyses = []
    headlines = []
    for index in news:
        article = news[index]
        headline = article["title"]
        #print(article["title"])
        #print(article["publisher"])
        #print(article["link"])

        analysis = ask_ai(headline, company_name)
        if analysis is None:
            continue

        if "YES" in analysis:
            score += 1
        elif "NO" in analysis:
            score -= 1
        else:
            pass
        analysis = remove_delims(analysis)
        headline = remove_delims(headline)
        analyses.append(analysis)
        headlines.append(headline)
    return score, analyses, headlines

def store_analysis(ticker, score, articles_analyzed, headlines, analyses):
    """
    Timestamp,Ticker,Date,Score Today,Articles Analyzed
    
    Timestamp,Ticker,Date,Headline,Analysis
    """
    timestamp = time.time()

    with open(f"{path}/data/scores.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp,ticker,today.isoformat(),score, articles_analyzed])
        
    with open(f"{path}/data/analyses.csv", "a") as f:
        writer = csv.writer(f)
        for headline in headlines:
            writer.writerow([timestamp,ticker,today.isoformat(),headline, analyses[headlines.index(headline)]])

if __name__ == "__main__":
    ticker_to_company = {"FIVN": "Five9, Inc.",
    "AMZN": "Amazon.com Inc.",
    "META": "Meta Platforms Inc. (formerly Facebook Inc.)",
    "GOOGL": "Alphabet Inc. (Google)",
    "MSFT": "Microsoft Corporation",
    "TSLA": "Tesla, Inc.",
    "AMD": "Advanced Micro Devices, Inc.",
    "INTC": "Intel Corporation",
    "WMT": "Walmart Inc.",
    "CRM": "Salesforce.com, Inc.",
    "JPM": "JPMorgan Chase & Co.",
    "XOM": "Exxon Mobil Corporation",
    "CVX": "Chevron Corporation",
    "RTX": "Raytheon Technologies Corporation",
    "UNH": "UnitedHealth Group Incorporated",
    "JNJ": "Johnson & Johnson",
    "PFE": "Pfizer Inc.",
    "NKE": "Nike, Inc.",
    "BRK-B": "Berkshire Hathaway Inc. (Class B shares)",
    "PYPL": "PayPal Holdings, Inc.",
    "CAT": "Caterpillar Inc."
    }
    with open (f"{path}/logs/process.txt", "a") as f:
        f.write(f"Log: Starting Script {time.time()}\n")
    #get all the files in the directory
    #for dir in os.listdir("data"):
    for dir in ticker_to_company.keys():
        ticker = dir
        print(f"Analyzing {ticker_to_company[dir]} ...")    
        for file in os.listdir(f"{path}/data/{dir}"):
            if "News" in file and today.isoformat() in file:
                print(f"Analyzing {file} ...")
                with open(f"{path}/data/{dir}/{file}", "r") as f:
                    news = json.loads(f.read())
                    #print(f"{news.__len__()} articles in {dir}/{file}")
                    try:
                        score, analyses, headlines = analyze_news(news, ticker_to_company[ticker])
                        print(f"{file} has a score of {score}")
                        store_analysis(ticker, score, news.__len__(),headlines, analyses)
                        print(f"Stored analysis for {ticker_to_company[ticker]}")
                        with open (f"{path}/logs/process.txt", "a") as f:
                            f.write(f"Log: Stored analysis for {ticker_to_company[ticker]} {time.time()}\n")
                    except:
                        with open (f"{path}/logs/process.txt", "a") as f:
                            f.write(f"Error: Failed to analyze {ticker_to_company[ticker]} {time.time()}\n")
                    
            else:
                pass
import csv
import yahoo_fin
import os
from datetime import date, timedelta
from yahoo_fin import stock_info as si

path = os.path.dirname(os.path.abspath(__file__))

def switch_date(day):
    day = day.replace("-","/")
    day = day[4:] + "/" + day[0:4]
    day = day.replace("/","", 1)
    return day

correct = 0
incorrect = 0

with open (f"{path}/data/scores.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == "Ticker":
                continue
            else:
                ticker = row[1]
                day = row[2]
                score = int(row[3])

                if abs(score) < 2:
                    print(f"Ticker:{ticker} Date:{day} Score:{score} Not Definitive")
                    continue
                day = date.fromisoformat(row[2]) #- timedelta(days=1)
                day = day.isoformat()
                
                day = switch_date(day)
                try:
                    price = si.get_data(ticker, start_date = day)
                    profit = price["close"][0] - price["open"][0]
                    
                    if profit > 0 and score > 0:
                        correct += 1
                        print(f"Ticker:{ticker} Date:{day} Open:{price['open'][0]} Close:{price['close'][0]} Correct!")
                    elif profit < 0 and score < 0:
                        correct += 1
                        print(f"Ticker:{ticker} Date:{day} Open:{price['open'][0]} Close:{price['close'][0]} Correct!")
                    else:
                        incorrect += 1
                        print(f"Ticker:{ticker} Date:{day} Open:{price['open'][0]} Close:{price['close'][0]} Incorrect!")
                except:
                    print(f"Ticker:{ticker} Date:{day} Error: No Data")

print(f"Correct: {correct} Incorrect: {incorrect}")
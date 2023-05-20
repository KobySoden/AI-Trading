import csv

with open("small-cap-stocks-stocks.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        print(f"Ticker:{row[1]} Name:{row[2]}")
from io import StringIO
import requests
import pandas as pd
from datetime import datetime, timedelta
import bs4
import csv
import os

session = requests.session()

headers = {
    "user-agent": "Chrome/87.0.4280.88"
}
head = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/87.0.4280.88 Safari/537.36 "
}

def getDataSpecifyDate(company, from_date=(datetime.today().strftime("%d-%m-%Y")), to=(datetime(datetime.today().year - 1, datetime.today().month,datetime.today().day).strftime("%d-%m-%Y"))):
    session.get("https://www.nseindia.com", headers=head)
    session.get("https://www.nseindia.com/get-quotes/equity?symbol=" + company, headers=head)
    session.get("https://www.nseindia.com/api/historical/cm/equity?symbol=" + company, headers=head)
    url = "https://www.nseindia.com/api/historical/cm/equity?symbol=" + company + "&series=[%22EQ%22]&from=" + from_date + "&to=" + to + "&csv=true"
    data = session.get(url=url, headers=head)
    df = pd.read_csv(StringIO(data.text[3:]))
    return df



def getDataOfOneYear(varient, from_date = ((datetime(datetime.today().year - 1, datetime.today().month, datetime.today().day) + timedelta(days=2)).strftime("%d-%m-%Y")), to_date =(datetime.today().strftime("%d-%m-%Y"))):
    varient = varient.upper()
    varient = varient.replace(' ', '%20')
    varient = varient.replace('-', '%20')
    url="https://www1.nseindia.com/products/dynaContent/equities/indices/historicalindices.jsp?indexType=" + varient + "&fromDate=" + from_date + "&toDate=" + to_date
    data = session.get(url=url, headers=head)
    soup = bs4.BeautifulSoup(data.text, 'html5lib')
    df = pd.read_csv(StringIO(soup.find('div', {'id': 'csvContentDiv'}).contents[0].replace(':','\n')))
    return df

def makeDataset(url):
    with open("dataset.csv", "w") as f:
        f.write(session.get(url).text)

    with open("dataset.csv", "r") as f:
        dataset = csv.reader(f)
        niftyData = []
        stockData = []

        for idx, row in enumerate(dataset):
            if 8 <= idx <= 72:
                niftyData.append(row)
            if 126 <= idx:
                stockData.append(row)
    os.remove("dataset.csv")
    return pd.DataFrame(niftyData), pd.DataFrame(stockData)



def getTodayData() -> object:
    data = session.get(url="https://www.nseindia.com/api/merged-daily-reports?key=favCapital", headers=headers)
    return makeDataset(data.json()[1]['link'])


# nifty_data, companies_data = getTodayData()
# print(nifty_data.tail())
# print(companies_data.tail())
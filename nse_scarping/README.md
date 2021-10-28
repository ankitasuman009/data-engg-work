# WebSite-Url : https://www.nseindia.com/


## getID.py

- getId function takes company name as an argument.
- Fetch the company symbol from url into search_results variable.
- Fetch the further details of the company into company_details variable.
- Return the identifier or ID of it.

## getData.py

- Three functions are defined here : getDataSpecifyDate(), getDataOfOneYear(), and getTodayData(). They all return data in dataframe.
- getDataSpecifyDate() will return data of a company of certain interval. Takes three argument: company_name, from_date and to_date.
- getDataOfOneYear() will return data of a comany of one year. Takes three argument: company_name, from_date(by default set to one year ago from the current date), and to_date(by default set to the current date)
- getTodayData() will return two dataframes, data of nifty data and stock data of current date.

## live_data.py

- companies_getLiveData(company_id) or nifty_getLiveData(nifty_type) to get live data i.e., from 09:00:00 AM to till now.
- user-agents ref https://oxylabs.io/blog/5-key-http-headers-for-web-scraping#link-user-agent

## nifty50.py

- a dummy code that gets company data of one year and save it into a csv file

## resampling.py

- read the csv file
- change the datatype of Date column into datetime
- set index column to Date column value
- resampled the data and store it into another dataframe df2.
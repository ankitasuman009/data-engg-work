from getData import getDataSpecifyDate

companies_data = getDataSpecifyDate('SHREECEM',from_date='30-04-2020',to='30-04-2021')

# print(companies_data.head())

companies_data.to_csv("one_year_data.csv")
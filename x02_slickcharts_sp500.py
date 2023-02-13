# scraper template


from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date

today = date.today()             # 2022-12-27
yymmdd = today.strftime("%y%m%d")  # 221227

# Step 01. request a URL
req = Request(
    url='https://www.slickcharts.com/sp500',
    headers={'User-Agent': 'Mozilla/5.0'}
)

# Step 02. save the webpage
webpage = urlopen(req).read()

# Step 03. format using beautiful soup
soup = BeautifulSoup(webpage, features="lxml")

# Step 04. find a table
table = soup.find('table')  # Find the table

# Step 05. extract elements
header = []                 # Init header list
rows = []                   # Init rows

# Iterate through all the table rows
# First row is the header
for i, row in enumerate(table.find_all('tr')):
    if i == 0:
        header = [el.text.strip() for el in row.find_all('th')]
    else:
        rows.append([el.text.strip() for el in row.find_all('td')])



# Step 06. copy the table into a dataframe
# Copy the rows and header into the dataframe
df = pd.DataFrame(rows, columns=header)

# Step 07. more processing
# Replace tickers with dots to dash to prevent error in yfinance download
tickers = [
    ticker.replace('.', '-')
    for ticker in df['Symbol'].unique().tolist()
]

# Save sp500 list
df0 = pd.DataFrame(tickers)               # Create dataframe from  series
df0.rename(columns = {0: 'Symbol'}, inplace=True)       # Rename/assign first column to new colname
df0.to_csv('data\sp500.csv')              # Save to csv


# Save all columns to CSV
df.to_csv('data\sp500_slickcharts.csv')

# Mangle the dataframe
df1 = df.drop(columns = ['#', 'Company', 'Weight', 'Price', 'Chg'])     # drop unwanted columns
df1['% Chg'] = df1['% Chg'].map(lambda x: x.lstrip('(').rstrip('%)'))   # remove non-numeric chars
df1['% Chg'] = df1['% Chg'].astype(float)                               # convert to float
# Save daily data
df1.to_csv(f'data\sp500_slickcharts_{yymmdd}.csv')          # df save to csv

print(f"Today: {yymmdd}")
print("\n Biggest Winners")
print(df1.sort_values(by='% Chg', ascending=False).head())  # df sort values
print("\n Biggest Losers")
print(df1.sort_values(by='% Chg', ascending=False).tail())





exit(0)






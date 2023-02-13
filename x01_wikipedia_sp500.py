import pandas as pd

#

INFOFILE = r'data\wikipedia_sp500.csv'

# Get list of sp 500  from wikipedia
html_tables = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
df = html_tables[0]  # get first html table from url to dataframe
print(df)
print(df.columns)
print(df.shape)
df.to_csv(INFOFILE)
print(f"INFOFILE : {INFOFILE}\n")

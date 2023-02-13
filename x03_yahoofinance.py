"""
https://wire.insiderfinance.io/how-to-collect-finance-news-data-45e82e4a4b9c
https://github.com/peiyingchin/Medium/blob/main/Extract%20finance%20news%20data/Scrap%20finance%20news%20data.ipynb


"""
import datetime
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
from datetime import date
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests

# create a driver
driver = webdriver.Chrome(ChromeDriverManager().install())

# link to extract
driver.get("https://finance.yahoo.com/")

# set a scroll limit
scroll_limit = 160

# set count, to count how many times we scroll
count = 0

# assign a dummy to new height
new_height = 0

# break if we scroll less than scroll limit defined
while True and count < scroll_limit:

    # give 15 second to make sure all page load
    time.sleep(15)

    # to get the height of our document
    height = driver.execute_script("return document.documentElement.scrollHeight")

    # if new height = height obtain, we should break the while loop
    if new_height == height:
        break

    # now new height is the height now
    new_height = height
    # execute script to scrol until end of height
    driver.execute_script("window.scrollTo(0, " + str(height) + ");")

    # count our scroll limit
    count += 1
time.sleep(10)

page = driver.page_source
driver.close()

# parse our page to html parser using beautiful soup
soup = BeautifulSoup(page,"html.parser")
# obtain the header table
tabl = soup.find_all("li" , {"class" : "js-stream-content Pos(r)"})

header = []
category =[]
link =[]
val=0
for i in tabl:
    val+=1
    header_value = i.findAll('div')[0].findAll('div')[0].findAll('h3')[0].text
    link_value = i.findAll('a',href=True)[0]['href']
    if len(i.findAll('div')[0].findAll('div')[0])>=3:
        category_value =i.findAll('div')[0].findAll('div')[0].findAll('div')[3].text
    else:
        source_value ='NA'
    header.append(header_value)
    category.append(category_value)
    link.append(link_value)

    # process the data
df = pd.DataFrame({'header': header, 'category': category, 'link': link})
# remove advertisement
remove_ads = df[df['category'] != 'NA']

#fix link infront the link we extract
fix_link = 'https://finance.yahoo.com'

# row by row to extract the link and get our article content
for i in range(remove_ads.shape[0]):
    header = remove_ads.header[i:i+1].values[0]
    url = fix_link+remove_ads.link[i:i+1].values[0]
    # get page content
    page = requests.get(url, allow_redirects=True)
    if (page.status_code == 200):
        page_content = page.content
        soup = BeautifulSoup(page_content,"html.parser")
        remove_ads.loc[remove_ads['header']==header,'article_content'] = soup.findAll('div',{'class':'caas-body'})[0].text

remove_ads.to_csv(r'Your Path'+str(date.today())+'.csv',index=False)



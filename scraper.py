import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import string
import re
import datetime
import sqlite3
import time

all_links = []
location = []
date = []
e_name = []





def scrape_data():

        data = requests.get("http://ufcstats.com/statistics/events/upcoming")
        soup = BeautifulSoup(data.text, 'html.parser')
        table = soup.find('table', {"class": "b-statistics__table-events"})
        links = table.find_all('a', href=True)

        for link in links:
            all_links.append(link.get('href'))

        for link in all_links:
            print(f"Now currently scraping link: {link}")

            data = requests.get(link)
            soup = BeautifulSoup(data.text, 'html.parser')
            time.sleep(1)

            h2 = soup.find("h2")
            e_name.append(h2.text.strip())

            box_item = soup.find('ul',{'class': "b-list__box-list"})
            box_item = box_item.find_all('li')

            place = box_item[1].text.strip().strip("Location:").strip()
            location.append(place)

            d = box_item[0].text.strip().strip("Date:").strip()
            date.append(d)

    

        return None

#preprocessing
# remove rows where DOB is null
# impute stance as orthodox for missing stances
def create_df():
    #create empty dataframe
    df = pd.DataFrame()

    df["Event"] = e_name
    df["Date"] = date
    df["Location"] = location


    return df

scrape_data()
df = create_df()
print("Scraping completed")

conn = sqlite3.connect('data.sqlite')
df.to_sql('data', conn, if_exists='replace')
print('Db successfully constructed and saved')
conn.close()

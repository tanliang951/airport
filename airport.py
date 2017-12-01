#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 04:53:06 2017

@author: RockyYeung
"""

import bs4
import requests
import pandas as pd
import string


AZ = list(string.ascii_uppercase)
tempURL = "https://en.wikipedia.org/wiki/List_of_airports_by_IATA_code:_{}"
first = True

for alpha in AZ:
    print("parsing", alpha)
    url = tempURL.format(alpha)
    page = requests.get(url).text
    soup = bs4.BeautifulSoup(page, 'lxml')
    tables = soup.find_all("table")
    assert len(tables) == 2
    # the first one is what we need
    dfs = pd.read_html(str(tables), header=0)
    df = dfs[0]
    assert "IATA" in df.columns.values
    assert "ICAO" in df.columns.values
    assert u'Airport\xa0name' in df.columns.values

    
    # filter
    flt = df['IATA'].str.contains("-[A-Za-z]{2}-")
    df_clean = df[~flt]

    # snap shoot the dataframe
    #print(df_clean.head())    

    if first:
        grand_df = df_clean
        first = False
    else:
        grand_df = grand_df.append(df_clean)

grand_df.sort_values(by=["IATA"], inplace=True)
grand_df.to_csv("~/Desktop/Airport_codes.csv", index=False)

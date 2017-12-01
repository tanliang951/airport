#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 13:41:53 2017

@author: RockyYeung
"""

from selenium_scrape import fly
from itertools import combinations
import pandas as pd

df = pd.read_csv("/Users/RockyYANG/Desktop/game/major_us_airports_final.csv", header=0)
# sort the aiports by enplanement amounts descendingly
df.sort_values(by=['Enplanements'], inplace=True, ascending=False)
names = list(df['City'])

codes = list(df['IATA'])
codes = codes[:15]
print("IATA of airports to check:")
print(codes)
print()

airports = list(zip(names, codes))
# short list the airports
date = "12/01/2017"

dataset = []
for dept, arrv in combinations(codes, 2):
    print("Checking from {} to {}".format(dept, arrv))
    data = fly(dept, arrv, date)
    dataset.append({
            'meta': {'dept': dept, 'arrv': arrv, 'date': date},
            'flights': data # a list
            })
    
m = []
for pair in dataset:
    meta = pair['meta']
    dept = meta['dept']
    arrv = meta['arrv']
    date = meta['date']
    
    flights = pair['flights']
    for f in flights:
        row = [dept, arrv, date] + [f[key] for key in f]
        m.append(row)

df = pd.DataFrame(data=m, columns=['dept', 'arrv', 'date']+ list(f.keys()))
df.to_csv("/Users/RockyYANG/Desktop/game/results.csv")
        
        
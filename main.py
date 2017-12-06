#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 13:41:53 2017

@author: RockyYeung
"""

from expedia import parse
import itertools
import pandas as pd

df = pd.read_csv("/Users/RockyYANG/Desktop/game/major_us_airports_final.csv", header=0)
# sort the aiports by enplanement amounts descendingly
df.sort_values(by=['Enplanements'], inplace=True, ascending=False)
names = list(df['City'])

codes = list(df['IATA'])
codes = [c.lower() for c in codes]
codes = codes[:10]
print("IATA of airports to check:")
print(codes)
print()

# short list the airports
date = "01/01/2018"
print('Date:', date)

dataset = []
total = len(list(itertools.permutations(codes, 2)))
print('In total',total , 'to search')
counter = 1
for dept, arrv in itertools.permutations(codes, 2):
    print('Complete:', "{0:.0f}%".format(counter/total* 100))
    counter += 1
    print("Checking from {} to {}".format(dept, arrv))
    data_scraped = parse(dept, arrv, date)
    print(len(data_scraped), 'flights found.')
    print('------------')
    dataset.append({
            'ftd': {'dept': dept, 'arrv': arrv, 'date': date},
            'flights': data_scraped # a list
            })
    
m = []
for pair in dataset:
    meta = pair['ftd']
    dept = meta['dept']
    arrv = meta['arrv']
    date = meta['date']
    flights = pair['flights']
    for f in flights:
        row = [dept, arrv, date] + [f[key] for key in f]
        m.append(row)

df_out = pd.DataFrame(data=m, columns=['dept', 'arrv', 'date']+ list(f.keys()))
df_out.to_csv("/Users/RockyYANG/Desktop/game/data/usa.csv")
        
        
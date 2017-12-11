#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 13:41:53 2017

@author: RockyYeung
"""

from expedia import parse
import pandas as pd

#date = "01/01/2018"

keys = ['total distance',
        'ticket price',
        'departure',
        'arrival',
        'flight duration',
        'airline',
        'plane',
        'departure_airport',
        'departure_time',
        'arrival_airport',
        'arrival_time',
        'plane code',
    ]

task_file = input("Input full path to task file: ")
date = input("Input date: ")
df = pd.read_csv(task_file, header=0)

depts = [c.lower() for c in list(df['dept'])]
arrvs = [c.lower() for c in list(df['arrv'])]
dept_arrv_tuple_list = list(zip(depts, arrvs))

dataset = []

counter = 0
total = len(dept_arrv_tuple_list)
for dept, arrv in dept_arrv_tuple_list:
    print('Complete:', "{0:.0f}%".format(counter/total* 100))
    counter += 1
    print("Checking from {} to {}".format(dept, arrv))
    
    data_scraped = parse(dept, arrv, date, display_url=True)
    print(len(data_scraped), 'flights found in this route.')
    dataset.append({'dept': dept,
            'arrv': arrv,
            'date': date,
            'flights': data_scraped})
            #a list
m = []
for data in dataset:
    dept = data['dept']
    arrv = data['arrv']
    date = data['date']
    flights = data['flights']
    for f in flights:
        row = [dept, arrv, date] + [f[key] for key in keys]
        m.append(row)

df_out = pd.DataFrame(data=m, columns=['dept', 'arrv', 'date']+keys)
fout_path = "csv/results.csv"
print('The data is write to', fout_path)
df_out.to_csv(fout_path)
        
        
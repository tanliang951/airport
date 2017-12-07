#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 13:41:53 2017

@author: RockyYeung
"""

from expedia import parse
import pandas as pd

#date = "01/01/2018"

task_number = input('Input your task number, 0-3: ')
task_file = 'csv/task_split_{}.csv'.format(task_number)
date = input("Input date: ")
df = pd.read_csv(task_file, header=0)

depts = list(df['dept'])
arrvs = list(df['arrv'])
dept_arrv_tuple_list = list(zip(depts, arrvs))

dataset = []

counter = 0
total = len(dept_arrv_tuple_list)
for dept, arrv in dept_arrv_tuple_list:
    print('Complete:', "{0:.0f}%".format(counter/total* 100))
    counter += 1
    print("Checking from {} to {}".format(dept, arrv))
    
    data_scraped = parse(dept, arrv, date)
    print(len(data_scraped), 'flights found.')
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
fout_path = "csv/results.csv"
print('The data is write to', fout_path)
df_out.to_csv(fout_path)
        
        
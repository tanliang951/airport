#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 15:18:26 2017

@author: RockyYeung
"""
out = open('/Users/RockyYANG/Desktop/game/major.csv', 'w')

with open('/Users/RockyYANG/Desktop/game/major_us_airports_1.csv') as f:
    first_line = True
    for line in f:
        if first_line:
            first_line = False
            out.write(line)
        else:
            l = line.split(',')
            l[-1] = l[-1].replace('\",', '')
            out.write(','.join(l))

out.close()
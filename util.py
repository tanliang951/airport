#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 18:05:27 2017

@author: RockyYeung
"""

import model
import numpy as np

"""
Spatial Lattice shape (101, 101)
D at position (50, 50), purely symetric
"""
def produce_one_D_in_center101x101(b):
    m = []
    for i in range(101):
        line = []
        for j in range(101):
            if (i, j) != (50, 50): # insert a Cooperator
                line.append(model.Player(model.Type.Cooperator, b))
            else: # insert a Defector at position (50, 50)
                line.append(model.Player(model.Type.Defector, b))
        m.append(line)
    board = model.Lattice.from_matrix(m)
    return board


def t2a(t):
    if t == model.Type.Defector:
        return "D"
    else:
        return "C"

def random_type(gama):
    if (np.random.rand() <= gama):
        return model.Type.Cooperator
    else:
        return model.Type.Defector

def produce_half_half_board(b):
    m = []
    for i in range(50):
        line = []
        for j in range(100):
            line.append(model.Player(model.Type.Defector, b=b))
        m.append(line)
    for i in range(50, 100):
        line = []
        for j in range(100):
            line.append(model.Player(model.Type.Cooperator, b=b))
        m.append(line)
    
    board = model.Lattice.from_matrix(m)
    return board
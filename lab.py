#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 10:28:21 2017

@author: RockyYeung
"""

from model import Lattice
import numpy as np
import matplotlib.pyplot as plot
#
#b_range = np.arange(1.3, 2.2, 0.05)
#y = []
#
#for b in b_range:
#    print('b=', b)
#    board = Lattice(shape=(100, 100), gama=0.8, b=b)
#    for i in range(100):
#        board.update()
#    gen_record = board.generation_record
#    fcs = [g[1] for g in gen_record]
#    stable_fcs = fcs[-5:]
#    y.append(np.average(stable_fcs))
#
#plot.plot(b_range, y, )
#plot.xlabel('b')
#plot.ylabel('The stable fraction of Cooperators')


"""
layer
"""
layers = [1, 2, 3]
b_range = np.arange(1.3, 2.2, 0.05)
y_layer = {1: [], 2:[], 3:[]}

for layer in layers:
    for b in b_range:
        print('b=', b, 'layer=', layer)
        board = Lattice(shape=(100, 100), gama=0.8, b=b)
        for i in range(100):
            board.update(layer=layer) # layer update
        gen_record = board.generation_record
        fcs = [g[1] for g in gen_record]
        stable_fcs = fcs[-5:]
        eqmfc = np.average(stable_fcs)
        y_layer[layer].append(eqmfc)

plot.plot(b_range, y_layer[1], label='1-layer')
plot.plot(b_range, y_layer[2], label='2-layer')
plot.plot(b_range, y_layer[3], label='3-layer')
plot.legend(loc='best')
plot.xlabel('b')
plot.ylabel('The stable fraction of Cooperators')
plot.savefig('/Users/RockyYANG/Desktop/game/layers.png', dpi=300)


#brange = np.arange(1, 3, 0.05)
#shape = (100, 100)
#generations = 100
#
#x = []
#y = []
#
#final_stable_frac_c_doubleb = dict(b1_3= [], b1_85= [])
#gama_range = np.arange(0.2, 1, 0.05)
#
#
#for b in [1.3, 1.85]:
#    for gama in gama_range:
#        print('b={}, gama={}'.format(round(b, 3), round(gama, 3)))
#        board = Lattice(shape=shape, gama=gama, b=b)
#        if gama == 0.3:
#            igen = generations
#        else:
#            igen = generations + 100 # evolve for 200 rounds
#        for g in range(igen):
#            board.update()
#        board.plot_figure()
#        board.figure.savefig("/Users/RockyYANG/Desktop/game/pics/gama/final_distribution_gama={}b={}.png".format(round(gama, 3), round(b, 3)))
#        plot.close(board.figure)
#        record = board.generation_record
#        rx = [i[0] for i in record]
#        ry = [i[1] for i in record]
#        f = plot.figure()
#        plot.plot(rx, ry, label='fc(t), b={}'.format(b))
#        plot.xlabel('Time (generation)')
#        plot.ylabel('Percentage')
#        plot.savefig('/Users/RockyYANG/Desktop/game/pics/gama/prc_gama={}b={}.png'.format(round(gama, 3), round(b, 3)))
#        plot.close(f)
#        # average the recent 5 generation to get the stable fraction of c
#        stable = ry[-5:]
#        if b == 1.3:
#            final_stable_frac_c_doubleb['b1_3'].append(np.average(stable))
#        else:
#            final_stable_frac_c_doubleb['b1_85'].append(np.average(stable))
#    
#f = plot.figure()
#plot.plot(list(gama_range), final_stable_frac_c_doubleb['b1_3'], label='eqm. fc(b={})'.format(1.3))
#plot.plot(list(gama_range), final_stable_frac_c_doubleb['b1_85'], label='eqm. fc(b={})'.format(1.85))
#plot.xlabel('Gamma')
#plot.ylabel('The stable fraction of Cooperators')
#plot.legend(loc='best')
#f.savefig('/Users/RockyYANG/Desktop/game/pics/gama/stable_frac_c_against_initial_gama.png', dpi=300)
#plot.show()

#f = plot.figure()
#plot.plot(x, y, label="Equilibrium proportion of cooperators")
#plot.xlable('b')
#plot.ylabel('fc')
#plot.legend(loc='best')
#plot.show()

#b = Lattice(shape=(100, 100), gama=0.8, b=1.85)
#for i in range(100):
#    b.update()
#
#gen_record = b.generation_record
#x = [g[0] for g in gen_record]
#y = [g[1] for g in gen_record]
#plot.plot(x, y)
#plot.xlabel('Time (generation)')
#plot.ylabel('Fraction of Cooperators')
#b.figure.savefig('/Users/RockyYANG/Desktop/game/after300genration.png', dpi=300)
#plot.savefig('/Users/RockyYANG/Desktop/game/evolve100gama0.8b1.85.png', dpi=300)
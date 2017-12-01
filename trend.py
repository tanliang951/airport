#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 00:04:51 2017

@author: RockyYeung
"""


import pandas as pd
from model import Lattice, Player, Type
import matplotlib.pyplot as plot
import util
import matplotlib.style as style
import itertools
import numpy as np
style.use("ggplot")

"""
xr (tuple): the start of x, the end of x
yr (tuple): the start of y, the end of y
"""
def view_part(board, num_gen, xr, yr):
    m = []
    xrange = range(*xr)
    yrange = range(*yr)
    for x in xrange:
        line = []
        for y in yrange:
            info = board.info_at_position_dict(x, y)
            line.append("{}<-{}, s({:.2f})".format(util.t2a(info['t']), util.t2a(info['pt']) ,info['score']))
            m.append(line)
    df = pd.DataFrame(m, columns=list(yrange), index=list(xrange))
    print(df)


def view_frac_c_trend(board, num_gen):
    for i in range(num_gen):
        board.update()
    # retrive generation record
    gr = board.generation_record
    x, y = zip(*gr)
    plot.plot(x, y, label="The fraction of Cooperators")
    plot.xlabel("Time (generations)")
    plot.ylabel("Percentage")
    plot.show()
    
    
# one Defector invading an infinite array of Cooperators
# The spatial lattice is constructed with exactly symetric shape
# so that the evolving pattern is symetric at any generation
def view_one_D_invading_C(numgen, b):
    board = util.produce_one_D_in_center101x101(b)
    for i in range(numgen):
#        print("At generation", i)
        board.update()
    x, y = zip(*board.generation_record)
    plot.plot(x, y, label="The fraction of Cooperators")
    plot.legend(loc="best")
    plot.xlabel("Time (generations)")
    plot.ylabel("Percentage")
    plot.show()

view_one_D_invading_C(100, 1.85)

#class ReplicatorLattice(Lattice):
#    def update(self):
#        frac_c = self.get_fraction_of_cooperators()
#        frac_d = 1 - frac_c
#        coords = list(itertools.product(range(self.shape[0]), range(self.shape[1])))
#        avg = np.average([self.grid[x][y].score for x, y in coords])
#
#        for i in range(self.shape[0]):
#            for j in range(self.shape[1]):
#                player = self.grid[i][j]
#                myscore = player.score
#                player.previous_type = player.type
#                player.pending_type = None


        
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 21:54:40 2017

@author: RockyYeung
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 18:09:56 2017

@author: RockyYeung
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style
import enum
import copy
import util


# game map: 200 * 200


"""
Payoff table
      C    D
C     1,1  0,b
D     b,0  0,0


b is the only variable, it is the betray payoff
"""
# use ggplot
matplotlib.style.use("ggplot")

# seed to zero
np.random.seed(0)

class Type(enum.Enum):
    Cooperator = enum.auto()
    Defector = enum.auto()
    Undefined = enum.auto()

class Lattice:
    """
    shape (tuple)
    gama (float): the fraction of cooperator in the population
    b (float): the floating payoff variable
    
    Default to randomly initiate the population as having gama fraction (exact)
    as Cooperators and the rest are Defectors. The distrution is symetric.
    """
    
    def __init__(self, shape, **kwargs):

        self.grid = list()
        self.shape = shape
        self.figure = plt.figure() # place holder of figure
        self.generation_record = []
        self.current_generation = 0
        
        # gama init, randomization with a initial fraction of type C
        if ('gama' in kwargs and 'b' in kwargs):
            gama = kwargs['gama']
            b = kwargs['b']
            players = Lattice.gen_players(gama=gama, total=self.shape[0]*self.shape[1], b=b)
            for i in range(self.shape[0]):
                line = []
                for j in range(self.shape[1]):
                    line.append(players.pop()) # try at b=1.8
                    self.grid.append(line)
            self.update_generation_record()
    
    @staticmethod
    def gen_players(gama, total, b):
        numC = int(gama*total)
        numD = total - int(gama*total)
        players = []
        # do not use multiplication! it copy reference to the same object
        for i in range(numC):
            players.append(Player(Type.Cooperator, b))
        for i in range(numD):
            players.append(Player(Type.Defector, b))
        np.random.shuffle(players)
        return players
    
    """
    Return whether this coordinate is on border
    """
    def is_on_border(self, x, y):
        if x == 0 or x == self.shape[0]-1 or y == 0 or y == self.shape[1]-1:
            return True
        return False
    
    """
    The matrix of the players distribution
    """
    
    @classmethod
    def from_matrix(cls, m):
        shape = (len(m), len(m[0]))
        board = cls(shape=shape)
        # manually
        for i in range(shape[0]):
            line = []
            for j in range(shape[1]):
                line.append(copy.copy(m[i][j]))
            board.grid.append(line)
        
        assert (len(board.grid), len(board.grid[0])) == shape
        # update generation record
        board.update_generation_record()
        return board
        

    def __getitem__(self, key):
        return self.grid[key]
    
    def plot_figure(self): # update the figure member
        def t2num(t): # 1 for C, 0 for D
            if t == Type.Cooperator:
                return 1
            else:
                return 0
        
        m = []
        for i in range(self.shape[0]):
            l = []
            for j in range(self.shape[1]):
                l.append(t2num(self[i][j].type))
            m.append(l)
        plt.clf()
        plt.pcolor(m, cmap='RdBu')
        plt.colorbar()
                
    
    """
    Return the adjance cells (including itself)
    3 to 9 cells
    """
    def get_neighbours(self, x, y):
        n = []
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                # check bounds
                if i >= 0 and i < self.shape[0] and j >= 0 and j < self.shape[1]:
                    n.append(self.grid[i][j])
        return n
    
    
    """
    function should take two integers as input and return nothing
    """
    def map_to(self, func):
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                func(i, j)
    
    def update(self):
        # record alter count
        # conduct interactions and update scores        
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                player = self.grid[i][j]
                # play with itself, also
                player.play_with_neighbours(nbs=self.get_neighbours(i, j))

        # decide the cell's owner again
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                this_p = self.grid[i][j]
                nbs = self.get_neighbours(i, j)
                # find out the maximum scores and update this cell's type to
                # the best performing neighbor's type
                scores = [p.score for p in nbs]
                maxIdx = scores.index(max(scores))
                this_p.previous_type = this_p.type # save current type
                this_p.pending_type = nbs[maxIdx].type # pending the status
        # refresh
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                self.grid[i][j].type = self.grid[i][j].pending_type
                self.grid[i][j].pending_type = Type.Undefined
        
        # update the generation record
        self.update_generation_record()
    
    def info_at_position(self, x, y):
        p = self.grid[x][y]

        return "<{t}, prv. {tp}, ({x}, {y}), {s:.2f}>".format(t=util.t2a(p.type),
                        tp=util.t2a(p.previous_type), x=x, y=y, s=p.score)
    def info_at_position_dict(self, x, y):
        p = self.grid[x][y]
        return dict(t=p.type, pt=p.previous_type, co=(x, y), score=p.score)
    
    def update_generation_record(self):
        self.generation_record.append((self.current_generation, self.get_fraction_of_cooperators()))
        self.current_generation += 1
    
    def get_fraction_of_cooperators(self):
        C_count = 0
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                if self[i][j].type == Type.Cooperator:
                    C_count += 1
        return C_count / (self.shape[0]*self.shape[1])
    
        
class Player:
    """
    object elements:
        score (float): The score this player gains in this round
    """
    
    """
    type (Type):
    """
    
    def __init__(self, _type, b):
        self.score = 0
        self.type = _type
        self.previous_type = Type.Undefined
        # the temporary holder for type that is going to be applied
        self.pending_type = Type.Undefined
        self.b = b
    
    
    def match(self, aPlayer):
        if self.type == Type.Cooperator:
            if aPlayer.type == Type.Cooperator:
                return 1 # C matches C
            else:
                return 0 # C matches D
        else:
            if aPlayer.type == Type.Cooperator:
                return self.b # D matches C
            else:
                return 0 # D matches D
                
                
    """
    nbs (list): a list of neighbours (8)
    """
    def play_with_neighbours(self, nbs):
        # play with each neighbour
        gains = []
        for player in nbs:
            gains.append(self.match(player))
        # average the gains, update it to self.score
        self.score = np.average(gains)
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        if self.type == Type.Cooperator:
            return "C({:.2f})".format(self.score)
        else:
            return "D({:.2f})".format(self.score)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 21:55:05 2017

@author: RockyYeung
"""

# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/	

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import model
import tkinter as tk
from tkinter import ttk
import util

def print_hello():
    print("Hello, world")

class Viewer(tk.Frame):
    def __init__(self, parent, board):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.board = board
        self.canvas = FigureCanvasTkAgg(self.board.figure, self)
        self.init_figure()
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        button = ttk.Button(self, text="Start", command=self.start_evolve)
        button.pack()        
        label = tk.Label(self, text="Red stands for defector\nBlue stands for cooperator")
        label.pack()
        self.pack()
    
    def init_figure(self):
        self.board.plot_figure()
        
    def start_evolve(self):
        for i in range(100): # evolve 100 generation
            print("At generation", i)
            self.board.update()
            self.board.plot_figure() # update the figure object
            self.canvas.draw() # redraw the canvas
            self.update() # update the frame
b = model.Lattice(shape=(100, 100), gama=0.8, b=1.85)
root = tk.Tk()
root.title("View the Evolution")
Viewer(root, b)
root.mainloop()
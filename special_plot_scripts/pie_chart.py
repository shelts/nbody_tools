#! /usr/bin/python
#/* Copyright (c) 2018 Siddhartha Shelton */

import os
import subprocess
from subprocess import call
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math as mt
import matplotlib.patches as mpatches



def piechart():
    labels = 'Mass Cost', 'Geometry', 'Dispersion'
    sizes = [120, 120, 120]
    colors = ['red', 'yellow', 'cyan']
    explode = (0.0, 0, 0, 0)  # explode 1st slice
    fig = plt.figure(facecolor='b', edgecolor='k')
    fig.patch.set_facecolor('grey')

    plt.pie(sizes, colors=colors, shadow=False, startangle=140)
    plt.axis('equal')
    plt.savefig('/home/sidd/Desktop/research/quick_plots/publish_plots/piechart.png', format='png')



piechart()
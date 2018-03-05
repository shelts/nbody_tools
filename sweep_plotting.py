#! /usr/bin/python
#/* Copyright (c) 2016 Siddhartha Shelton */
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from nbody_functional import *
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                #/# # # # # # # # # # # # # # \#
                #          Control Panel       #
                #\# # # # # # # # # # # # # # /#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
y = True
n = False
plot_1D = y
plot_2D = n

path = '/home/sidd/Desktop/research/'
folder = path + "like_surface/"
name_of_sweeps = '_beta_dispersions'
#name_of_sweeps = '_2d'

oneD_names   = ['ft', 'r', 'rr', 'm', 'mr']

twoD_names   = ['rr_mr']

correct = [3.95, 0.2, 0.2, 12, 0.2]
ranges  = [ [2.0, 6.0],  \
            [0.1, 1.3],  \
            [0.1, .95],  \
            [1., 120.0], \
            [.1, .95],   \
          ]   
plot_dim = [0, 5]

plot_dim2 = [4, 5]

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                #/# # # # # # # # # # # # # # \#
                #          Engine Room         #
                #\# # # # # # # # # # # # # # /#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # #
#    One Dimensional Surface Sweep Func   #
# # # # # # # # # # # # # # # # # # # # # #

def oneD_plot():
    titles  = ['Backward Evolve Time (Gyr)',  'Baryon Scale Radius (kpc)', r'Scale Radius Ratio ($R_{B}/(R_{B}+R_{D})$)', 'Baryonic Mass (SMU)',  'Mass Ratio (Baryonic/Total)']
    plot_corr = 231
    l = -200
    plt.figure(figsize=(20, 10))
    for i in range(plot_dim[0], plot_dim[1]):
        plt.subplot(plot_corr + i)
        sweep = sweep_data(folder, name_of_sweeps, oneD_names[i], 1)
        sweep.plottable_list(correct[i])
        
        #plt.title(titles[i], fontsize=24)
        if(i == 0 or i == 3):
            plt.ylabel('Likelihood', fontsize=16)
        plt.xlabel(titles[i], fontsize=16)
        plt.xlim(ranges[i][0], ranges[i][1])
        plt.ylim(l, 0)
        plt.plot(sweep.vals, sweep.liks, linestyle = '-', linewidth = 2, color ='b')
        plt.scatter(sweep.vals, sweep.liks, marker = 'o', s = 4, color ='r')
        plt.plot(sweep.corr, sweep.cor2, linestyle = '-', linewidth = 1, color ='k', alpha = 1)
    plt.savefig(folder + 'parameter_sweeps' + name_of_sweeps + '/multiplot.png', format = 'png')

# # # # # # # # # # # # # # # # # # # # # #
#    Two Dimensional Surface Sweep Func   #
# # # # # # # # # # # # # # # # # # # # # #
def twoD_plot():
    titles  = ['Backward Evolve Time (Gyr)',  'Baryon Scale Radius (kpc)', r'Scale Radius Ratio ($R_{B}/(R_{B}+R_{D})$)', 'Baryonic Mass (SMU)',  'Mass Ratio (Baryonic/Total)']
    plot_corr = 231
    l = -200
    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(111, projection='3d')
    for i in range(plot_dim[0], plot_dim[1]):
        for j in range(plot_dim2[0], plot_dim2[1]):
            print 'this ran'
            name = oneD_names[i] + '_' + oneD_names[j]
            print name
            sweep = sweep_data(folder, name_of_sweeps, name, 2)
            sweep.plottable_list(correct[i])
            
            #ax.title(titles[i], fontsize=24)
            ax.set_xlabel(titles[i], fontsize=16)
            ax.set_ylabel(titles[i + 1], fontsize=16)
            ax.set_zlabel('Likelihood', fontsize=16)
            ax.set_xlim(ranges[i][0], ranges[i][1])
            ax.set_ylim(ranges[i + 1][0], ranges[i + 1][1])
            ax.set_zlim(l, 0)
            ax.scatter(sweep.vals, sweep.liks, marker = 'o', s = 4, color ='r')
            plt.plot(sweep.corr, sweep.cor2, linestyle = '-', linewidth = 1, color ='k', alpha = 1)
            plt.savefig(folder + 'parameter_sweeps' + name_of_sweeps + '/multiplot.png', format = 'png')
    return 0

def main():
    if(plot_1D):
        oneD_plot()
    if(plot_2D):
        twoD_plot()
main()
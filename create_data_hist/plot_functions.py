#! /usr/bin/python
#/* Copyright (c) 2018 Siddhartha Shelton */
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Useful Plotting functions                                               #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import AutoMinorLocator





# # # # # # # # # # # # # # # # # # # 
# Serving create_data_hist          #
# # # # # # # # # # # # # # # # # # # 
def lamda_beta_plot(dat):
    plt.ylim(-5, 7)
    plt.xlabel(r'$\Lambda_{Orphan}$')
    plt.ylabel(r'$\beta_{Orphan,corr}$')
    plt.plot(dat.ON_star_N_lbda, dat.ON_star_N_beta,  '.', markersize = .4, color = 'b', alpha=1.0, marker = 'o',label = 'ON')
    plt.plot(dat.OFF_star_N_lbda, dat.OFF_star_N_beta, '.', markersize = .4, color = 'black', alpha=.75, marker = 'o', label = 'OFF')
    plt.savefig('plots/lmbda_beta.png', format='png', dpi=500)
    
    
def plot_binned_counts(dat):
    plt.xlim(50, -50)
    plt.ylim(0, 1500)
    plt.xlabel("$\Lambda_{Orphan}$")
    plt.ylabel("N")
    plt.xticks( [50, 40, 30, 20, 10, 0, -10, -20, -30, -40, -50])
    #plt.tick_params(which='minor', length=4, color='r')
    w = 2.6
    if(len(dat.bin_ON.counts) > 0):
        plt.bar(dat.bnd.bin_centers, dat.bin_ON.counts, width = w, color = "w", edgecolor = "k", alpha = 1)
    if(len(dat.bin_OFF.counts) > 0):
        plt.bar(dat.bnd.bin_centers, dat.bin_OFF.counts, width = w, color = "w", edgecolor = "r", alpha = 0.5)
    
    if(len(dat.bin_diff.counts) > 0):
        plt.bar(dat.bnd.bin_centers, dat.bin_diff.counts, width = w, color = "b", edgecolor = "b", alpha = 0.5)
        #plt.bar(dat.bnd.bin_centers, dat.bnd.bin_N, width = w, color = "k", edgecolor = "b", alpha = 0.5)
    plt.savefig('plots/figure5_recreation.png', format='png')
    plt.clf()
    #plt.show()

def plot_simN_normed(dat):
    plt.xlim(50, -50)
    #plt.ylim(0, 1500)
    plt.xlabel("$\Lambda_{Orphan}$")
    plt.ylabel("N")
    plt.xticks( [50, 40, 30, 20, 10, 0, -10, -20, -30, -40, -50])
    #plt.tick_params(which='minor', length=4, color='r')
    w = 2.6
    plt.bar(dat.bnd.bin_centers, dat.bin_normed.counts, width = w, color = "b", edgecolor = "b", alpha = 0.5)
    plt.savefig('plots/figure5_simunits_normed.png', format='png')
    plt.clf()
    #plt.show()   
    
    
    
# # # # # # # # # # # # # # # # # # # 
# Serving beta_bins                 #
# # # # # # # # # # # # # # # # # # # 
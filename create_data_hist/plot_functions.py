#! /usr/bin/python
#/* Copyright (c) 2018 Siddhartha Shelton */
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Useful Plotting functions                                               #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import AutoMinorLocator




def write_lambda_beta(On_field):
    f = open('lambda_betas_refa.dat', 'w')
    
    for i in range(len(On_field.star_lmda)):
        f.write("%0.15f\t%0.15f\n" % (On_field.star_lmda[i], On_field.star_beta[i]))
        
    f.close()
    


# # # # # # # # # # # # # # # # # # # 
# Serving create_data_hist          #
# # # # # # # # # # # # # # # # # # # 
def lamda_beta_plot(On_field, Off_field):
    plt.ylim(-5, 7)
    plt.xlabel(r'$\Lambda_{Orphan}$')
    plt.ylabel(r'$\beta_{Orphan,corr}$')
    plt.plot(On_field.star_lmda,  On_field.star_beta,  '.', markersize = .4, color = 'b', alpha=1.0, marker = 'o',label = 'ON')
    plt.plot(Off_field.star_lmda, Off_field.star_beta, '.', markersize = .4, color = 'black', alpha=.75, marker = 'o', label = 'OFF')
    plt.savefig('plots/lmbda_beta_refac.png', format='png', dpi=500)
    plt.clf()
    
def plot_binned_counts(On_bnd, Off_bnd, diff_bnd, bnd_paras):
    plt.figure(figsize=(15, 10))
    params = {'legend.fontsize': 28,
            'legend.handlelength': 1}
    plt.rcParams.update(params)
    plt.xlim(50, -50)
    plt.ylim(0, 1500)
    plt.tick_params(axis='y', which='major', labelsize=20)
    plt.tick_params(axis='x', which='major', labelsize=20)
    plt.xlabel("$\Lambda_{Orphan}$", fontsize=28)
    plt.ylabel("Star Count", fontsize=28)
    plt.xticks( [50, 40, 30, 20, 10, 0, -10, -20, -30, -40, -50])
    #plt.tick_params(which='minor', length=4, color='r')
    w = 2.6
    if(len(On_bnd.binned_data.counts) > 0):
        plt.bar(bnd_paras.bin_centers, On_bnd.binned_data.counts, width = w, color = "w", edgecolor = "k", alpha = 1, hatch='...', label = 'ON field')
    
    if(len(Off_bnd.binned_data.counts) > 0):
        plt.bar(bnd_paras.bin_centers, Off_bnd.binned_data.counts, width = w, color = "w", edgecolor = "r", alpha = 1, hatch='//', label = 'OFF field')
    
    if(len(diff_bnd.binned_data.counts) > 0):
        plt.bar(bnd_paras.bin_centers, diff_bnd.binned_data.counts, width = w, color = "cyan", edgecolor = "b", alpha = 1, hatch='xx', label = 'Difference')
        #plt.bar(dat.bnd.bin_centers, dat.bnd.bin_N, width = w, color = "k", edgecolor = "b", alpha = 0.5)
    plt.legend()
    plt.savefig('plots/figure5_recreation_refac.png', format='png', bbox_inches='tight')
    plt.savefig('plots/figure5_recreation_refac.pdf', format='pdf', bbox_inches='tight')
    plt.clf()
    #plt.show()

def plot_simN_normed(bnd_diff_normed, bin_paras):
    plt.xlim(50, -50)
    plt.ylim(0, 0.3)
    plt.xlabel("$\Lambda_{Orphan}$")
    plt.ylabel("N")
    plt.xticks( [50, 40, 30, 20, 10, 0, -10, -20, -30, -40, -50])
    #plt.tick_params(which='minor', length=4, color='r')
    w = 2.6
    plt.bar(bin_paras.bin_centers, bnd_diff_normed.binned_data.counts, width = w, color = "b", edgecolor = "b", alpha = 0.5)
    plt.savefig('plots/figure5_simunits_normed_refac.png', format='png')
    plt.clf()
    #plt.show()   
    
    
    
# # # # # # # # # # # # # # # # # # # 
# Serving beta_bins                 #
# # # # # # # # # # # # # # # # # # # 
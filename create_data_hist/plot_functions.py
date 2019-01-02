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
def plot_each_bin(i, hist_paras, beta_hist_init, ON_field_bins, OFF_field_bins, combined_field):
    w = 0.25
    #test_dat = test_data()
    plt.xlim(beta_hist_init.lower - 2, beta_hist_init.upper + 2)
    plt.ylim(0.0, 400)
    plt.ylabel("counts")
    plt.xlabel(r"$\beta_{Orphan}$")
    plt.figure(figsize=(20, 60))
    fig, axes = plt.subplots(ncols=2, sharex=True, sharey=True)
    fig.subplots_adjust(hspace=0, wspace=0)
    for i in range(0, hist_paras.Nbins):
        #plt.ylabel("counts")
        
        plt.subplot(3, 8, i + 1)
        plt.xlim(beta_hist_init.lower - 0.5 , beta_hist_init.upper + 0.5)
        plt.ylim(0.0, 200)
        plt.yticks([])
        if(i == 0 or i == 8 or i == 16): #or i == 16 or i == 20):
            plt.yticks([50,100, 150])
        if(i == 8):
            plt.ylabel("N")
        if(i >= 16):
            plt.xticks([-2, 0, 2])
        if(i == 19):
            plt.xlabel(r"$\beta_{Orphan}$")
        plt.bar(beta_hist_init.bin_centers, combined_field[i], width=w, color='k', alpha = 1., label = 'Combined')
        plt.bar(beta_hist_init.bin_centers, OFF_field_bins[i], width=w, color='r', alpha = 0.5, label = 'OFF Field')
        plt.bar(beta_hist_init.bin_centers, ON_field_bins[i],  width=w, color='b', alpha = 0.5, label = 'ON Field')
        #plt.legend()
        
    plt.savefig('stream_beta_plots/lambda_bin_combined.png', format = 'png', dpi=300)
    plt.close()
    
    
    
def plot_fit_dots(i, hist_paras, beta_hist_init, ON_field_bins, OFF_field_bins, combined_field, fit_parameters, fit, cost):
    plt.figure()
    plt.xlim(beta_hist_init.lower - 2, beta_hist_init.upper + 2)
    
    # this is sloppy. but whatevs
    fit_paras = list(fit_parameters)
    fit_xs, fit_fs = fit.cost.generate_plot_points(fit_paras)
    w = 0.25
    
    lb = 'paras: m=' + str(round(fit_paras[0], 2)) + ' b=' + str(round(fit_paras[1], 2)) + ' A=' + str(round(fit_paras[2], 2)) + r" $x_{0}$=" + str(round(fit_paras[3], 2)) + r' $\sigma$=' + str(round(fit_paras[4], 2)) + ' L=' + str(cost)
    
    fig, axes = plt.subplots(ncols=2, sharex=True, sharey=True)
    fig.subplots_adjust(hspace=0)
    ax1 = plt.subplot(211)
    plt.ylabel("Star Count", fontsize=16)
    plt.xlim(beta_hist_init.lower - 0.5 , beta_hist_init.upper + 0.5)
    plt.ylim(0.0, 400)
    plt.plot(fit_xs,  fit_fs, color='k',linewidth = 2, alpha = 1., label = '' )
    plt.plot(beta_hist_init.bin_centers, combined_field[i], '.', markersize=4.5, markerfacecolor='white', markeredgecolor='k', alpha = 0.9, marker = 'o', markeredgewidth=1,label = 'C')
    #plt.plot(bin_centers, binned_beta_OFF[i]     , 'o', markersize=2.5, color='r', alpha = 0.8, marker = 'o', label = 'OFF')
    #plt.plot(bin_centers, binned_beta_ON[i]      , 'o', markersize=2.5,  color='b', alpha = 0.8, marker = 'o', label = 'ON')
    plt.xticks([])
    plt.yticks([50, 100, 150, 200, 250, 300, 350, 400])
    
    ax2 = plt.subplot(212)
    plt.ylabel("Star Count", fontsize=16)
    plt.xlabel(r"$\beta_{Orphan}$", fontsize=16)
    plt.xlim(beta_hist_init.lower - 0.5 , beta_hist_init.upper + 0.5)
    plt.ylim(0.0, 400)
    #plt.bar(bin_centers, binned_beta_combined[i], width=w, color='w', edgecolor = "k", hatch='xxxxx', alpha = 1., label = 'Combined')
    plt.bar(beta_hist_init.bin_centers, OFF_field_bins[i],      width=w, color='w', edgecolor = "firebrick", hatch='\\\\\\\\', alpha = 1., label = 'OFF')
    plt.bar(beta_hist_init.bin_centers, ON_field_bins[i],       width=w, color='w', edgecolor = "b", hatch='////', alpha = 1., label = 'ON')
    plt.yticks([50, 100, 150,  200, 250, 300, 350])
    #plt.legend()
    
    if(i == 0 ):
        plt.legend(bbox_to_anchor=(0.65,0.7), loc='lower left', borderaxespad=0.,  prop={'size': 14}, framealpha=1)
    elif(i == 1 ):
        plt.legend(bbox_to_anchor=(0.65,0.87), loc='lower left', borderaxespad=0.,  prop={'size': 14}, framealpha=1)
    elif(i == 2 ):
        plt.legend(bbox_to_anchor=(0.65,0.87), loc='lower left', borderaxespad=0.,  prop={'size': 14}, framealpha=1)
    elif(i == 3 ):
        plt.legend(bbox_to_anchor=(0.65,0.4), loc='lower left', borderaxespad=0.,  prop={'size': 14}, framealpha=1)
        
    plt.title(str(hist_paras.bin_lowers[i]) + r'$^o$<$\Lambda$<'+ str(hist_paras.bin_uppers[i]) + r'$^o$',  y=1, x=.2, fontsize=16)
    if(i == 3):
        plt.title(str(hist_paras.bin_lowers[i]) + r'$^o$<$\Lambda$<'+ str(hist_paras.bin_uppers[i]) + r'$^o$',  y=1.5, x=.2, fontsize=16)
    plt.savefig('stream_beta_plots/lambda_dots_' + str(i) + '_(' + str(hist_paras.bin_lowers[i]) + ',' + str(hist_paras.bin_centers[i]) + ',' +  str(hist_paras.bin_uppers[i]) + ').png', format = 'png')
    plt.savefig('stream_beta_plots/dots/lambda_dots_' + str(i) + '.pdf', format = 'pdf', bbox_inches='tight')
    plt.savefig('stream_beta_plots/dots/lambda_dots_' + str(i) + '.png', format = 'png', bbox_inches='tight')
    plt.close()
    
    
    
def plot_sigma(sigmas, hist_paras):
    plt.title(r'$\sigma$ vs $\Lambda_{Orphan}$')
    plt.xlabel(r'$\Lambda_{Orphan}$')
    plt.ylabel(r'$\sigma$')
    plt.ylim(0, 1.5)
    plt.scatter(hist_paras.bin_centers, sigmas, marker='o')
    plt.savefig('plots/sigma_v_lambda.png', format='png')

#! /usr/bin/python
#/* Copyright (c) 2016 Siddhartha Shelton */

import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from nbody_functional import *


# # # # # # # # # # # # # # # # # # # # # #
#        histogram plot                   #
# # # # # # # # # # # # # # # # # # # # # #
# # 
#fit_folder = 'diff_seeds/'
#labels = ['data', 'fit1', 'fit2', 'fit3']
#labels = ['Seed 1','Seed 2','Seed 3','Seed 4','Seed 5','Seed 6','Seed 7','Seed 8','Seed 9','Seed 10']
#plot_name = '20k_diff_seed_ericseeds'

#fit_folder = 'fitted_sim_results_12_6_runs/'
#labels = ['MilkyWay@home', 'fit1', 'fit2', 'fit3']
#plot_name = 'fitted_sim_1_15_2018'

fit_folder = 'fitted_sim_results_12_6_runs/'
labels = ['data', 'fit1', 'fit2', 'fit3']
plot_name = 'fitted_data_1_21_2018'

#fit_folder = '/home/sidd/Desktop/research/quick_plots/hists_outs/willet_paras/'
#labels = ['data', 'half_in_baryons, L = -9531', 'data hist mass as baryon mass, rest as DM, L =-2707.77', '1.5 data hist mass as barons, rest DM, L=-61.85', '1.4 data mass as barons, rest DM, .2 Baryon scale, .8 rad ratio, -77.155']
#plot_name = 'willet_parameters'


def plot_hists(hists, ftype):
    hs = []
    for i in range(len(hists)):
        hs.append(nbody_histograms(hists[i] + '.hist'))

    labsiz = 20
    fntsiz = 26
    if(ftype == 'sim'):
        xlower = -180.0
        xupper = 180.0
    else:
        xlower = -40.0
        xupper = 40.0
    
    ylower = 0
    yupper = .4
    wid = 2
    #coor  = (len(hs) * 100)  + 10
    #coor  = 410
    coori = 1
    
    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row', figsize=(10, 10))
    #f.text(0.04, 0.5, r'$\beta$' , va='center', fontsize = fntsiz)
    f.subplots_adjust(hspace=0)
    f.subplots_adjust(wspace=0)
    params = {'legend.fontsize': 14,
            'legend.handlelength': 1}
    plt.rcParams.update(params)
    
    for coori in range(len(hs)):
        #plt.subplot(coor + coori + 1)
        plt.subplot(len(hs), 1 , coori + 1)
        plt.xlim((xlower, xupper))
        plt.ylim((ylower, yupper))
        plt.ylabel('N', fontsize = fntsiz)
        plt.tick_params(axis='y', which='major', labelsize=labsiz)
        plt.tick_params(axis='x', which='major', labelsize=labsiz)
        #plt.yticks([0.0, 0.1, 0.2, 0.3, 0.4])
        plt.yticks([0.0, 0.2])
        
        if(coori < len(hs) - 1):#get the tics on the last panel of plot
            plt.xticks([])
        
        if(coori == len(hs) - 1):
            plt.xlabel(r'$\Lambda_{Orphan}$', fontsize = fntsiz)
            
        c = 'r' if coori == 0 else 'k'
        
        plt.bar(hs[coori].lbins, hs[coori].counts, width = wid, color=c, alpha=1, label = labels[coori])
        plt.legend()
        #plt.legend(bbox_to_anchor=(0.5,0.1), loc='center', borderaxespad=0.,  prop={'size': 20}, framealpha=1)

    if(ftype == 'sim'):
        plt.savefig('plots/' + fit_folder + 'lmbdahist_sim_' + plot_name + '.png', format='png', dpi = 300, bbox_inches='tight')
        plt.savefig('plots/' + fit_folder + 'lmbdahist_sim_' + plot_name + '.pdf', format='pdf', dpi = 300, bbox_inches='tight')
        
    else:
        plt.savefig('plots/' + fit_folder + 'lmbdahist_data_' + plot_name + '.png', format='png', dpi = 300, bbox_inches='tight')
        plt.savefig('plots/' + fit_folder + 'lmbdahist_data_' + plot_name + '.pdf', format='pdf', dpi = 300, bbox_inches='tight')
        #plt.savefig(fit_folder + 'lmbdahist_data_' + plot_name + '.png', format='png', dpi = 300, bbox_inches='tight')
 
 

def plot_unnormalized_hists(hists, data, ftype):
    hs = []
    angle_cuttoffs = [-36.0, 36.0, 24, -15.0, 15.0, 1]
    dh = nbody_histograms(data + '.hist')
    hs.append(dh)
    for i in range(1, len(hists) + 1):
        hs.append(nbody_outputs(hists[i - 1] + '.out'))
        hs[i].binner(angle_cuttoffs)
    labsiz = 20
    fntsiz = 26
    if(ftype == 'sim'):
        xlower = -180.0
        xupper = 180.0
    else:
        xlower = -40.0
        xupper = 40.0
    
    ylower = 0
    yupper = 250
    wid = 2
    #coor  = (len(hs) * 100)  + 10
    #coor  = 410
    coori = 1
    
    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row', figsize=(10, 10))
    #f.text(0.04, 0.5, r'$\beta$' , va='center', fontsize = fntsiz)
    f.subplots_adjust(hspace=0)
    f.subplots_adjust(wspace=0)
    params = {'legend.fontsize': 14,
            'legend.handlelength': 1}
    plt.rcParams.update(params)
    
    for coori in range(len(hs)):
        #plt.subplot(coor + coori + 1)
        plt.subplot(len(hs), 1 , coori + 1)
        plt.xlim((xlower, xupper))
        plt.ylim((ylower, yupper))
        plt.ylabel('N', fontsize = fntsiz)
        plt.tick_params(axis='y', which='major', labelsize=labsiz)
        plt.tick_params(axis='x', which='major', labelsize=labsiz)
        #plt.yticks([0.0, 0.1, 0.2, 0.3, 0.4])
        #plt.yticks([0.0, 500, 1000, 1500])
        plt.yticks([0.0, 250])
        
        if(coori < len(hs) - 1):#get the tics on the last panel of plot
            plt.xticks([])
        
        if(coori == len(hs) - 1):
            plt.xlabel(r'$\Lambda_{Orphan}$', fontsize = fntsiz)
            
        c = 'r' if coori == 0 else 'k'
        if(coori == 0):
            plt.bar(hs[coori].lbins, hs[coori].counts, width = wid, color=c, alpha=1, label = labels[coori])
            continue
        
        plt.bar(hs[coori].mid_bins, hs[coori].binned_bm, width = wid, color=c, alpha=1, label = labels[coori])
        plt.legend()
        #plt.legend(bbox_to_anchor=(0.5,0.1), loc='center', borderaxespad=0.,  prop={'size': 20}, framealpha=1)

    if(ftype == 'sim'):
        plt.savefig('plots/' + fit_folder + 'lmbdahist_sim_' + plot_name + '.png', format='png', dpi = 300, bbox_inches='tight')
        plt.savefig('plots/' + fit_folder + 'lmbdahist_sim_' + plot_name + '.pdf', format='pdf', dpi = 300, bbox_inches='tight')
        
    else:
        plt.savefig('plots/' + fit_folder + 'unnormalized_lmbdahist_data_' + plot_name + '.png', format='png', dpi = 300, bbox_inches='tight')
        plt.savefig('plots/' + fit_folder + 'unnormalized_lmbdahist_data_' + plot_name + '.pdf', format='pdf', dpi = 300, bbox_inches='tight')
        #plt.savefig(fit_folder + 'unnormalized_lmbdahist_data_' + plot_name + '.png', format='png', dpi = 300, bbox_inches='tight')
 
def plot_lhists(hists, ftype):#for plotting the data and the fitted values
    hs = []
    outs_l = []
    outs_d = []
    binN = 100
    if(ftype =='dat'):
        outs_l.append('')
        outs_d.append('')
        
    for i in range(len(hists) ):
        hs.append(nbody_outputs(hists[i] + '.out'))
        hs[i].dark_light_split()
        outs_l.append(binner([0., 360.], binN, hs[i].light_l))
        outs_d.append(binner([0., 360.], binN, hs[i].dark_l))
        
    baryon_color = 'r'
    dm_color = 'k'
    labsiz = 20
    fntsiz = 26
    if(ftype == 'sim'):
        xlower = 360.0
        xupper = 120.0
        yupper = 2000
    else:
        xlower = 360.0
        xupper = 120.0
        yupper = 2000
    
    
    ylower = 0
    wid = 2
    #coor  = len(hs) * 100 + 10
    #coor  = 210
    coori = 1
    
    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row', figsize=(10, 10))
    #f.text(0.04, 0.5, r'$\beta$' , va='center', fontsize = fntsiz)
    f.subplots_adjust(hspace=0)
    f.subplots_adjust(wspace=0)
    params = {'legend.fontsize': 14,
            'legend.handlelength': 1}
    plt.rcParams.update(params)
    
    for coori in range(len(outs_l)):
        #plt.subplot(coor + coori + 1)
        #print coor + coori + 1
        #print len(outs_l)
        plt.subplot(len(outs_l), 1 , coori + 1)
        plt.xlim((xlower, xupper))
        plt.ylim((ylower, yupper))
        plt.ylabel('N', fontsize = fntsiz)
        plt.tick_params(axis='y', which='major', labelsize=labsiz)
        plt.tick_params(axis='x', which='major', labelsize=labsiz)
        plt.yticks([0.0, 1000])
        
        if(coori < len(outs_l) - 1):#get the tics on the last panel of plot
            plt.xticks([])
        
        if(coori == len(outs_l) - 1):
            plt.xlabel('l (deg)', fontsize = fntsiz)
            
        c = 'r' if coori == 0 else 'k'
    
        if(ftype == 'sim' or (ftype == 'dat' and coori > 0)):
            plt.bar(outs_l[coori].bin_centers, outs_l[coori].counts, width = wid, color=c, alpha=1, label = labels[coori])
            #plt.bar(outs_d[coori].bin_centers, outs_d[coori].counts, width = wid, color='b', alpha=.5, label = 'DM')
        plt.legend()
        #plt.legend(bbox_to_anchor=(0.5,0.1), loc='center', borderaxespad=0.,  prop={'size': 20}, framealpha=1)
        coori += 1

    if(ftype == 'sim'):
        plt.savefig('plots/' + fit_folder + 'lhists_sim_' + plot_name + '.png', format='png', dpi = 300, bbox_inches='tight')
        plt.savefig('plots/' + fit_folder + 'lhists_sim_' + plot_name + '.pdf', format='pdf', dpi = 300, bbox_inches='tight')
    else:
        plt.savefig('plots/' + fit_folder + 'lhists_data_' + plot_name + '.png', format='png', dpi = 300, bbox_inches='tight')
        #plt.savefig('plots/' + fit_folder + 'fitted_lhists_sim.pdf', format='pdf', dpi = 300, bbox_inches='tight')


def lambda_beta_outputs_plot(hists, ftype):#for plotting the data and the fitted values
    outs = []
    hs = []

    if(ftype == 'dat'):
        dat_lambdas = []
        dat_betas = []
        f = open('./create_data_hist/lambda_betas.dat', 'r')
        for line in f:
            ss = line.split('\t')
            dat_lambdas.append(float(ss[0]))
            dat_betas.append(float(ss[1]))
        f.close()
        outs.append('')
    
    for i in range(len(hists)):
        hs.append(nbody_outputs(hists[i] + '.out'))
        hs[i].dark_light_split()
        hs[i].convert_lambda_beta(True)
        outs.append(hs[i])
        
      
    angle_cuttoffs = [-150.0, 150.0, 50, -15.0, 15.0, 1]
    baryon_color = 'r'
    dm_color = 'k'
    labsiz = 20
    fntsiz = 26
    
    if(ftype == 'sim'):
        xlower = -180.0
        xupper = 180.0
    else:
        xlower = -180.0
        xupper = 180.0
    
    ylower = -15
    yupper = 15
    
    coor  = 410
    coori = 1
    
    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row', figsize=(20, 10))
    #f.text(0.04, 0.5, r'$\beta$' , va='center', fontsize = fntsiz)
    f.subplots_adjust(hspace=0)
    f.subplots_adjust(wspace=0)
    params = {'legend.fontsize': 20,
            'legend.handlelength': 1}
    plt.rcParams.update(params)
    
    for coori in range(len(outs)):
        #plt.subplot(coor + coori + 1)
        plt.subplot(len(hs) + 1, 1 , coori + 1)
        plt.xlim((xlower, xupper))
        plt.ylim((ylower, yupper))
        plt.ylabel(r'$\beta$', fontsize = fntsiz)
        plt.tick_params(axis='y', which='major', labelsize=labsiz)
        plt.tick_params(axis='x', which='major', labelsize=labsiz)
        
        if(coori < len(outs) - 1):#get the tics on the last panel of plot
            plt.xticks([])
            
        if(coori == len(outs) - 1):
            plt.xlabel(r'$\Lambda$', fontsize = fntsiz)
            
            
        if(ftype == 'sim' or (ftype == 'dat' and coori > 0)):
            plt.plot(outs[coori].light_lambdas, outs[coori].light_betas, '.', markersize = .5, color = baryon_color, alpha=1, marker = '.', label = labels[coori])
            #plt.plot(outs[coori].dark_lambdas,  outs[coori].dark_betas, '.', markersize = .5, color = dm_color, alpha=1, marker = '.', label = labels[coori])

        elif(ftype == 'dat' and coori == 0):
            plt.plot(dat_lambdas, dat_betas, '.', markersize = .75, color = baryon_color, alpha=1, marker = '.', label = labels[coori])

        plt.legend(bbox_to_anchor=(0.01,0.03), loc='lower left', borderaxespad=0.,  prop={'size': 20}, framealpha=1)

        
    if(ftype == 'sim'):
        plt.savefig('plots/' + fit_folder + 'lambda_beta_sim_' + plot_name + '.png', format='png', dpi = 300, bbox_inches='tight')
        #plt.savefig('plots/' + fit_folder + 'fitted_lambda_beta_sim.pdf', format='pdf', dpi = 300, bbox_inches='tight')
    else:
        plt.savefig('plots/' + fit_folder + 'lambda_beta_data_' + plot_name + '.png', format='png', dpi = 300, bbox_inches='tight')
        #plt.savefig('plots/' + fit_folder + 'fitted_lambda_beta_data.pdf', format='pdf', dpi = 300, bbox_inches='tight')


def plot_betadisps_hists(hists, ftype):#plots the dispersions from the histograms with lambda beta on top. for 2 hists
    hs = []
    for i in range(len(hists)):
        hs.append(nbody_histograms(hists[i] + '.hist'))

    labsiz = 20
    fntsiz = 26
    if(ftype == 'sim'):
        xlower = -180.0
        xupper = 180.0
    else:
        xlower = -40.0
        xupper = 40.0
    
    ylower = 0
    yupper = 2
    wid = 2
    coor  = 410
    coori = 1
    
    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row', figsize=(10, 10))
    #f.text(0.04, 0.5, r'$\beta$' , va='center', fontsize = fntsiz)
    f.subplots_adjust(hspace=0)
    f.subplots_adjust(wspace=0)
    params = {'legend.fontsize': 20,
            'legend.handlelength': 1}
    plt.rcParams.update(params)
    
    for coori in range(len(hs)):
        #plt.subplot(coor + coori + 1)
        plt.subplot(len(hs), 1 , coori + 1)
        plt.xlim((xlower, xupper))
        plt.ylim((ylower, yupper))
        plt.ylabel(r'$\sigma_{\beta}$', fontsize = fntsiz)
        plt.tick_params(axis='y', which='major', labelsize=labsiz)
        plt.tick_params(axis='x', which='major', labelsize=labsiz)
        plt.yticks([0.0, 0.5, 1, 1.5])
        
        if(coori < len(hs) - 1):#get the tics on the last panel of plot
            plt.xticks([])
        
        if(coori == len(hs) - 1):
            plt.xlabel(r'$\Lambda$', fontsize = fntsiz)
            
        c = 'r' if coori == 0 else 'k'
        
        plt.bar(hs[coori].lbins, hs[coori].bd, width = wid, color=c, alpha=1, label = labels[coori])
        plt.legend()
        #plt.legend(bbox_to_anchor=(0.5,0.1), loc='center', borderaxespad=0.,  prop={'size': 20}, framealpha=1)

    if(ftype == 'sim'):
        plt.savefig('plots/' + fit_folder + 'betadisp_hists_sim_' + plot_name + '.png', format='png', dpi = 300, bbox_inches='tight')
        #plt.savefig('plots/' + fit_folder + 'fitted_hists_sim.pdf', format='pdf', dpi = 300, bbox_inches='tight')
    else:
        #plt.savefig('plots/' + fit_folder + 'betadisp_hists_data_' + plot_name + '.png', format='png', dpi = 300, bbox_inches='tight')
        #plt.savefig('plots/' + fit_folder + 'fitted_hists_data.pdf', format='pdf', dpi = 300, bbox_inches='tight')
        plt.savefig(fit_folder + 'betadisp_hists_data_' + plot_name + '.png', format='png', dpi = 300, bbox_inches='tight')

    #plt.show()
    return 1

def main():
    path = '/home/sidd/Desktop/research/'

    #folder = path + 'quick_plots/hists_outs/willet_paras/'
    folder = path + 'quick_plots/hists_outs/'
     
    if(False):
        f1 = folder + 'hist_v172_4bt_3p95ft_0p2_0p2_12_0p2__11_29_18_seed1'
        f2 = folder + 'hist_v172_4bt_3p95ft_0p2_0p2_12_0p2__11_29_18_seed2'
        f3 = folder + 'hist_v172_4bt_3p95ft_0p2_0p2_12_0p2__11_29_18_seed3'
        f4 = folder + 'hist_v172_4bt_3p95ft_0p2_0p2_12_0p2__11_29_18_seed4'
        f5 = folder + 'hist_v172_4bt_3p95ft_0p2_0p2_12_0p2__11_29_18_seed5'
        f6 = folder + 'hist_v172_4bt_3p95ft_0p2_0p2_12_0p2__11_29_18_seed6'
        f7 = folder + 'hist_v172_4bt_3p95ft_0p2_0p2_12_0p2__11_29_18_seed7'
        f8 = folder + 'hist_v172_4bt_3p95ft_0p2_0p2_12_0p2__11_29_18_seed8'
        f9 = folder + 'hist_v172_4bt_3p95ft_0p2_0p2_12_0p2__11_29_18_seed9'
        f10 = folder + 'hist_v172_4bt_3p95ft_0p2_0p2_12_0p2__11_29_18_seed10'
        fs = [cor, f2, f3, f4, f5, f6, f7, f8, f9, f10]
        
        f1 = folder + 'hist_v172_3p95bt_3p95ft_0p2_0p2_12_0p2__12_5_18_seed1'
        f2 = folder + 'hist_v172_3p95bt_3p95ft_0p2_0p2_12_0p2__12_5_18_seed2'
        f3 = folder + 'hist_v172_3p95bt_3p95ft_0p2_0p2_12_0p2__12_5_18_seed3'
        f4 = folder + 'hist_v172_3p95bt_3p95ft_0p2_0p2_12_0p2__12_5_18_seed4'
        f5 = folder + 'hist_v172_3p95bt_3p95ft_0p2_0p2_12_0p2__12_5_18_seed5'
        f6 = folder + 'hist_v172_3p95bt_3p95ft_0p2_0p2_12_0p2__12_5_18_seed6'
        f7 = folder + 'hist_v172_3p95bt_3p95ft_0p2_0p2_12_0p2__12_5_18_seed7'
        f8 = folder + 'hist_v172_3p95bt_3p95ft_0p2_0p2_12_0p2__12_5_18_seed8'
        f9 = folder + 'hist_v172_3p95bt_3p95ft_0p2_0p2_12_0p2__12_5_18_seed9'
        f10 = folder + 'hist_v172_3p95bt_3p95ft_0p2_0p2_12_0p2__12_5_18_seed10'
        fs = [cor, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10]
        
        
    
    f1 = folder + 'hist_v172_4bt_3p95ft_0p2_0p2_12_0p2__11_29_18_seed5'
    f2 = folder + '4bt_3.95ft_test'
    f3 = folder + '4bt_3.95ft_withbestlikerange_test'
    f4 = folder + '4gy_test'
    f5 = folder + '3.94gy_test'
    fs = [f1, f2, f3, f4, f5]
    
    if(False):
        f1 = folder + 'hist_v172_4bt_3p95ft_0p2_0p2_12_0p2__11_29_18_oldorb_seed1'
        f2 = folder + 'hist_v172_4bt_3p95ft_0p2_0p2_12_0p2__11_29_18_oldorb_seed2'
        f3 = folder + 'hist_v172_4bt_3p95ft_0p2_0p2_12_0p2__11_29_18_oldorb_seed3'
        f4 = folder + 'hist_v172_4bt_3p95ft_0p2_0p2_12_0p2__11_29_18_oldorb_seed4'
        f5 = folder + 'hist_v172_4bt_3p95ft_0p2_0p2_12_0p2__11_29_18_oldorb_seed5'
        f6 = folder + 'hist_v172_4bt_3p95ft_0p2_0p2_12_0p2__11_29_18_oldorb_seed6'
        f7 = folder + 'hist_v172_4bt_3p95ft_0p2_0p2_12_0p2__11_29_18_oldorb_seed7'
        f8 = folder + 'hist_v172_4bt_3p95ft_0p2_0p2_12_0p2__11_29_18_oldorb_seed8'
        f9 = folder + 'hist_v172_4bt_3p95ft_0p2_0p2_12_0p2__11_29_18_oldorb_seed9'
        f10 = folder + 'hist_v172_4bt_3p95ft_0p2_0p2_12_0p2__11_29_18_oldorb_seed10'
        
        
        f1 = folder + 'hist_v174_100k_4bt_3p95ft_0p2_0p2_12_0p2__1_2_19_seed1'
        f2 = folder + 'hist_v174_100k_4bt_3p95ft_0p2_0p2_12_0p2__1_2_19_seed2'
        f3 = folder + 'hist_v174_100k_4bt_3p95ft_0p2_0p2_12_0p2__1_2_19_seed3'
        f4 = folder + 'hist_v174_100k_4bt_3p95ft_0p2_0p2_12_0p2__1_2_19_seed4'
        f5 = folder + 'hist_v174_100k_4bt_3p95ft_0p2_0p2_12_0p2__1_2_19_seed5'
        f6 = folder + 'hist_v174_100k_4bt_3p95ft_0p2_0p2_12_0p2__1_2_19_seed6'
        f7 = folder + 'hist_v174_100k_4bt_3p95ft_0p2_0p2_12_0p2__1_2_19_seed7'
        f8 = folder + 'hist_v174_100k_4bt_3p95ft_0p2_0p2_12_0p2__1_2_19_seed8'
        f9 = folder + 'hist_v174_100k_4bt_3p95ft_0p2_0p2_12_0p2__1_2_19_seed9'
        f10 = folder + 'hist_v174_100k_4bt_3p95ft_0p2_0p2_12_0p2__1_2_19_seed10'
        
    
    
        fs = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10]
        #plot_hists(fs, 'sim')
        #plot_lhists(fs, 'sim')
        #lambda_beta_outputs_plot(fs, 'sim')
    
    cor = folder + 'hist_v172_3p95bt_3p95ft_0p2_0p2_12_0p2__12_5_18_seed5'
    f1 = folder + 'fit_sim2_1'
    f2 = folder + 'fit_sim2_2'
    f3 = folder + 'fit_sim2_3'
    fs = [cor, f1, f2, f3]
    #plot_hists(fs, 'sim')
    #plot_betadisps_hists(fs, 'sim')
    
    
    d1 = folder + 'data_hist_fall_2018'
    f1 = folder + 'fit_data_1'
    f2 = folder + 'fit_data_2'
    f3 = folder + 'fit_data_3'
    
    fs = [d1, f1, f2, f3]
    
    plot_hists(fs, 'dat')
    d1 = folder + 'data_hist_fall_2018_unnormalized'

    fs = [f1, f2, f3]
    lambda_beta_outputs_plot(fs, 'dat')
    plot_unnormalized_hists(fs, d1, 'dat')
    
    
    #d1 = folder + 'data_hist_fall_2018'
    #f1 = folder + 'willet_parameters_total_mass_halfb_halfd_3.945'
    #f2 = folder + 'willet_parameters_DataHistMassAsBaryonMass_RestAsDM_3.945'
    #f3 = folder + 'willet_parameters_1.5DataHistMassAsBaryonMass_RestAsDM'
    #f4 = folder + 'willet_parameters_1.4DataHistMassAsBaryonMass_RestAsDM_.2r_.8rr'
    
    
    #fs = [d1, f1, f2, f3, f4]
    
    #plot_hists(fs, 'dat')
    #plot_betadisps_hists(fs, 'dat')
    #plot_lhists(fs, 'dat')
    
    return 0 
main()




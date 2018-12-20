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
#fit_folder = 'test_fits/data_best_like_range_bensparameters/bensparas_as_total/'
#fit_folder = '11.14_data_runs_converged_fits/'
#fit_folder = 'test_fits/test_fits_for_release/'
fit_folder = 'test_fits/diff_seeds_bteqft/'
fit_folder = 'test_fits/diff_seed2/'

#fit_folder = 'test_fits/ben_parameters_baryonmasssameasdata_12_7_2018/'
#labels = ['mw@home', 'same diff seed', 'same- diff seed - with best likelihood', '4gyr', '3.94 gyr']
#labels = ['data', 'fit1', 'fit2', 'fit3']
#fit_folder = '11.27.fits/'
#labels = ['data', 'lower best like range', 'middle range', 'upper range']
#labels = ['data', '.98', '.99']
labels = ['MilkyWay@home', 'Seed 1','Seed 2','Seed 3','Seed 4','Seed 5','Seed 6','Seed 7','Seed 8','Seed 9','Seed 10']
#labels = ['Eric branch- eric lua','master-branch-sidd lua-same seed- same parameters','^ more bodies, 3.95 ft','7','8','9','10']
#plot_name = 'fitparameter1_99per_window'
#plot_name = 'benparas_astotal_compared_massfollowslight_reducedbaryoncscale10_98window'
#plot_name = 'fit_data_converged_11_14_2018'
#plot_name = 'test_fits_for_release'
#plot_name = 'eric_orphan_test'
#plot_name = 'ben_parameters_baryonmasssameasdata_12_7_2018_compared'
plot_name = 'different_seeds'


def plot4hists(hists, ftype):
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
        #plt.savefig('plots/' + fit_folder + 'fitted_hists_data.pdf', format='pdf', dpi = 300, bbox_inches='tight')
    
def plot4_lhists(hists, ftype):#for plotting the data and the fitted values
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


def lambda_beta_4outputs_plot(hists, ftype):#for plotting the data and the fitted values
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
        plt.subplot(len(hs), 1 , coori + 1)
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
            plt.plot(outs[coori].dark_lambdas,  outs[coori].dark_betas, '.', markersize = .5, color = dm_color, alpha=1, marker = '.', label = labels[coori])

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
        plt.savefig('plots/' + fit_folder + 'betadisp_hists_data_' + plot_name + '.png', format='png', dpi = 300, bbox_inches='tight')
        #plt.savefig('plots/' + fit_folder + 'fitted_hists_data.pdf', format='pdf', dpi = 300, bbox_inches='tight')

    #plt.show()
    return 1

def main():
    path = '/home/sidd/Desktop/research/'

    folder = path + 'quick_plots/hists_outs/'
    
    cor = folder + 'hist_v172_3p95_0p2_0p2_12_0p2__11_7_18'
    f1 = folder + 'fit_sim2_1'
    f2 = folder + 'fit_sim2_2'
    f3 = folder + 'fit_sim2_3'
    
    f1 = folder + 'willet_values'
    f1 = folder + 'mw_hist_values_kpcgy_orbit_3.95'
    
    #f1 = folder + 'mw_hist_values_kms_orbit_3.95_seed3'#same as used to create it
    f1 = folder + 'hist_v172_3p95_0p2_0p2_12_0p2__9_24_18'
    #f2 = folder + 'mw_hist_values_kms_orbit_3.95_mwathomeseed_compared' # milkyway@home seed but comparing it with correct hist L=-44.174160067193867 
    #f3 = folder + 'mw_hist_values_kms_orbit_3.95_mwathomeseed_compared_4gy' # milkyway@home seed but comparing it with correct hist L =-43.284475063290735
    
    #f2 = folder + 'mw_hist_values_kms_orbit_mwathomeseed_3.51gy'
    f2 = folder + 'mw_hist_values_kms_orbit_mwathomeseed_4gy'
    f3 = folder + 'mw_hist_values_kms_orbit_mwathomeseed_3.8gy'
    
    #f2 = folder + 'mw_hist_values_kms_orbit_3.95_seed2'
    #f3 = folder + 'mw_hist_values_kms_orbit_3.95_mwathomeseed'#same as mw@home fits
    #f3 = folder + 'mw_hist_values_kms_orbit_3.95_seed3'#used to make the current mw@h hist
     
    #f1 = folder + 'hist_v172_4bt_3p95ft_0p2_0p2_12_0p2__11_29_18_seed1'
    #f2 = folder + 'hist_v172_4bt_3p95ft_0p2_0p2_12_0p2__11_29_18_seed2'
    #f3 = folder + 'hist_v172_4bt_3p95ft_0p2_0p2_12_0p2__11_29_18_seed3'
    #f4 = folder + 'hist_v172_4bt_3p95ft_0p2_0p2_12_0p2__11_29_18_seed4'
    #f5 = folder + 'hist_v172_4bt_3p95ft_0p2_0p2_12_0p2__11_29_18_seed5'
    #f6 = folder + 'hist_v172_4bt_3p95ft_0p2_0p2_12_0p2__11_29_18_seed6'
    #f7 = folder + 'hist_v172_4bt_3p95ft_0p2_0p2_12_0p2__11_29_18_seed7'
    #f8 = folder + 'hist_v172_4bt_3p95ft_0p2_0p2_12_0p2__11_29_18_seed8'
    #f9 = folder + 'hist_v172_4bt_3p95ft_0p2_0p2_12_0p2__11_29_18_seed9'
    #f10 = folder + 'hist_v172_4bt_3p95ft_0p2_0p2_12_0p2__11_29_18_seed10'
    #fs = [cor, f2, f3, f4, f5, f6, f7, f8, f9, f10]
    
    #f1 = folder + 'hist_v172_3p95bt_3p95ft_0p2_0p2_12_0p2__12_5_18_seed1'
    #f2 = folder + 'hist_v172_3p95bt_3p95ft_0p2_0p2_12_0p2__12_5_18_seed2'
    #f3 = folder + 'hist_v172_3p95bt_3p95ft_0p2_0p2_12_0p2__12_5_18_seed3'
    #f4 = folder + 'hist_v172_3p95bt_3p95ft_0p2_0p2_12_0p2__12_5_18_seed4'
    #f5 = folder + 'hist_v172_3p95bt_3p95ft_0p2_0p2_12_0p2__12_5_18_seed5'
    #f6 = folder + 'hist_v172_3p95bt_3p95ft_0p2_0p2_12_0p2__12_5_18_seed6'
    #f7 = folder + 'hist_v172_3p95bt_3p95ft_0p2_0p2_12_0p2__12_5_18_seed7'
    #f8 = folder + 'hist_v172_3p95bt_3p95ft_0p2_0p2_12_0p2__12_5_18_seed8'
    #f9 = folder + 'hist_v172_3p95bt_3p95ft_0p2_0p2_12_0p2__12_5_18_seed9'
    #f10 = folder + 'hist_v172_3p95bt_3p95ft_0p2_0p2_12_0p2__12_5_18_seed10'
    #fs = [cor, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10]
    
    
    
    #f1 = folder + 'hist_v172_4bt_3p95ft_0p2_0p2_12_0p2__11_29_18_seed5'
    #f2 = folder + '4bt_3.95ft_test'
    #f3 = folder + '4bt_3.95ft_withbestlikerange_test'
    #f4 = folder + '4gy_test'
    #f5 = folder + '3.94gy_test'
    #fs = [f1, f2, f3, f4, f5]
    
    #fs = [folder + 'eric_orphan_test', folder + 'eric_orphan_test6', folder + 'eric_orphan_test_20k', folder + 'eric_orphan_test_20k_old_orbital', folder + 'eric_orphan_test_20k_old_orbital2']
    
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
    fs = [cor, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10]
    plot4_lhists(fs, 'sim')
    plot4hists(fs, 'sim')
    #plot_betadisps_hists(fs, 'sim')
    #lambda_beta_4outputs_plot(fs, 'sim')
    
    d1 = folder + 'data_hist_fall_2018'
    f1 = folder + 'fit_data3_1'
    f2 = folder + 'fit_data3_2'
    f3 = folder + 'fit_data3_3'
    
    #f1 = folder + 'benparas_compared_newscheme_window95'
    f2 = folder + 'benparas_compared_newscheme_window98'
    f3 = folder + 'benparas_compared_newscheme_window99'

    f2 = folder + 'benparas_astotal_compared_newscheme_window98'
    f3 = folder + 'benparas_astotal_compared_newscheme_window99'

    f2 = folder + 'benparas_astotal_scaled_cost_massfollowslight_compared_newscheme_window98'
    f3 = folder + 'benparas_astotal_scaled_cost_massfollowslight_compared_newscheme_window98'
    
    f2 = folder + 'benparas_astotal_massfollowslight_reducedbaryonscale10_compared_newscheme_window98'
    f3 = folder + 'benparas_astotal_massfollowslight_reducedbaryonscale10_compared_newscheme_window98'
    
    f1 = folder + 'fit_data_converged_11_14_2018_1'
    f2 = folder + 'fit_data_converged_11_14_2018_2'
    f3 = folder + 'fit_data_converged_11_14_2018_3'
    
    fs = [d1, f1, f2, f3]
    
    f1 = folder + 'ben_parameters_baryonmasssameasdata_12_7_2018_smaller_binrange' #1 orphan mass as baryons not compared at all 
    #f1 = folder + 'ben_parameters_baryonmasssameasdata_12_7_2018_compared_4bt_3p95ft1'#same as 1
    f2 = folder + 'ben_parameters_baryonmasssameasdata_12_7_2018_compared_4bt_3p95ft'#2 adjusted orphan mass as baryons compared without best like
    #f2 = folder + 'ben_parameters_baryonmasssameasdata_12_7_2018_compared_4bt_3p95ft2'#same as 2
    f3 = folder + 'ben_parameters_baryonmasssameasdata_12_7_2018_compared_4bt_3p95ft2_bestlike'#3 adjusted orphan mass as baryons compared with best like
    f4 = folder + 'ben_parameters_baryonmasssameasdata_12_7_2018_compared_4bt_3p95ft_datahist_newflags'
    #f4 = folder + 'ben_parameters_baryonmasssameasdata_12_7_2018_compared_4bt_3p95ft2_bestlike_7176steps'
    #f5 = folder + 'ben_parameters_baryonmasssameasdata_12_7_2018_compared_4bt_3p95ft2_bestlike_98to100'
    f5 = folder + 'ben_parameters_baryonmasssameasdata_12_7_2018_compared_4bt_3p95ft_datahist_newflags_alteredbaryons_bestlike'
    #f3 = folder + 'ben_parameters_baryonmasssameasdata_12_7_2018_compared_lowerbaryonmass'
    #f4 = folder + 'ben_parameters_baryonmasssameasdata_12_7_2018_compared_lowerbaryonmass2'
    #f5 = folder + 'ben_parameters_baryonmasssameasdata_12_7_2018_compared_lowerbaryonmass3'
    fs = [d1, f1, f2, f3, f4, f5]
    
    #plot4hists(fs, 'dat')
    #plot_betadisps_hists(fs, 'dat')
    
    #fs = [f1, f2, f3]
    #-1214.631705639678103
    #-116.953356173626347
    #-58.622409798384950
    #-48.494902698171977
    fs = [ f1, f2]
    #lambda_beta_4outputs_plot(fs, 'dat')
    #plot4_lhists(fs, 'dat')
    
    return 0 
main()




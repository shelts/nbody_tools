#! /usr/bin/python
#/* Copyright (c) 2016 Siddhartha Shelton */

import os
import subprocess
from subprocess import call
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math as mt
import matplotlib.patches as mpatches
import random
from nbody_functional import *


# # # # # # # # # # # # # # # # # # # # # #
#        histogram plot                   #
# # # # # # # # # # # # # # # # # # # # # #
# # 
fit_folder = '11.27.fits/'

def plot4hists(hist1, hist2, hist3, hist4, ftype):
    h1 = nbody_histograms(hist1 + '.hist')
    h2 = nbody_histograms(hist2 + '.hist')
    h3 = nbody_histograms(hist3 + '.hist')
    h4 = nbody_histograms(hist4 + '.hist')
    hs = [h1, h2, h3, h4]
    labels = ['data', 'Fit 1', 'Fit 2', 'Fit 3']
    
    labsiz = 20
    fntsiz = 26
    if(ftype == 'sim'):
        xlower = -180.0
        xupper = 180.0
    else:
        xlower = -40.0
        xupper = 40.0
    
    ylower = 0
    yupper = .2
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
        plt.subplot(coor + coori + 1)
        plt.xlim((xlower, xupper))
        plt.ylim((ylower, yupper))
        plt.ylabel('N', fontsize = fntsiz)
        plt.tick_params(axis='y', which='major', labelsize=labsiz)
        plt.tick_params(axis='x', which='major', labelsize=labsiz)
        plt.yticks([0.0, 0.1])
        
        if(coori < len(hs) - 1):#get the tics on the last panel of plot
            plt.xticks([])
        
        if(coori == len(hs) - 1):
            plt.xlabel(r'$\Lambda$', fontsize = fntsiz)
            
        if(coori == 0):
            c = 'r'
        else:
            c = 'k'
        
        plt.bar(hs[coori].lbins, hs[coori].counts, width = wid, color=c, alpha=1, label = labels[coori])
        plt.legend()
        #plt.legend(bbox_to_anchor=(0.5,0.1), loc='center', borderaxespad=0.,  prop={'size': 20}, framealpha=1)

    if(ftype == 'sim'):
        plt.savefig('plots/' + fit_folder + 'fitted_hists_sim_11.27.png', format='png', dpi = 300, bbox_inches='tight')
        #plt.savefig('plots/' + fit_folder + 'fitted_hists_sim.pdf', format='pdf', dpi = 300, bbox_inches='tight')
    else:
        plt.savefig('plots/' + fit_folder + 'fitted_hists_data_11.27.png', format='png', dpi = 300, bbox_inches='tight')
        #plt.savefig('plots/' + fit_folder + 'fitted_hists_data.pdf', format='pdf', dpi = 300, bbox_inches='tight')
    
def plot4_lhists(cor, f1, f2, f3, ftype):#for plotting the data and the fitted values
    cor  = nbody_outputs(cor + '.out')
    out1 = nbody_outputs(f1 + '.out')
    out2 = nbody_outputs(f2 + '.out')
    out3 = nbody_outputs(f3 + '.out')
    
    binN = 100
    cor.dark_light_split()
    cor_lbins = binner([0., 360.], binN, cor.ls)
    
    out1.dark_light_split()
    out1_lbins = binner([0., 360.], binN, out1.ls)
    
    out2.dark_light_split()
    out2_lbins = binner([0., 360.], binN, out2.ls)
    
    out3.dark_light_split()
    out3_lbins = binner([0., 360.], binN, out3.ls)
    
    if(ftype == 'sim'):
        outs = [cor_lbins, out1_lbins, out2_lbins, out3_lbins]
    else:
        outs = ['', out1_lbins, out2_lbins, out3_lbins]
    labels = ['data', 'Fit 1', 'Fit 2', 'Fit 3']
    
    baryon_color = 'r'
    dm_color = 'k'
    labsiz = 20
    fntsiz = 26
    if(ftype == 'sim'):
        xlower = 300.0
        xupper = 120.0
        yupper = 2000
    else:
        xlower = 360.0
        xupper = 120.0
        yupper = 1000
    
    
    ylower = 0
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
    
    for coori in range(len(outs)):
        plt.subplot(coor + coori + 1)
        plt.xlim((xlower, xupper))
        plt.ylim((ylower, yupper))
        plt.ylabel('N', fontsize = fntsiz)
        plt.tick_params(axis='y', which='major', labelsize=labsiz)
        plt.tick_params(axis='x', which='major', labelsize=labsiz)
        #plt.yticks([0.0, 1000])
        
        if(coori < len(outs) - 1):#get the tics on the last panel of plot
            plt.xticks([])
        
        if(coori == len(outs) - 1):
            plt.xlabel(r'$\Lambda$', fontsize = fntsiz)
            
        if(coori == 0):
            c = 'r'
        else:
            c = 'k'
    
        if(ftype == 'sim' or (ftype == 'dat' and coori > 0)):
            plt.bar(outs[coori].bin_centers, outs[coori].counts, width = wid, color=c, alpha=1, label = labels[coori])
        plt.legend()
        #plt.legend(bbox_to_anchor=(0.5,0.1), loc='center', borderaxespad=0.,  prop={'size': 20}, framealpha=1)
        coori += 1

    if(ftype == 'sim'):
        plt.savefig('plots/' + fit_folder + 'fitted_lhists_sim_11.27.png', format='png', dpi = 300, bbox_inches='tight')
        #plt.savefig('plots/' + fit_folder + 'fitted_hists_sim.pdf', format='pdf', dpi = 300, bbox_inches='tight')
    else:
        plt.savefig('plots/' + fit_folder + 'fitted_lhists_data_11.27.png', format='png', dpi = 300, bbox_inches='tight')
        #plt.savefig('plots/' + fit_folder + 'fitted_lhists_sim.pdf', format='pdf', dpi = 300, bbox_inches='tight')


def lambda_beta_4outputs_plot(cor, f1, f2, f3, ftype):#for plotting the data and the fitted values
    if(ftype == 'sim'):
        cor  = nbody_outputs(cor + '.out')
        cor.dark_light_split()
        cor.convert_lambda_beta(True)
    else:
        dat_lambdas = []
        dat_betas = []
        f = open('./create_data_hist/lambda_betas.dat', 'r')
        for line in f:
            ss = line.split('\t')
            dat_lambdas.append(float(ss[0]))
            dat_betas.append(float(ss[1]))
        f.close()
        
    out1 = nbody_outputs(f1 + '.out')
    out2 = nbody_outputs(f2 + '.out')
    out3 = nbody_outputs(f3 + '.out')
    
    
    out1.dark_light_split()
    out1.convert_lambda_beta(True)
    
    out2.dark_light_split()
    out2.convert_lambda_beta(True)
    
    out3.dark_light_split()
    out3.convert_lambda_beta(True)
    
    if(ftype == 'sim'):
        outs = [cor, out1, out2, out3]
    else:
        outs = ['', out1, out2, out3]
    labels = ['data', 'Fit 1', 'Fit 2', 'Fit 3']
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
        plt.subplot(coor + coori + 1)
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
        plt.savefig('plots/' + fit_folder + 'fitted_lambda_beta_sim_11.27.png', format='png', dpi = 300, bbox_inches='tight')
        #plt.savefig('plots/' + fit_folder + 'fitted_lambda_beta_sim.pdf', format='pdf', dpi = 300, bbox_inches='tight')
    else:
        plt.savefig('plots/' + fit_folder + 'fitted_lambda_beta_data_11.27.png', format='png', dpi = 300, bbox_inches='tight')
        #plt.savefig('plots/' + fit_folder + 'fitted_lambda_beta_data.pdf', format='pdf', dpi = 300, bbox_inches='tight')


def plot_betadisps_hists(hist1, hist2, hist3, hist4, ftype):#plots the dispersions from the histograms with lambda beta on top. for 2 hists
    h1 = nbody_histograms(hist1 + '.hist')
    h2 = nbody_histograms(hist2 + '.hist')
    h3 = nbody_histograms(hist3 + '.hist')
    h4 = nbody_histograms(hist4 + '.hist')
    hs = [h1, h2, h3, h4]
    labels = ['data', 'Fit 1', 'Fit 2', 'Fit 3']
    
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
        plt.subplot(coor + coori + 1)
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
            
        if(coori == 0):
            c = 'r'
        else:
            c = 'k'
        
        plt.bar(hs[coori].lbins, hs[coori].bd, width = wid, color=c, alpha=1, label = labels[coori])
        plt.legend()
        #plt.legend(bbox_to_anchor=(0.5,0.1), loc='center', borderaxespad=0.,  prop={'size': 20}, framealpha=1)

    if(ftype == 'sim'):
        plt.savefig('plots/' + fit_folder + 'fitted_betadisp_hists_sim_11.27.png', format='png', dpi = 300, bbox_inches='tight')
        #plt.savefig('plots/' + fit_folder + 'fitted_hists_sim.pdf', format='pdf', dpi = 300, bbox_inches='tight')
    else:
        plt.savefig('plots/' + fit_folder + 'fitted_betadisp_hists_data_11.27.png', format='png', dpi = 300, bbox_inches='tight')
        #plt.savefig('plots/' + fit_folder + 'fitted_hists_data.pdf', format='pdf', dpi = 300, bbox_inches='tight')

    #plt.show()
    return 1




def main():
    path = '/home/sidd/Desktop/research/'

    folder = path + 'quick_plots/hists_outs/'
    
    cor = folder + 'hist_v172_3p95_0p2_0p2_12_0p2__11_7_18'
    f1 = folder + 'fit_sim1'
    f2 = folder + 'fit_sim2'
    f3 = folder + 'fit_sim3'
    #cor = folder + ''
    
    plot4hists(cor, f1, f2, f3, 'sim')
    plot4_lhists(cor, f1, f2, f3, 'sim')
    plot_betadisps_hists(cor, f1, f2, f3, 'sim')
    lambda_beta_4outputs_plot(cor, f1, f2, f3, 'sim')
    
    d1 = folder + 'data_hist_fall_2018'
    f1 = folder + 'fit_data3_1'
    f2 = folder + 'fit_data3_2'
    f3 = folder + 'fit_data3_3'
    plot4hists(d1, f1, f2, f3, 'dat')
    plot4_lhists(f1, f1, f2, f3, 'dat')
    plot_betadisps_hists(d1, f1, f2, f3, 'dat')
    lambda_beta_4outputs_plot(d1, f1, f2, f3, 'dat')
    
    return 0 

main()




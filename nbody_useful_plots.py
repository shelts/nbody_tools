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

# # 

def plot_disps(file1):#plots the dispersions from the histogram with lambda beta on top
    ylimit = 1
    xlower = -75 
    xupper = 150
    w_overlap = 2.5
    w_adjacent = 4
    #folder = 'like_surface/'
    save_folder = '/home/sidd/Desktop/research/quick_plots/publish_plots/'
    save_folder_adj = '/home/sidd/Desktop/research/quick_plots/comp_hist_plots/adj/'

    print "plot histogram 1: ", file1

    print("plotting histograms\n")
    hist1 = nbody_histograms(file1 + ".hist")
    out1 = nbody_outputs(file1 + ".out")
    
    out1.dark_light_split()
    out1.convert_lambda_beta(True)    
    
    
    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row')
    f.subplots_adjust(hspace=0)
    f.subplots_adjust(wspace=0)
    
    
    
    ax1 = plt.subplot(411)
    plt.xlim((xlower, xupper))
    plt.ylim((-10, 10))
    #plt.xlabel(r'$\Lambda_{Orphan}$')
    plt.ylabel(r'$\beta_{Orphan}$')
    #plt.title(r'Simulated Orphan Stream')
    #plt.plot(out1.dark_lambdas, out1.dark_betas, '.', markersize = .75, color = 'red', alpha=1., marker = '.', label = 'Dark Matter')
    plt.plot(out1.light_lambdas, out1.light_betas, '.', markersize = .75, color = 'b', alpha=.75, marker = '.', label = 'Stars')
    plt.xticks([])
    plt.yticks([-10, 0, 10])
    
    ax2 = plt.subplot(412)
    plt.bar(hist1.lbins, hist1.counts, width = w_adjacent, color='r')
    #plt.legend(handles=[mpatches.Patch(color='b', label= 'Counts')])
    #plt.title('Line of Sight Vel Disp Distribution')
    plt.xlim((xlower, xupper))
    plt.ylim((0.0, .2))
    plt.ylabel('N')
    plt.xticks([])
    plt.yticks([0.05, 0.1, 0.15])
    #plt.xlabel(r'\sigma_{v_{los}} (km/s)')
    
    ax3 = plt.subplot(413)
    #f, (f1, f2) = plt.subplots(2, sharex = True, sharey = True)
    plt.bar(hist1.lbins, hist1.bd, width = w_adjacent, color='darkgreen')
    #plt.legend(handles=[mpatches.Patch(color='b', label= plot_hist1)])
    #plt.title('Line of Sight Vel Disp Distribution')
    plt.xlim((xlower, xupper))
    plt.ylim((0.0, 2.5))
    plt.ylabel(r'$\sigma_{\beta_{Orphan}}$')
    #plt.xlabel('Lambda')
    plt.xticks([])
    plt.yticks([0.5, 1, 1.5, 2.0])
    
    ax4 = plt.subplot(414)
    plt.bar(hist1.lbins, hist1.vd, width = w_adjacent, color='k')
    #plt.legend(handles=[mpatches.Patch(color='k', label= plot_hist1)])
    plt.xlim((xlower, xupper))
    plt.ylim((0.0, 10))
    plt.yticks([2.0, 4.0, 6.0, 8.0])
    plt.ylabel(r'$\sigma_{v_{los}}$ (km/s)')
    plt.xlabel(r'$\Lambda_{Orphan}$')
    plt.savefig(save_folder + 'disps.png', format='png', bbox_inches='tight')
    plt.clf()
    #plt.show()
    return 1


# # # # # # # # # # # # # # # # # # # # # #
#        NON-histogram plot               #
# # # # # # # # # # # # # # # # # # # # # #
# #



def vlos_plot_single(file1):#plots the line of sight velocity from outputs with hist counts
    ylimit = 100
    xlower = 180 
    xupper = -180
    w_overlap = 2.5
    w_adjacent = 1.5
    folder_hist = 'quick_plots/hists/'
    folder_outs = 'quick_plots/outputs/'
    save_folder_adj = 'quick_plots/comp_hist_plots/adj/'
    save_folder_ove = 'quick_plots/comp_hist_plots/overlap/'
    
    print "plot histogram 1: ", file1
    
    plot_hist1 = file1 + ".hist"
    
    output1 = file1 + ".out"
    
    label1 = '1'
    
    name = 'vlos_plots'
    print("plotting histograms\n")
    
    hist1 = nbody_histograms(folder_hist + plot_hist1)
     
    angle_cuttoffs = [-150.0, 150.0, 50, -15.0, 15.0, 1]
    
    out1 = nbody_outputs(folder_outs + output1)
    
    out1.binner_vlos(angle_cuttoffs)#bin the line of sight vels
    # plot overlapping #
    count_y_limit = 0.4
    rawcount_y_limit = 2000
    vel_disp_ylimit = 50
    
    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row')
    f.subplots_adjust(hspace=0)
    f.subplots_adjust(wspace=0)

    ax1 = plt.subplot(311)
    plt.bar(hist1.lbins, hist1.counts, width = w_adjacent, color='k', alpha=1)
    #plt.title(r'Line of Sight $\sigma_{line of sight}$ Distribution')
    plt.xlim((xlower, xupper))
    plt.ylim((0.0, count_y_limit))
    plt.ylabel('counts')
    plt.legend()
    
    #ax3 = plt.subplot(412)
    #plt.bar(hist1.lbins, hist1.count_err, width = w_adjacent, color='k', alpha=1)
    #plt.xlim((xlower, xupper))
    #plt.ylim((0.0, count_y_limit**0.5))
    #plt.ylabel('Count error')
    #plt.xlabel('Lambda')
    #plt.legend()
    
    ax2 = plt.subplot(312)
    plt.bar(hist1.lbins, hist1.vd, width = w_adjacent, color='k', alpha=1)
    plt.xlim((xlower, xupper))
    plt.ylim((0.0, vel_disp_ylimit))
    plt.ylabel(r'$\sigma$ (km/s)')
    #plt.legend()
    
    ax2 = plt.subplot(313)
    plt.scatter(out1.which_bin, out1.binned_vlos, s=2, marker= '.',  color='k', alpha=1, edgecolors='none')
    plt.xlim((xlower, xupper))
    #plt.ylim((0.0, vel_disp_ylimit))
    plt.ylabel(r'${v_{los}}$ (km/s)')
    #plt.legend()
    plt.xlabel(r'$\Lambda$')
    plt.savefig(save_folder_ove + name + '_overlapping_single.png', format='png', dpi=500)
    #plt.clf()
    #plt.show()
    
    return 1

def vlos_plot(file1, file2): 
    ylimit = 100
    xlower = 180 
    xupper = -180
    w_overlap = 2.5
    w_adjacent = 1.5
    folder_hist = 'quick_plots/hists/'
    folder_outs = 'quick_plots/outputs/'
    save_folder_adj = 'quick_plots/comp_hist_plots/adj/'
    save_folder_ove = 'quick_plots/comp_hist_plots/overlap/'
    
    print "plot histogram 1: ", file1
    print "plot histogram 2: ", file2
    
    plot_hist1 = file1 + ".hist"
    plot_hist2 = file2 + ".hist"
    
    output1 = file1 + ".out"
    output2 = file2 + ".out"
    
    label1 = '1'
    label2 = '2'
    
    name = 'vlos_plots'
    print("plotting histograms\n")
    
    hist1 = nbody_histograms(folder_hist + plot_hist1)
    hist2 = nbody_histograms(folder_hist + plot_hist2)
     
    angle_cuttoffs = [-150.0, 150.0, 50, -15.0, 15.0, 1]
    
    out1 = nbody_outputs(folder_outs + output1)
    out2 = nbody_outputs(folder_outs + output2)
    
    out1.binner_vlos(angle_cuttoffs)#bin the line of sight vels
    out2.binner_vlos(angle_cuttoffs)
    
    # plot_adjacent #
    count_y_limit = 0.4
    rawcount_y_limit = 2000
    vel_disp_ylimit = 100
    
    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row')
    f.subplots_adjust(hspace=0)
    f.subplots_adjust(wspace=0)
    #plt.subplots(4, sharex = True, sharey = True)
    ax1 = plt.subplot(421)
    plt.bar(hist1.lbins, hist1.counts, width = w_adjacent, color='b')
    plt.title('Line of Sight Vel Disp Distribution')
    plt.xlim((xlower, xupper))
    plt.ylim((0.0, count_y_limit))
    plt.ylabel('counts')

    ax2 = plt.subplot(422)
    plt.bar(hist2.lbins, hist2.counts, width = w_adjacent, color='k')
    plt.xlim((xlower, xupper))
    plt.ylim((0.0, count_y_limit))
    plt.yticks([])

    ax5 = plt.subplot(423)
    plt.bar(hist1.lbins, hist1.count_err, width = w_adjacent, color='b')
    plt.xlim((xlower, xupper))
    plt.ylim((0.0, rawcount_y_limit))
    plt.ylabel('raw count')
    #plt.xlabel('Lambda')

    ax6 = plt.subplot(424)
    plt.bar(hist2.lbins, hist2.count_err, width = w_adjacent, color='k')
    plt.xlim((xlower, xupper))
    plt.ylim((0.0, rawcount_y_limit))
    plt.yticks([])
    #plt.xlabel('Lambda')
    
    ax3 = plt.subplot(425)
    #plt.subplots(2, sharex = True, sharey = False)
    plt.bar(hist1.lbins, hist1.vd, width = w_adjacent, color='b')
    plt.xlim((xlower, xupper))
    plt.ylim((0.0, vel_disp_ylimit))
    plt.ylabel('vel disp')

    ax4 = plt.subplot(426)
    plt.bar(hist2.lbins, hist2.vd, width = w_adjacent, color='k')
    plt.xlim((xlower, xupper))
    plt.ylim((0.0, vel_disp_ylimit))
    plt.yticks([])
    
    ax3 = plt.subplot(427)
    #plt.subplots(2, sharex = True, sharey = False)
    plt.scatter(out1.which_bin, out1.binned_vlos, color='b', s=.5, marker= 'o')
    plt.xlim((xlower, xupper))
    #plt.ylim((0.0, vel_disp_ylimit))
    plt.ylabel('vel disp')

    ax4 = plt.subplot(428)
    plt.scatter(out2.which_bin, out2.binned_vlos, color='k', s=.5, marker= 'o', )
    plt.xlim((xlower, xupper))
    #plt.ylim((0.0, vel_disp_ylimit))
    plt.yticks([])
    plt.savefig(save_folder_adj + name + '.png', format='png', dpi=1000)
    
     # plot overlapping #   
    count_y_limit = 0.4
    rawcount_y_limit = 2000
    vel_disp_ylimit = 100
    
    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row')
    f.subplots_adjust(hspace=0)
    f.subplots_adjust(wspace=0)

    ax1 = plt.subplot(411)
    plt.bar(hist1.lbins, hist1.counts, width = w_adjacent, color='k', alpha=1,    label= label1)
    plt.bar(hist2.lbins, hist2.counts, width = w_adjacent, color='r', alpha=0.75, label= label2)
    plt.title('Line of Sight Vel Disp Distribution')
    plt.xlim((xlower, xupper))
    plt.ylim((0.0, count_y_limit))
    plt.ylabel('counts')
    plt.legend()
    
    ax3 = plt.subplot(412)
    plt.bar(hist1.lbins, hist1.count_err, width = w_adjacent, color='k', alpha=1,    label= label1)
    plt.bar(hist2.lbins, hist2.count_err, width = w_adjacent, color='r', alpha=0.75, label= label2)
    plt.xlim((xlower, xupper))
    plt.ylim((0.0, rawcount_y_limit))
    plt.ylabel('raw count')
    plt.xlabel('Lambda')
    plt.legend()
    
    ax2 = plt.subplot(413)
    plt.bar(hist1.lbins, hist1.vd, width = w_adjacent, color='k', alpha=1,    label= label1)
    plt.bar(hist2.lbins, hist2.vd, width = w_adjacent, color='r', alpha=0.75, label= label2)
    plt.xlim((xlower, xupper))
    plt.ylim((0.0, vel_disp_ylimit))
    plt.ylabel('vel disp')
    plt.legend()
    
    ax2 = plt.subplot(414)
    plt.scatter(out1.which_bin, out1.binned_vlos, s=1, marker= '.',  color='red', alpha=1,label= label1, edgecolors='none')
    plt.scatter(out2.which_bin, out2.binned_vlos, s=1, marker= '.', color='blue', alpha=1, label= label2, edgecolors='none')
    plt.xlim((xlower, xupper))
    #plt.ylim((0.0, vel_disp_ylimit))
    plt.ylabel('vel disp')
    plt.legend()
    plt.savefig(save_folder_ove + name + '_overlapping.png', format='png', dpi=1000)
    #plt.clf()
    #plt.show()
    
    return 1


# # # # # # # # # # # # # # # # # # # # # #
#        Standard needed plots            #
# # # # # # # # # # # # # # # # # # # # # #


 
def lb_plot(file_name): #plots lb from output
    path_charles = 'quick_plots/outputs/'
    path = ''
    print file_name
    plot_lbr = False
    plot_light_and_dark = True
    plot_dm_only = False
    plot_xyz = True
    plot_xyz_3d = False
    out = nbody_outputs(path + file_name + '.out')
    out.rescale_l()
    out.dark_light_split()
    
    fig = plt.figure()
    fig.subplots_adjust(hspace = 1., wspace = 0.8)
    
    # # # # # # # # # #
    if(plot_lbr):
        plt.figure(figsize=(10, 10))
        xlower = -180.0
        xupper = 180.0
        ylower = -80
        yupper = 80
        plt.xlim((xlower, xupper))
        plt.ylim((ylower, yupper))
        plt.xlabel('l')
        plt.ylabel('b')
        plt.title('l vs b')
        #default to just plot lm
        plt.plot(out.light_l, out.light_b, '.', markersize = 1., color = 'b', alpha=1.0, marker = '.', label = 'baryons')
        plt.legend()
        plt.savefig(file_name, format='png')
        print "plotting:", len(out.light_l), " points"
        # # # # # # # # # #
        if(plot_light_and_dark):#plot lm and dm overlapping
            plt.xlim((xlower, xupper))
            plt.ylim((ylower, yupper))
            plt.xlabel('l')
            plt.ylabel('b')
            plt.title('l vs b')
            plt.plot(out.dark_l, out.dark_b, '.', markersize = 1, color = 'red', alpha=.25, marker = '.', label = 'dark matter')
            plt.legend()
            plt.savefig(file_name, format='png')
            print "plotting:", len(out.light_l) + len(out.dark_l), " points"
        # # # # # # # # # #
        if(plot_dm_only):#to plot just dm
            plt.clf()
            plt.figure(figsize=(20, 20))
            plt.xlim((xlower, xupper))
            plt.ylim((ylower, yupper))
            plt.xlabel('l')
            plt.ylabel('b')
            plt.title('l vs b')
            plt.plot(out.dark_l, out.dark_b, '.', markersize = 1, color = 'b', marker = '+')
            plt.savefig(file_name + '_tidal_stream_lbr_dark', format='png')
            
    if(plot_xyz):
        plt.figure(figsize=(10, 20))
        xlower = .5
        xupper = -.5
        ylower = -.5
        yupper = .5
        
        xlower = -50
        xupper = 50
        ylower = -60
        yupper = 60
        ms = 0.5
        #fig.tight_layout()
        plt.axes().set_aspect('equal')
        plt.subplot(311, aspect='equal')
        #plt.subplot(311)
        plt.tick_params(axis='y', which='major', labelsize=22)
        plt.tick_params(axis='x', which='major', labelsize=22)
        if(plot_light_and_dark == True):
            plt.plot(out.dark_x, out.dark_y, '.', markersize = ms, color = 'k', marker = '.')
        plt.plot(out.light_x, out.light_y, '.', markersize = ms, color = 'b', marker = '.')
        
        plt.xlim((xlower, xupper))
        plt.ylim((ylower, yupper))
        plt.xlabel('x', fontsize=24)
        plt.ylabel('y', fontsize=24)
        #plt.title('x vs y')
        
        plt.subplot(312,aspect='equal')
        #plt.subplot(312)
        plt.tick_params(axis='y', which='major', labelsize=22)
        plt.tick_params(axis='x', which='major', labelsize=22)
        if(plot_light_and_dark == True):
            plt.plot(out.dark_x, out.dark_z, '.', markersize = ms, color = 'k', marker = '.')
        
        plt.plot(out.light_x, out.light_z, '.', markersize = ms, color = 'b', marker = '.')
        
        plt.xlim((xlower, xupper))
        plt.ylim((ylower, yupper))
        plt.xlabel('x', fontsize=24)
        plt.ylabel('z', fontsize=24)
        #plt.title('x vs z')
        
        plt.subplot(313, aspect='equal')
        #plt.subplot(313)
        plt.tick_params(axis='y', which='major', labelsize=22)
        plt.tick_params(axis='x', which='major', labelsize=22)
        if(plot_light_and_dark == True):
            plt.plot(out.dark_z, out.dark_y, '.', markersize = ms, color = 'k', marker = '.')
        plt.plot(out.light_z, out.light_y, '.', markersize = ms, color = 'b', marker = '.')
        
        plt.xlim((xlower, xupper))
        plt.ylim((ylower, yupper))
        plt.xlabel('z', fontsize=24)
        plt.ylabel('y', fontsize=24)
        #plt.title('z vs y')
        plt.savefig('plots/simulation2.png', format='png', bbox_inches='tight')
    
    
    if(plot_xyz_3d):
        xlower = .5
        xupper = -.5
        ylower = -.5
        yupper = .5
        ms = 0.5
        #fig.tight_layout()
        fig =  plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlim(xlower, xupper)
        ax.set_ylim(xlower, xupper)
        ax.set_zlim(xlower, xupper)
        ax.set_xlabel('X ')
        ax.set_ylabel('Y ')
        ax.set_zlabel('Z ')
        ax.scatter(out.light_x, out.light_y, out.light_z, s = ms, color = 'b', marker = '.')
        plt.savefig(file_name + 'ultrafaint_tidal_stream_xyz_3d_light.png', format='png', dpi=200)
        
        ms = 1.1
        ax.scatter(out.light_x, out.light_y, out.light_z, s = 0.5, color = 'b', marker = 'o')
        ax.scatter(out.dark_x, out.dark_y, out.dark_z,  s= ms, color = 'k', alpha = 1, marker = '.')
        
        plt.savefig(file_name + 'ultrafaint_tidal_stream_xyz_3d.png', format='png', dpi=200)
        #plt.show()
    
        
    return 0


# # # # # # # # # # # # # # # # # # # # # #
#        Very Specific Plots              #
# # # # # # # # # # # # # # # # # # # # # #
# #

def lambda_beta_light_dark_histogram_plot(file_name):
    out = nbody_outputs(file_name + '.out')
    angle_cuttoffs = [-150.0, 150.0, 50, -15.0, 15.0, 1]
    out.binner(angle_cuttoffs)
    out.cross_selection(True, 2500)
    baryon_color = 'r'
    dm_color = 'k'
    labsiz = 20
    fntsiz = 26
    xlower = -180.0
    xupper = 180.0
    ylower = -11
    yupper = 11
    
    coor  = 310
    coori = 1
    
    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row', figsize=(15, 10))
    f.subplots_adjust(hspace=0)
    #f.subplots_adjust(wspace=0)
    params = {'legend.fontsize': 20,
            'legend.handlelength': 1}
    plt.rcParams.update(params)
    
    #plt.subplot(coor + coori)
    #plt.xlim((xlower, xupper))
    #plt.ylim((ylower, yupper))
    #plt.title(r'$\Lambda$ vs $\beta$', fontsize = 30)
    #plt.ylabel(r'$\beta$', fontsize = fntsiz)
    
    #plt.tick_params(axis='y', which='major', labelsize=labsiz)
    #plt.tick_params(axis='x', which='major', labelsize=labsiz)
    #plt.plot(out.dark_lambdas, out.dark_betas, '.', markersize = .5, color = dm_color, alpha=.75, marker = '.', label = 'dark matter')
    #plt.plot(out.light_lambdas, out.light_betas, '.', markersize = .75, color = baryon_color, alpha=1.0, marker = '.',label = 'baryons')
    #plt.legend()
    #coori += 1
    
    plt.subplot(coor + coori)
    plt.xlim((xlower, xupper))
    plt.ylim((ylower, yupper))
    plt.ylabel(r'$\beta$', fontsize = fntsiz)
    
    plt.tick_params(axis='y', which='major', labelsize=labsiz)
    plt.tick_params(axis='x', which='major', labelsize=labsiz)
    plt.plot(out.light_lambdas, out.light_betas, '.', markersize = .75, color = baryon_color, alpha=0.75, marker = '.',label = 'Baryonic Matter')
    plt.legend()
    coori += 1
    
    plt.subplot(coor + coori)
    plt.xlim((xlower, xupper))
    plt.ylim((ylower, yupper))
    plt.ylabel(r'$\beta$', fontsize = fntsiz)
    
    plt.tick_params(axis='y', which='major', labelsize=labsiz)
    plt.tick_params(axis='x', which='major', labelsize=labsiz)
    plt.plot(out.dark_lambdas, out.dark_betas, '.', markersize = .5, color = dm_color, alpha=.75, marker = '.', label = 'Dark Matter')
    plt.legend()
    coori += 1


    plt.subplot(coor + coori)
    plt.xlim((xlower, xupper))
    #plt.ylim((0, 0.3))
    plt.xlabel(r'$\Lambda$', fontsize = fntsiz)
    plt.ylabel('N', fontsize = fntsiz)
    
    plt.tick_params(axis='y', which='major', labelsize=labsiz)
    plt.tick_params(axis='x', which='major', labelsize=labsiz)
    plt.bar(out.mid_bins, out.dm_normed, width = 5., color=dm_color,hatch="xxx", alpha=0.75, label = 'Dark Matter')
    plt.bar(out.mid_bins, out.bm_normed, width = 5., color=baryon_color, hatch="\\\\", alpha=0.5, label = 'Baryonic Matter')
    plt.legend()
    coori += 1

    plt.savefig(file_name + '_lambdabeta_hist.png', format='png', dpi = 300)
    plt.savefig(file_name + '_lambdabeta_hist.pdf', format='pdf', dpi = 300)
    
    
    # just plotting the overlapping lambda beta and the histograms.
    plt.clf()
    plt.subplot(211)
    plt.tick_params(axis='y', which='major', labelsize=labsiz)
    plt.tick_params(axis='x', which='major', labelsize=labsiz)
    plt.xlim((xlower, xupper))
    plt.ylim((ylower, yupper))
    #plt.title(r'$\Lambda$ vs $\beta$', fontsize = 26)
    plt.ylabel(r'$\beta$', fontsize = fntsiz)
    plt.yticks([-10, -5, 0, 5, 10])
    
    plt.tick_params(axis='y', which='major', labelsize=labsiz)
    plt.tick_params(axis='x', which='major', labelsize=labsiz)
    plt.plot(out.sub_dark_lambdas, out.sub_dark_betas, '.', markersize = 4, color = dm_color, alpha=.75, marker = '.', label = 'dark matter')
    plt.plot(out.sub_light_lambdas, out.sub_light_betas, '.', markersize = 4.25, color = baryon_color, alpha=1.0, marker = '.',label = 'baryons')
    plt.legend()

    plt.subplot(212)
    plt.tick_params(axis='y', which='major', labelsize=labsiz)
    plt.tick_params(axis='x', which='major', labelsize=labsiz)
    plt.xlim((xlower, xupper))
    #plt.ylim((0, 0.3))
    plt.xlabel(r'$\Lambda$', fontsize = fntsiz)
    plt.ylabel('N', fontsize = fntsiz)
    plt.yticks([0.02, 0.04, .06, .08])
    plt.tick_params(axis='y', which='major', labelsize=labsiz)
    plt.tick_params(axis='x', which='major', labelsize=labsiz)
    plt.bar(out.mid_bins, out.dm_normed, width = 5., color=dm_color, hatch="xxx", alpha=0.75, label = 'dark matter')
    plt.bar(out.mid_bins, out.bm_normed, width = 5., color=baryon_color, hatch="\\\\", alpha=0.5, label = 'baryons')
    plt.legend()

    plt.savefig(file_name + '_lambdabeta_hist2_11_7.png', format='png', dpi = 300)
    plt.savefig(file_name + '_lambdabeta_hist2_11_7.pdf', format='pdf', dpi = 200)


def plot_hist_lambda_beta(file1, file2, file_name = None):
    path = '/home/sidd/Desktop/research/quick_plots/hists_outs/'
    
    out1 = nbody_outputs(path + file1 + ".out")
    out2 = nbody_outputs(path + file2 + ".out")
    
    hist1 = nbody_histograms(path + file1 + ".hist")
    hist2 = nbody_histograms(path + file2 + ".hist")
    
    w_overlap = 2.5
    w_adjacent = 1.5
    count_y_limit = 0.4
    out1.dark_light_split()
    out1.convert_lambda_beta(True)
    
    out2.dark_light_split()
    out2.convert_lambda_beta(True)
    xlower = -180.0
    xupper = 180.0
    ylower = -80
    yupper = 80
    
    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row')
    f.subplots_adjust(hspace=0)
    f.subplots_adjust(wspace=0)
    plt.figure(figsize=(20, 10))
    ax1 = plt.subplot(221)
    plt.xlim((xlower, xupper))
    plt.ylim((ylower, yupper))
    plt.ylabel(r'$\beta$')
    plt.title(r'$\Lambda$ vs $\beta$')
    #default to just plot lm
    if(not file_name):
        plt.plot(out1.dark_lambdas, out1.dark_betas, '.', markersize = .5, color = 'black', alpha=.75, marker = '.', label = 'dark matter')
    plt.plot(out1.light_lambdas, out1.light_betas, '.', markersize = .75, color = 'b', alpha=1.0, marker = '.', label = 'baryons')
    plt.legend()
    #plt.subplots(4, sharex = True, sharey = True)
    
    
    ax2 = plt.subplot(222)
    plt.xlim((xlower, xupper))
    plt.ylim((ylower, yupper))
    plt.xlabel(r'$\Lambda$')
    #plt.ylabel(r'$\beta$')
    plt.title(r'$\Lambda$ vs $\beta$')
    if(not file_name):
        plt.plot(out2.dark_lambdas, out2.dark_betas, '.', markersize = .5, color = 'black', alpha=.75, marker = '.', label = 'dark matter')
    plt.plot(out2.light_lambdas, out2.light_betas, '.', markersize = .75, color = 'b', alpha=1.0, marker = '.',label = 'baryons')
    
    ax5 = plt.subplot(223)
    plt.bar(hist1.lbins, hist1.counts, width = w_adjacent, color='b')
    plt.xlim((xlower, xupper))
    plt.ylim((0.0, count_y_limit))
    plt.xlabel(r'$\Lambda$')
    plt.ylabel('counts')
    
    #plt.legend()
    
    
    ax6 = plt.subplot(224)
    plt.bar(hist2.lbins, hist2.counts, width = w_adjacent, color='k')
    plt.xlim((xlower, xupper))
    plt.xlabel(r'$\Lambda$')
    plt.ylim((0.0, count_y_limit))
    plt.ylabel('counts')
    #plt.yticks([])
    
    #plt.show()
    if(not file_name):
        plt.savefig('/home/sidd/Desktop/research/quick_plots/lambda_beta_with_dark', format='png')
    else:
        plt.savefig('/home/sidd/Desktop/research/quick_plots/lambda_beta_without_dark', format='png')
            
    return 0 

def plot_hist_lambda_beta_single(file1, file_name = None):
    path = 'quick_plots/'
    hist = path + 'hists/'
    outs = path + 'outputs/'
    
    out1 = nbody_outputs(outs + file1 + ".out")
    
    hist1 = nbody_histograms(hist + file1 + ".hist")
    
    w_overlap = 2.5
    w_adjacent = 1.5
    count_y_limit = 0.4
    out1.dark_light_split()
    out1.convert_lambda_beta(True)
    
    xlower = -180.0
    xupper = 180.0
    yupper = 30
    ylower = -yupper
    
    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row')
    f.subplots_adjust(hspace=0)
    f.subplots_adjust(wspace=0)
    #plt.figure(figsize=(10, 5))
    ax1 = plt.subplot(211)
    plt.xlim((xlower, xupper))
    plt.ylim((ylower, yupper))
    plt.ylabel(r'$\beta$')
    plt.title(r'$\Lambda$ vs $\beta$')
    plt.yticks( [ 20, 10, 0, -10, -20])
    #default to just plot lm
    if(not file_name):
        plt.plot(out1.dark_lambdas, out1.dark_betas, '.', markersize = .5, color = 'black', alpha=.75, marker = '.', label = 'dark matter')
    plt.plot(out1.light_lambdas, out1.light_betas, '.', markersize = .75, color = 'b', alpha=1.0, marker = '.', label = 'baryons')
    plt.legend()
    #plt.subplots(4, sharex = True, sharey = True)
    
    
    
    ax5 = plt.subplot(212)
    plt.bar(hist1.lbins, hist1.counts, width = w_adjacent, color='b')
    plt.xlim((xlower, xupper))
    plt.ylim((0.0, count_y_limit))
    plt.xlabel(r'$\Lambda$')
    plt.ylabel('counts')
    
    if(not file_name):
        plt.savefig('/home/sidd/Desktop/research/quick_plots/lambda_beta_with_dark', format='png')
    else:
        plt.savefig('/home/sidd/Desktop/research/quick_plots/lambda_beta_without_dark', format='png')
            
    return 0 


def single_xyz(file_name):
    path = 'quick_plots/hists_outs/'
    print file_name
    plot_light_and_dark = True
    plot_dm = True
    
    out = nbody_outputs(file_name + '.out')
    out.rescale_l()
    out.dark_light_split()
    
    fig = plt.figure()
    fig.subplots_adjust(hspace = 0.8, wspace = 0.8)
    # # # # # # # # # #
            
    xlower = 1
    xupper = -1
    ylower = 1
    yupper = -1
    #fig.tight_layout()
    #plt.axes().set_aspect('equal')
    plt.figure(figsize=(10, 10))
    plt.subplot(131,aspect='equal')
    plt.plot(out.light_x, out.light_y, '.', markersize = 1, color = 'r', marker = 'o')
    
    if(plot_light_and_dark == True):
        plt.plot(out.dark_x, out.dark_y, '.', markersize = 1, color = 'b', marker = '+')
    
    plt.xlim((xlower, xupper))
    plt.ylim((ylower, yupper))
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('x vs y')
    
    plt.subplot(132,aspect='equal')
    
    plt.plot(out.light_x, out.light_z, '.', markersize = 1, color = 'r', marker = 'o')
    
    if(plot_light_and_dark == True):
        plt.plot(out.dark_x, out.dark_z, '.', markersize = 1, color = 'b', marker = '+')
    
    plt.xlim((xlower, xupper))
    plt.ylim((ylower, yupper))
    plt.xlabel('x')
    plt.ylabel('z')
    plt.title('x vs z')
    
    plt.subplot(133, aspect='equal')
    
    plt.plot(out.light_z, out.light_y, '.', markersize = 1, color = 'r', marker = 'o')
    if(plot_light_and_dark == True):
        plt.plot(out.dark_z, out.dark_y, '.', markersize = 1, color = 'b', marker = '+')
    
    plt.xlim((xlower, xupper))
    plt.ylim((ylower, yupper))
    plt.xlabel('z')
    plt.ylabel('y')
    plt.title('z vs y')
    plt.savefig('/home/sidd/Desktop/research/quick_plots/ultrafaint_tidal_stream_xyz', format='png')

    return 0


def main():
    path = '/home/sidd/Desktop/research/'

    folder = path + 'quick_plots/hists_outs/'
    file1 = folder + 'ultrafaint'
    #file2 = 'arg_3.95_0.2_0.2_12_0.2_correct1'
    
    
    #plot_hist_lambda_beta(file1, file2)
    
    hist1 = folder + 'hist_v172_3p95_0p2_0p2_12_0p2__9_24_18'
    hist2 = folder + 'hist_v172_4_0p2_0p2_12_0p2__9_25_18'
    #name = 'mwh_hist'
    
    #single_xyz(file1)
    #lb_plot(file1)
    hist1 = folder + 'hist_v172_3p95_0p2_0p2_12_0p2__11_7_18'
    lambda_beta_light_dark_histogram_plot(hist1)
    
    file1 = folder + 'reverse_orbit'
    #lb_plot(file1)
    
    
    return 0 

main()




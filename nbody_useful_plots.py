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

def plot(hist1, hist2, name, label1, label2): #plots two histograms. 
    ylimit = 0.4
    xlower = 180 
    xupper = -180
    w_overlap = 2.5
    w_adjacent = 3.5
    folder = 'quick_plots/hists/'
    #folder = ''
    #folder = 'like_surface/'
    save_folder_ove = 'quick_plots/comp_hist_plots/overlap/'
    save_folder_adj = 'quick_plots/comp_hist_plots/adj/'
    #os.system("" + path + "scripts/plot_matching_hist.py " + hist1 + " " + hist2)
    print "plot histogram 1: ", hist1
    print "plot histogram 2: ", hist2
    plot_hist1 = hist1 + ".hist"
    plot_hist2 = hist2 + ".hist"

    
    print("plotting histograms\n")
    hist1 = nbody_histograms(folder + plot_hist1)
    hist2 = nbody_histograms(folder + plot_hist2)
            
            
    # plot overlapping #
    #f, (f1, f2) = plt.subplots(2, sharex = True, sharey = True)
    #plt.subplot(211)
    plt.bar(hist1.lbins, hist1.counts, width = w_overlap, color='k', alpha=1,    label= label1)
    plt.bar(hist2.lbins, hist2.counts, width = w_overlap, color='r', alpha=0.75, label= label2)
    plt.title('Histogram of Light Matter Distribution After 4 Gy')
    plt.xlim((xlower, xupper))
    plt.ylim((0.0, ylimit))
    plt.ylabel('N')
    plt.xlabel(r'$\Lambda$')
    plt.legend()
    plt.savefig(save_folder_ove + name + '_overlapping.png', format='png')
    plt.clf()
    #plt.show()
        
    # plot_adjacent #
    plt.subplot(211)
    #f, (f1, f2) = plt.subplots(2, sharex = True, sharey = True)
    plt.bar(hist1.lbins, hist1.counts, width = w_adjacent, color='k')
    plt.legend(handles=[mpatches.Patch(color='b', label= label1)])
    #plt.title('Milkyway@home')
    plt.xlim((xlower, xupper))
    plt.ylim((0.0, ylimit))
    plt.ylabel('N')
    #plt.xlabel(r'$\Lambda$')
    
    plt.subplot(212)
    plt.bar(hist2.lbins, hist2.counts, width = w_adjacent, color='k')
    plt.legend(handles=[mpatches.Patch(color='k', label= label2)])
    #plt.title('')
    plt.xlim((xlower, xupper))
    plt.ylim((0.0, ylimit))
    plt.ylabel('N')
    plt.xlabel(r'$\Lambda$')
    #f.subplots_adjust(hspace=0)
    plt.savefig(save_folder_adj + name + '.png', format='png')
    plt.clf()
    #plt.show()
    return 1
# # 
def plot_veldisp(hist1, hist2, name, label1, label2):#plots the velocity dispersion from the histograms
    ylimit = 100
    xlower = 180 
    xupper = -180
    w_overlap = 2.5
    w_adjacent = 1.5
    folder = 'quick_plots/hists/'
    #folder = 'like_surface/'
    save_folder_ove = 'quick_plots/comp_hist_plots/overlap/'
    save_folder_adj = 'quick_plots/comp_hist_plots/adj/'
    #os.system("" + path + "scripts/plot_matching_hist.py " + hist1 + " " + hist2)
    print "plot histogram 1: ", hist1
    print "plot histogram 2: ", hist2
    plot_hist1 = hist1 + ".hist"
    plot_hist2 = hist2 + ".hist"

    print("plotting histograms\n")
    hist1 = nbody_histograms(folder + plot_hist1)
    hist2 = nbody_histograms(folder + plot_hist2)
            
    # plot overlapping #    
    #f, (f1, f2) = plt.subplots(2, sharex = True, sharey = True)
    #plt.subplot(211)
    plt.bar(hist1.lbins, hist1.vd, width = w_overlap, color='k', alpha=1,    label= label1)
    plt.bar(hist2.lbins, hist2.vd, width = w_overlap, color='r', alpha=0.75, label= label2)
    #plt.bar(hist1.lbins, hist1.count_err, width = w_overlap, color='black', alpha=0.75, label= label2)
    #plt.bar(hist2.lbins, hist2.count_err, width = w_overlap, color='b', alpha=0.75, label= label2)
    plt.title('Line of Sight Vel Disp Distribution')
    plt.xlim((xlower, xupper))
    plt.ylim((0.0, ylimit))
    plt.ylabel('vel disp')
    plt.legend()
    plt.savefig(save_folder_ove + name + '_overlapping.png', format='png')
    plt.clf()
    #plt.show()
        
    # plot_adjacent #
    plt.subplot(211)
    #f, (f1, f2) = plt.subplots(2, sharex = True, sharey = True)
    plt.bar(hist1.lbins, hist1.vd, width = w_adjacent, color='b')
    plt.legend(handles=[mpatches.Patch(color='b', label= plot_hist1)])
    plt.title('Line of Sight Vel Disp Distribution')
    plt.xlim((xlower, xupper))
    plt.ylim((0.0, ylimit))
    plt.ylabel('counts')
    plt.xlabel('Lambda')

    plt.subplot(212)
    plt.bar(hist2.lbins, hist2.vd, width = w_adjacent, color='k')
    plt.legend(handles=[mpatches.Patch(color='k', label= plot_hist2)])
    plt.xlim((xlower, xupper))
    plt.ylim((0.0, ylimit))
    plt.xlabel('l')
    plt.ylabel('vel disp')
    plt.xlabel('Lambda')
    #f.subplots_adjust(hspace=0)
    plt.savefig(save_folder_adj + name + '.png', format='png')
    plt.clf()
    #plt.show()
    return 1
# # 

def plot_single(hist1, name):
    ylimit = 0.6
    xlower = 100 
    xupper = -100
    w_adjacent = 4
    folder = 'quick_plots/hists/'
    save_folder = 'quick_plots/'
    print "plot histogram 1: ", hist1
    plot_hist1 = hist1 + ".hist"

    
    print("plotting histograms\n")
    hist1 = nbody_histograms(folder + plot_hist1)
            
    plt.bar(hist1.lbins, hist1.counts, width = w_adjacent, color='b')
    #plt.legend(handles=[mpatches.Patch(color='b', label= plot_hist1)])
    plt.title('MW@h Test Histogram')
    plt.xlim((xlower, xupper))
    plt.ylim((0.0, ylimit))
    plt.ylabel('N')
    plt.xlabel('Lambda')

    plt.savefig(save_folder + name + '.png', format='png')
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

def lambda_beta_plot(file_name):#plots the outputs in lambda beta. uses the nbody output class to convert lb to lambda beta
    path_charles = 'quick_plots/outputs/'
    path = 'quick_plots/'
    print file_name
    plot_lbr = y
    plot_light_and_dark = y
    plot_dm_alone = n
    
    out = nbody_outputs(path_charles + file_name + '.out')
    out.dark_light_split()
    out.convert_lambda_beta(True)
    
    fig = plt.figure()
    fig.subplots_adjust(hspace = 0.8, wspace = 0.8)
    # # # # # # # # # #
    if(plot_lbr):
        plt.figure(figsize=(10, 10))
        xlower = -180.0
        xupper = 180.0
        ylower = -80
        yupper = 80
        plt.xlim((xlower, xupper))
        plt.ylim((ylower, yupper))
        plt.xlabel(r'$\Lambda$')
        plt.ylabel(r'$\beta$')
        plt.title(r'$\Lambda$ vs $\beta$')
        #default to just plot lm
        plt.plot(out.light_lambda, out.light_beta, '.', markersize = .75, color = 'b', alpha=1.0, marker = '.',label = 'baryons')
        plt.legend()
        plt.savefig('/home/sidd/Desktop/research/quick_plots/' + file_name + '_lambdabeta_nodark', format='png')
        print "plotting:", len(out.light_l), " points"
        # # # # # # # # # #
        if(plot_light_and_dark):#plot lm and dm overlapping
            plt.xlim((xlower, xupper))
            plt.ylim((ylower, yupper))
            plt.xlabel(r'$\Lambda$')
            plt.ylabel(r'$\beta$')
            plt.title(r'$\Lambda$ vs $\beta$')
            plt.plot(out.dark_lambda, out.dark_beta, '.', markersize = .5, color = 'black', alpha=.75, marker = '.', label = 'dark matter')
            plt.legend()
            plt.savefig('/home/sidd/Desktop/research/quick_plots/' + file_name + '_lambdabeta', format='png')
            print "plotting:", len(out.light_l) + len(out.dark_l), " points"
        # # # # # # # # # #
        if(plot_dm_alone):#to plot just dm
            plt.clf()
            plt.figure(figsize=(20, 20))
            plt.xlim((xlower, xupper))
            plt.ylim((ylower, yupper))
            plt.xlabel(r'$\Lambda$')
            plt.ylabel(r'$\beta$')
            plt.title(r'$\Lambda$ vs $\beta$')
            plt.plot(out.dark_lambda, out.dark_beta, '.', markersize = 1, color = 'b', marker = '+')
            plt.legend()
            plt.savefig('/home/sidd/Desktop/research/quick_plots/tidal_stream_lambdabeta_dark', format='png')
            
    return 0 
 
def lb_plot(file_name): #plots lb from output
    path_charles = 'quick_plots/outputs/'
    path = 'quick_plots/'
    print file_name
    plot_lbr = y
    plot_light_and_dark = y
    plot_dm = n
    plot_xyz = n
    
    out = nbody_outputs(path_charles + file_name + '.out')
    out.rescale_l()
    out.dark_light_split()
    
    fig = plt.figure()
    fig.subplots_adjust(hspace = 0.8, wspace = 0.8)
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
        plt.savefig('/home/sidd/Desktop/research/quick_plots/' + file_name, format='png')
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
            plt.savefig('/home/sidd/Desktop/research/quick_plots/' + file_name, format='png')
            print "plotting:", len(out.light_l) + len(out.dark_l), " points"
        # # # # # # # # # #
        if(plot_dm):#to plot just dm
            plt.clf()
            plt.figure(figsize=(20, 20))
            plt.xlim((xlower, xupper))
            plt.ylim((ylower, yupper))
            plt.xlabel('l')
            plt.ylabel('b')
            plt.title('l vs b')
            plt.plot(out.dark_l, out.dark_b, '.', markersize = 1, color = 'b', marker = '+')
            plt.savefig('/home/sidd/Desktop/research/quick_plots/tidal_stream_lbr_dark', format='png')
            
    if(plot_xyz):
        xlower = 50
        xupper = -50
        fig.tight_layout()
        plt.axes().set_aspect('equal')
        plt.subplot(131, aspect='equal')
        plt.plot(out.light_x, out.light_y, '.', markersize = 1, color = 'r', marker = 'o')
        
        if(plot_light_and_dark == True):
            plt.plot(out.dark_x, out.dark_y, '.', markersize = 1, color = 'b', marker = '+')
        
        plt.xlim((xlower, xupper))
        plt.ylim((-80, 80))
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('x vs y')
        
        plt.subplot(132,aspect='equal')
        
        plt.plot(out.light_x, out.light_z, '.', markersize = 1, color = 'r', marker = 'o')
        
        if(plot_light_and_dark == True):
            plt.plot(out.dark_x, out.dark_z, '.', markersize = 1, color = 'b', marker = '+')
        
        plt.xlim((xlower, xupper))
        plt.ylim((-80, 80))
        plt.xlabel('x')
        plt.ylabel('z')
        plt.title('x vs z')
        
        plt.subplot(133, aspect='equal')
        
        plt.plot(out.light_z, out.light_y, '.', markersize = 1, color = 'r', marker = 'o')
        if(plot_light_and_dark == True):
            plt.plot(out.dark_z, out.dark_y, '.', markersize = 1, color = 'b', marker = '+')
        
        plt.xlim((xlower, xupper))
        plt.ylim((-80, 80))
        plt.xlabel('z')
        plt.ylabel('y')
        plt.title('z vs y')
        plt.savefig('/home/sidd/Desktop/research/quick_plots/tidal_stream_xyz', format='png')
    
    return 0


# # # # # # # # # # # # # # # # # # # # # #
#        Very Specific Plots              #
# # # # # # # # # # # # # # # # # # # # # #
# #


def plot_hist_lambda_beta(file1, file2, file_name = None):
    path = 'quick_plots/'
    hist = path + 'hists/'
    outs = path + 'outputs/'
    
    out1 = nbody_outputs(outs + file1 + ".out")
    out2 = nbody_outputs(outs + file2 + ".out")
    
    hist1 = nbody_histograms(hist + file1 + ".hist")
    hist2 = nbody_histograms(hist + file2 + ".hist")
    
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
        plt.plot(out1.dark_lambda, out1.dark_beta, '.', markersize = .5, color = 'black', alpha=.75, marker = '.', label = 'dark matter')
    plt.plot(out1.light_lambda, out1.light_beta, '.', markersize = .75, color = 'b', alpha=1.0, marker = '.', label = 'baryons')
    plt.legend()
    #plt.subplots(4, sharex = True, sharey = True)
    
    
    ax2 = plt.subplot(222)
    plt.xlim((xlower, xupper))
    plt.ylim((ylower, yupper))
    plt.xlabel(r'$\Lambda$')
    #plt.ylabel(r'$\beta$')
    plt.title(r'$\Lambda$ vs $\beta$')
    if(not file_name):
        plt.plot(out2.dark_lambda, out2.dark_beta, '.', markersize = .5, color = 'black', alpha=.75, marker = '.', label = 'dark matter')
    plt.plot(out2.light_lambda, out2.light_beta, '.', markersize = .75, color = 'b', alpha=1.0, marker = '.',label = 'baryons')
    
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
        plt.plot(out1.dark_lambda, out1.dark_beta, '.', markersize = .5, color = 'black', alpha=.75, marker = '.', label = 'dark matter')
    plt.plot(out1.light_lambda, out1.light_beta, '.', markersize = .75, color = 'b', alpha=1.0, marker = '.', label = 'baryons')
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
def plot_lmda_beta(file1, file2):
    path = 'quick_plots/'
    hist = path + 'hists/'
    outs = path + 'outputs/'
    
    out1 = nbody_outputs(outs + file1 + ".out")
    out2 = nbody_outputs(outs + file2 + ".out")
    
    hist1 = nbody_histograms(hist + file1 + ".hist")
    hist2 = nbody_histograms(hist + file2 + ".hist")
    
    w_overlap = 2.5
    w_adjacent = 1.5
    count_y_limit = 0.4
    out1.dark_light_split()
    out1.convert_lambda_beta(True)
    
    out2.dark_light_split()
    out2.convert_lambda_beta(True)
    
    xlower = -100.0
    xupper = 50.0
    ylower = -60
    yupper = 40
    
    plt.figure(figsize=(10, 5))
    plt.subplot(211)
    plt.xlim((xlower, xupper))
    plt.ylim((ylower, yupper))
    plt.ylabel(r'$\beta_{Orphan}$')
    plt.title(r'Simulated Stream and Best Fit Stream')
    plt.plot(out1.dark_lambda, out1.dark_beta, '.', markersize = .75, color = 'red', alpha=1, marker = '.', label = 'Simulated Dark Matter ')
    plt.plot(out1.light_lambda, out1.light_beta, '.', markersize = .75, color = 'b', alpha=0.75, marker = '.', label = 'Simulated Stars')
    plt.legend()
    #plt.subplots(4, sharex = True, sharey = True)
    
    
    ax2 = plt.subplot(212)
    plt.xlim((xlower, xupper))
    plt.ylim((ylower, yupper))
    plt.xlabel(r'$\Lambda_{Orphan}$')
    plt.ylabel(r'$\beta_{Orphan}$')
    #plt.title(r'$\Lambda$ vs $\beta$')
    plt.plot(out2.dark_lambda, out2.dark_beta, '.', markersize = .75, color = 'red', alpha=1, marker = '.', label = 'Best Fit  Dark Matter')
    plt.plot(out2.light_lambda, out2.light_beta, '.', markersize = .75, color = 'b', alpha=.75, marker = '.',label = 'Best Fit  Stars')
    plt.legend()
    plt.savefig('/home/sidd/Desktop/research/quick_plots/for_heidi/both_lambda_beta_init', format='png')
    #plt.show()
    
    
    plt.clf()
    plt.figure(figsize=(10, 5))
    plt.xlim((xlower, xupper))
    plt.ylim((ylower, yupper))
    plt.xlabel(r'$\Lambda_{Orphan}$')
    plt.ylabel(r'$\beta_{Orphan}$')
    plt.title(r'Simulated Orphan Stream')
    plt.plot(out1.dark_lambda, out1.dark_beta, '.', markersize = .75, color = 'red', alpha=1., marker = '.', label = 'Dark Matter')
    plt.plot(out1.light_lambda, out1.light_beta, '.', markersize = .75, color = 'b', alpha=.75, marker = '.', label = 'Stars')
    #plt.legend(handles=[mpatches.Patch(color='red', label= 'Dark Matter', color='b', label='Stars')])
    plt.legend()
    plt.savefig('/home/sidd/Desktop/research/quick_plots/for_heidi/mw_lambda_beta_init', format='png')
    
    
    plt.clf() 
    plt.figure(figsize=(10, 5))
    plt.xlim((xlower, xupper))
    plt.ylim((ylower, yupper))
    plt.xlabel(r'$\Lambda_{Orphan}$')
    plt.ylabel(r'$\beta_{Orphan}$')
    plt.title(r'MilkyWay@home Best Fit')
    plt.plot(out2.dark_lambda, out2.dark_beta, '.', markersize = .75, color = 'red', alpha=1, marker = '.', label = 'Dark Matter')
    plt.plot(out2.light_lambda, out2.light_beta, '.', markersize = .75, color = 'b', alpha=.75, marker = '.',label = 'Stars')
    plt.legend()
    plt.savefig('/home/sidd/Desktop/research/quick_plots/for_heidi/best_fit_lambda_beta_init', format='png')
    

def veldisp(file1):#plots the velocity dispersion from the histograms
    path = 'quick_plots/'
    hist = path + 'hists/'
    outs = path + 'outputs/'
    
    out1 = nbody_outputs(outs + file1 + ".out")
    hist1 = nbody_histograms(hist + file1 + ".hist")
    
    
    
    ylimit = 100
    xlower = 180 
    xupper = -100
    w_overlap = 2.5
    w_adjacent = 5
    folder = 'quick_plots/hists/'

    # to unnormalize counts. Make sure to change the number to the value from histogram
    #for i in range(0, len(hist1.counts)):
        #hist1.counts[i] *= 9217#mw hist
        #hist1.counts[i] *= 9211#best fit
        
            
    # plot_adjacent #
    plt.subplot(211)
    #f, (f1, f2) = plt.subplots(2, sharex = True, sharey = True)
    plt.bar(hist1.lbins, hist1.counts, width = w_adjacent, color='b')
    #plt.legend(handles=[mpatches.Patch(color='k', label= '')])
    plt.title('Best Fit Star Counts and Velocity Dispersion')
    plt.xlim((xlower, xupper))
    plt.ylim((0.0, 3000))
    plt.ylabel('N')
    #plt.xlabel(r'$\Lambda_{Orphan}$')

    plt.subplot(212)
    plt.bar(hist1.lbins, hist1.vd, width = w_adjacent, color='b')
    #plt.legend(handles=[mpatches.Patch(color='k', label= '')])
    plt.xlim((xlower, xupper))
    plt.ylim((0.0, 40))
    plt.ylabel(r'$\sigma$ (km/s)')
    plt.xlabel(r'$\Lambda_{Orphan}$')
    #f.subplots_adjust(hspace=0)
    #plt.savefig(path + 'for_heidi/vel_disp_hist_simulated' + '.png', format='png')
    plt.savefig(path + 'for_heidi/vel_disp_hist_best_fit' + '.png', format='png')
    plt.clf()
    #plt.show()



def veldisp_lbda_beta(file1):#plots the velocity dispersion from the histograms
    path = 'quick_plots/'
    hist = path + 'hists/'
    outs = path + 'outputs/'
    
    out1 = nbody_outputs(outs + file1 + ".out")
    hist1 = nbody_histograms(hist + file1 + ".hist")
    out1.dark_light_split()
    out1.convert_lambda_beta(True)
    
    ylimit = 100
    xlower = -180 
    xupper = 180
    ylower = -80
    yupper = 80
    w_overlap = 2.5
    w_adjacent = 5
    folder = 'quick_plots/hists/'

    # to unnormalize counts. Make sure to change the number to the value from histogram
    for i in range(0, len(hist1.counts)):
        hist1.counts[i] *= 9217
        
    plt.figure(figsize=(8, 5))
    plt.subplot(311)
    plt.xlim((xlower, xupper))
    plt.ylim((ylower, yupper))
    plt.ylabel(r'$\beta_{Orphan}$')
    plt.title(r'Simulated Stream and Best Fit Stream')
    plt.plot(out1.dark_lambda, out1.dark_beta, '.', markersize = .75, color = 'red', alpha=1, marker = '.', label = 'Dark Matter ')
    plt.plot(out1.light_lambda, out1.light_beta, '.', markersize = .75, color = 'b', alpha=0.75, marker = '.', label = 'Stars')
    plt.legend()
        
            
    # plot_adjacent #
    plt.subplot(312)
    #f, (f1, f2) = plt.subplots(2, sharex = True, sharey = True)
    plt.bar(hist1.lbins, hist1.counts, width = w_adjacent, color='b')
    #plt.legend(handles=[mpatches.Patch(color='k', label= '')])
    #plt.title('Simulated Star Counts and Velocity Dispersion')
    plt.xlim((xlower, xupper))
    #plt.ylim((0.0, 0.4))
    plt.ylabel('N')
    #plt.xlabel(r'$\Lambda_{Orphan}$')

    plt.subplot(313)
    plt.bar(hist1.lbins, hist1.vd, width = w_adjacent, color='b')
    #plt.legend(handles=[mpatches.Patch(color='k', label= '')])
    plt.xlim((xlower, xupper))
    plt.ylim((0.0, 40))
    plt.ylabel(r'$\sigma$ (km/s)')
    plt.xlabel(r'$\Lambda_{Orphan}$')
    #f.subplots_adjust(hspace=0)
    plt.savefig(path + 'for_heidi/vel_disp_hist_lmda_beta_unnormalized' + '.png', format='png')
    plt.clf()
    #plt.show()

def chi_sq_dist_plot():
    k = 50.0
    cf = (k / 2.0) - 1.0
    x = 0.1
    xs = []
    func1s = []
    func2s = []
    func3s = []
    while(1):
        func1 = cf * mt.log(x) - x / 2.0
        func2 = func1 - cf * (mt.log(2.0 * cf) - 1.0) 
        if(x < 2.0 * cf):
            func3 = 0.0
        else:
            func3 = func2
            
        xs.append(x)
        func1s.append(func1)
        func2s.append(func2)
        func3s.append(func3)
        if(x > 1000):
            break
        else:
            x += 0.1
    plt.ylim((-200, 100))
    plt.xlim((0, 400))
    plt.xlabel(r'N$_{\sigma}$$^{2}$')
    plt.ylabel('Probability')
    plt.plot(xs, func1s, color='k', linestyle = 'solid', alpha = 1, linewidth = 2)
    plt.plot(xs, func3s, color='r', linestyle = 'dotted', alpha = 1, linewidth = 4)
    plt.plot(xs, func2s, color='b', linestyle = 'dashed', alpha = .5, linewidth = 2)
    
    plt.savefig('/home/sidd/Desktop/research/quick_plots/chi_sq_func', format='png')
    #plt.show()
# #


def single_xyz(file_name):
    path = 'quick_plots/hists_outs/'
    print file_name
    plot_light_and_dark = True
    plot_dm = True
    
    out = nbody_outputs(path + file_name + '.out')
    out.rescale_l()
    out.dark_light_split()
    
    fig = plt.figure()
    fig.subplots_adjust(hspace = 0.8, wspace = 0.8)
    # # # # # # # # # #
            
    xlower = 50
    xupper = -50
    #fig.tight_layout()
    #plt.axes().set_aspect('equal')
    plt.figure(figsize=(10, 10))
    plt.subplot(131,aspect='equal')
    plt.plot(out.light_x, out.light_y, '.', markersize = 1, color = 'r', marker = 'o')
    
    if(plot_light_and_dark == True):
        plt.plot(out.dark_x, out.dark_y, '.', markersize = 1, color = 'b', marker = '+')
    
    plt.xlim((xlower, xupper))
    plt.ylim((-80, 80))
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('x vs y')
    
    plt.subplot(132,aspect='equal')
    
    plt.plot(out.light_x, out.light_z, '.', markersize = 1, color = 'r', marker = 'o')
    
    if(plot_light_and_dark == True):
        plt.plot(out.dark_x, out.dark_z, '.', markersize = 1, color = 'b', marker = '+')
    
    plt.xlim((xlower, xupper))
    plt.ylim((-80, 80))
    plt.xlabel('x')
    plt.ylabel('z')
    plt.title('x vs z')
    
    plt.subplot(133, aspect='equal')
    
    plt.plot(out.light_z, out.light_y, '.', markersize = 1, color = 'r', marker = 'o')
    if(plot_light_and_dark == True):
        plt.plot(out.dark_z, out.dark_y, '.', markersize = 1, color = 'b', marker = '+')
    
    plt.xlim((xlower, xupper))
    plt.ylim((-80, 80))
    plt.xlabel('z')
    plt.ylabel('y')
    plt.title('z vs y')
    plt.savefig('/home/sidd/Desktop/research/quick_plots/tidal_stream_xyz', format='png')

    return 0


def main():
    file1 = 'hist_v166_3p95_0p2_0p2_12_0p2__1_2_2018'
    file2 = 'hist_v166_3p95_0p2_0p2_12_0p2__1_2_2018'
    
    #plot_hist_lambda_beta(file1, file2)
    
    #plot_lmda_beta(file1, file2)
    #veldisp(file2)
    #veldisp_lbda_beta(file1)
    
    #chi_sq_dist_plot()
    hist1 = 'hist_v168_3p95_0p2_0p2_12_0p2__1_31_18_diffSeed'
    hist2 = 'mw@home_best_fit'
    name = 'mwh_hist'
    #plot_single(hist1, name)
    #plot(hist1, hist2, 'mw@home_best_fit', 'MilkyWay@home', 'Best Fit')
    #plot_hist_lambda_beta_single(hist2, True)
    
    file1 = "dist_test"
    #single_xyz(file1)
    
    return 0 

main()




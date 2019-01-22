#! /usr/bin/python
#/* Copyright (c) 2018 Siddhartha Shelton */
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Algorithm to take in stream data and create a milkyway@home compatible histogram  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import os
from subprocess import call

from bin_classes import *
from vel_disp import *
from beta_bins import *
from plot_functions import *

    
def main():
    use_vgsr = False
    use_custom_bins = False
    calc_beta_dispersions = False
    make_hist = False
    make_unnormalized_hist = False
    normalize_counts =  True
    
    plot_counts = True
    plot_normed_counts = False
    
    # name of the data files # 
    vgsr_file = "my16lambet2bg.specbhb.dist.lowmet.stream"
    on_field_counts_file = "l270soxlbfgcxNTbcorr.newon"
    off_field_counts_file = "l270soxlbfgcxNTbcorr.newoff"
    bin_data = "data_from_yanny.dat"#uncombined. bins arrangement from orphan paper
    bin_data = "custom_bins3.dat" #combined
    
    if(not use_custom_bins):
        bin_data = None
    
    On_field_data  = field(on_field_counts_file)
    Off_field_data = field(off_field_counts_file)
    
    data_correction(On_field_data)
    data_correction(Off_field_data)
    
    lamda_beta_plot(On_field_data, Off_field_data)
    write_lambda_beta(On_field_data)
    # initiaze bins parameters #
    
    hist_paramaters  = bin_parameters(bin_data)

    # bin the star counts #
    On_field_binned  = bin_counts(On_field_data,   hist_paramaters  )
    Off_field_binned = bin_counts(Off_field_data,  hist_paramaters )
    #print On_field_binned.binned_data.counts

    
    binned_difference = get_binned_difference(On_field_binned, Off_field_binned)
    #print binned_difference.binned_data.counts
    
    # clears the data lists, only need binned data #
    del On_field_data, Off_field_data

    # plot the binned counts #
    if(plot_counts):
        plot_binned_counts(On_field_binned, Off_field_binned, binned_difference, hist_paramaters)                                       
    
    # bin the beta counts #
    if(calc_beta_dispersions):
        betas = bin_betas(On_field_binned.beta_data.beta_coors, Off_field_binned.beta_data.beta_coors, hist_paramaters)
    
    # deletes the on and off field bin data. only need bin diff data # 
    del On_field_binned, Off_field_binned
    
    
    # normalize the binned counts #
    if(normalize_counts):
        binned_difference_normed = normalize(binned_difference.binned_data.counts, binned_difference.binned_data.err)
        #print binned_difference_normed.binned_data.counts, binned_difference_normed.binned_data.err
        
    if(plot_normed_counts):
        plot_simN_normed(binned_difference_normed, hist_paramaters)  
    
    # deletes binned diff. only need converted #
    del binned_difference
    
    
    # makes the actual mw@h histogram #
    if(use_vgsr and make_hist):
        vgsr_dat = vgsr_data(vgsr_file)
        # bin the vgsr los, and vel disp #
        vgsr_dat.bin_vgsr(hist_paramaters.bin_lowers, hist_paramaters.bin_uppers)#may not work correctly
    
        # plot the vgsr points #
        vgsr_dat.plot_vgsr()                                         
        vgsr_dat.clear('data lists')
        make_mw_hist(binned_difference_normed, hist_paramaters, vgsr_dat)
    elif(make_hist):
        make_mw_hist(binned_difference_normed, True, hist_paramaters)
    
    if(make_unnormalized_hist):
         make_mw_hist(binned_difference_normed, False,  hist_paramaters)
main()
    
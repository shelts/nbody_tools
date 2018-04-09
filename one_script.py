#! /usr/bin/python
#/* Copyright (c) 2016 Siddhartha Shelton */
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                #/# # # # # # # # # # # # # # # # #\#
                #    One script to rule them all.   #
                #    One script to call them        #
                #    One script to run them.        #
                #    And in the folder, bind them   #
                #\# # # # # # # # # # # # # # # # #/#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import os
import subprocess
import math as mt
import random
from nbody_functional import *
from nbody_useful_plots import *
random.seed(a = 12345678)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                #/# # # # # # # # # # # # # # \#
                #          Control Panel       #
                #\# # # # # # # # # # # # # # /#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
y = True
n = False
#    pathways  #
#I am tired of constantly adapting it for the servers
lmc_dir = '/home/shelts/research/'
sid_dir = '/home/sidd/Desktop/research/'
sgr_dir = '/Users/master/sidd_research/'
path = sid_dir

args_run = [3.95, 0.2, 0.2, 12, 0.2] 
args_run_comp = [3.9, 0.2, 0.2, 12, 0.2] 
#args_run_comp = [3.94243049428117, 0.204575760168173, 0.179013230102704, 12.0318620456042, 0.140573755762348]
# # # # # # # # # # # # # # # # # # # # # # # #
#              Standard Run switches          #
# # # # # # # # # # # # # # # # # # # # # # # #
run_nbody                 = y                 #
remake                    = n                 #
run_and_compare           = n                 #
match_histograms          = n                 #
run_from_checkpoint       = n                 #
# # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # #
#              Hist Plot Switches             #
# # # # # # # # # # # # # # # # # # # # # # # #
plot_hists                = n                 #
plot_veldisp_switch       = n                 #
vlos_plot_switch          = n                 #
# # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # #
#              Non-Hist Plot Switches         #
# # # # # # # # # # # # # # # # # # # # # # # #
lb_plot_switch            = n                 #
lambda_beta_plot_switch   = n                 #

plot_adjacent             = y                 #
plot_overlapping          = y                 #
# # # # # # # # # # # # # # # # # # # # # # # #


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                #/# # # # # # # # # # # # # # \#
                #          Names               #
                #\# # # # # # # # # # # # # # /#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#    Histogram names      #
histogram_v168 = 'hist_v168_3p95_0p2_0p2_12_0p2__1_31_18_diffSeed'


#    hist to match against for compare after run  #
correct_hist = 'hist_v168_3p95_0p2_0p2_12_0p2__1_31_18_diffSeed'
compare_hist = 'data_hist_spring_2018'



#    hist name for the nbody run: either set them manually or use from the list above #
folder = path + 'quick_plots/hists_outs/'
correctans_hist = folder + 'fun'
simulations_hist = folder + '3.9'

plot_name = compare_hist



#    run specfics   #
#version = '_1.68_x86_64-pc-linux-gnu__mt'
version  = ''
lua = path + 'lua/' + "full_control.lua"
#lua = "manual_body_input.lua"
#lua = path + 'lua/' + "halo_object_dev.lua"
#lua = path + 'lua/' + "EMD_v168.lua"


# # # # # # # # # # # # # # # # # # # # # #
#    standard nbody running functions     #
# # # # # # # # # # # # # # # # # # # # # #
def standard_run():
    nbody = nbody_running_env(lua, version, path)
    
    if(remake):
        nbody.build(False)#true for complete rebuild
        
    if(run_nbody):
        nbody.run(args_run, correctans_hist)
    
    if(run_and_compare):
        nbody.run(args_run_comp, simulations_hist, correctans_hist)
    
    if(match_histograms):
        nbody.match_hists(simulations_hist, correctans_hist)
        
    if(plot_hists):
        plot(correctans_hist , simulations_hist, plot_name, '1', '2')
        
    if(plot_veldisp_switch):
        plot_veldisp(correctans_hist , simulations_hist, plot_name + "_velDisp", '1', '2')
    
    
    if(vlos_plot_switch):
        vlos_plot(correctans_hist, simulations_hist)
        vlos_plot_single(correctans_hist)
    
    return 0
# #        

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #    
def main():
    standard_run()
    
    if(lb_plot_switch):
        lb_plot(correctans_hist)
    
    if(lambda_beta_plot_switch):
        lambda_beta_plot(correctans_hist)
    
    #nb = nbody_running_env(lua, version, path)
    dat = folder + 'data_hist_spring_2018'
    sim = folder + 'arg_3.95_0.2_0.2_12_0.2_correct'
    
    #nb.run(args_run, folder + 'test1', dat)
    #nb.run(args_run, folder + 'test2', sim)
    
    
        
# spark plug #
main()

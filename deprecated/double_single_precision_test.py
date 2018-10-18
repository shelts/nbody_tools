#! /usr/bin/python
#/* Copyright (c) 2016 Siddhartha Shelton */
from nbody_functional import *
#from nbody_useful_plots import *
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
args_run_comp = [3.95, 0.3, 0.2, 15, 0.2] 

#    Histogram names      #

folder = path + 'quick_plots/hists_outs/'


# optional run arguements #
manual_body_list = '' #"~/Desktop/research/nbody_tools/disk.out"
piping_file = None

version  = ''
lua = path + 'lua/' + "full_control.lua"


# # # # # # # # # # # # # # # # # # # # # #
#    standard nbody running env usage     #
# # # # # # # # # # # # # # # # # # # # # #
nbody = nbody_running_env(lua, version, path)
    
nbody.build(True)

correctans_hist = folder + 'test_correct_double'
simulations_hist = folder + 'test_compare_double'
nbody.run(args_run, correctans_hist, None, piping_file, manual_body_list)#normally used to create the correctans_hist
nbody.run(args_run_comp, simulations_hist, correctans_hist, piping_file, manual_body_list)
    
    
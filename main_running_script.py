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

running = [3.95, 0.2, 0.2, 12., 0.2] 
compare = [3.95, 0.2, 0.2, 12, 0.2] 


# # # # # # # # # # # # # # # # # # # # # # # #
#              Standard Run switches          #
# # # # # # # # # # # # # # # # # # # # # # # #
run_nbody                 = n                 #
remake                    = y                 #
full_remake               = n
run_and_compare           = n                 #
match_histograms          = y                 #
# # # # # # # # # # # # # # # # # # # # # # # #

#    Histogram names      #
histogram_v168 = 'hist_v168_3p95_0p2_0p2_12_0p2__1_31_18_diffSeed'

folder = path + 'quick_plots/hists_outs/'

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# correctans_hist: name for non comparing hist file or the sim data hist for the compare runs #
# simulations_hist: name for the comparison hist file for comparison runs                     #
correctans_hist  =  'hist_v170_3p95_0p2_0p2_12_0p2__7_17_18_diffSeed3'
simulations_hist = 'hist_v170_3p95_0p2_0p2_12_0p2__7_23_18_diffSeed'
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


compares = [compare]#doing it this way because I often want to do multiple arguements with a single comparison hist
sim_hists = [simulations_hist]
#compares  = [comp1, comp2, comp3]
#sim_hists = ['fit1', 'fit2', 'fit3']

# optional run arguements #
manual_body_list = '' #"~/Desktop/research/nbody_tools/disk.out"
piping_file = None

#    run specfics   #
#version = '_1.70_x86_64-pc-linux-gnu__mt'
version  = ''
lua = path + 'lua/' + "full_control.lua"
#lua = path + 'lua/' + "EMD_v170_vhalounits.lua"
#lua = path + 'lua/' + "EMD_v170.lua"


# # # # # # # # # # # # # # # # # # # # # #
#    standard nbody running env usage     #
# # # # # # # # # # # # # # # # # # # # # #
def standard_run(sim_args, sim_hist):
    nbody = nbody_running_env(lua, version, path)
    
    if(remake):
        if(full_remake):
            nbody.build(True)#true for complete rebuild
        else:
            nbody.build(False)

    if(run_nbody):
        nbody.run(sim_args, folder + correctans_hist, None, piping_file, manual_body_list)#normally used to create the correctans_hist
    
    if(run_and_compare):
        nbody.run(sim_args, sim_hist, folder + correctans_hist, piping_file, manual_body_list)
    
    if(match_histograms):
        nbody.match_hists(sim_hist, folder + correctans_hist)
    
    return 0

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #    

for i in range(len(compares)):
    standard_run(compares[i], folder + sim_hists[i])


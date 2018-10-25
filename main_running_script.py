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
compare = [3.95, 0.2, 0.2, 12., 0.2] 

compare1 = [4.08753706475328, 0.20861176280277, 0.235449047582905, 11.9003162573009, 0.269766858968207]
compare2 = [4.04829233251125, 0.202535436238761, 0.173454370530649, 11.9484601872371, 0.166652986169686]
compare3 = [3.98887482577406, 0.212173176887538, 0.219882548707629, 12.0152276604504, 0.23749775053657]


# # # # # # # # # # # # # # # # # # # # # # # #
#              Standard Run switches          #
# # # # # # # # # # # # # # # # # # # # # # # #
run_nbody                 = y                 #
remake                    = n                 #
full_remake               = n
run_and_compare           = n                 #
match_histograms          = n                 #
# # # # # # # # # # # # # # # # # # # # # # # #

#    Histogram names      #
histogram_v168 = 'hist_v168_3p95_0p2_0p2_12_0p2__1_31_18_diffSeed'

folder = path + 'quick_plots/hists_outs/'

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# correctans_hist: name for non comparing hist file or the sim data hist for the compare runs #
# simulations_hist: name for the comparison hist file for comparison runs                     #
correctans_hist  =  'hist_v172_3p95_0p2_0p2_12_0p2__9_24_18'
simulations_hist =  'hist_v172_3p95_0p2_0p2_12_0p2__9_24_18_diffSeed1'
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


compare_args = [compare]#doing it this way because I often want to do multiple arguements with a single comparison hist
sim_hists = [simulations_hist]

compare_args = [compare1, compare2, compare3]
sim_hists = ['fit1', 'fit2', 'fit3']

# optional run arguements #
manual_body_list = '' #"~/Desktop/research/nbody_tools/disk.out"
piping_file = None

#    run specfics   #
#version = '_1.70_x86_64-pc-linux-gnu__mt'
version  = ''
lua = path + 'lua/' + "full_control.lua"
#lua = path + 'lua/' + "EMD_v170_vhalounits.lua"
#lua = path + 'lua/' + "EMD_v172.lua"


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
        nbody.run(running, folder + correctans_hist, None, piping_file, manual_body_list)#normally used to create the correctans_hist
    
    if(run_and_compare):
        nbody.run(sim_args, sim_hist, folder + correctans_hist, piping_file, manual_body_list)
    
    if(match_histograms):
        nbody.match_hists(sim_hist, folder + correctans_hist)
    
    return 0

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #    

for i in range(len(compare_args)):
    standard_run(compare_args[i], folder + sim_hists[i])


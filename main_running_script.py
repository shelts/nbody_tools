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

args_run = [3.95, 0.006, 0.02, 0.027, 0.001] 
args_run_comp = [3.9, 0.2, 0.2, 12, 0.2] 
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
#              Plot Switches                  #
# # # # # # # # # # # # # # # # # # # # # # # #
plot_hists                = n                 #
lb_plot_switch            = n                 #
lambda_beta_plot_switch   = n                 #
# # # # # # # # # # # # # # # # # # # # # # # #

#    Histogram names      #
histogram_v168 = 'hist_v168_3p95_0p2_0p2_12_0p2__1_31_18_diffSeed'

folder = path + 'quick_plots/hists_outs/'

# name for non comparing hist file or the sim data hist for the compare runs #
correctans_hist = folder + 'ultrafaint'

# name for the comparison hist file for comparison runs #
simulations_hist = folder + '3.9'

plot_name = compare_hist

#    run specfics   #
#version = '_1.68_x86_64-pc-linux-gnu__mt'
version  = ''
lua = path + 'lua/' + "full_control.lua"
#lua = path + 'milkywayathome_client/nbody/sample_workunits/for_dev_manual_body.lua'
#lua = "manual_body_input.lua"
#lua = path + 'lua/' + "halo_object_dev.lua"
#lua = path + 'lua/' + "EMD_v168.lua"


# # # # # # # # # # # # # # # # # # # # # #
#    standard nbody running env usage     #
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
    
    return 0

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #    
standard_run()

if(lb_plot_switch):
    lb_plot(correctans_hist)

if(lambda_beta_plot_switch):
    lambda_beta_plot(correctans_hist)
    
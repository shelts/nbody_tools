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
full_remake               = n
run_and_compare           = n                 #
match_histograms          = n                 #
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

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# correctans_hist: name for non comparing hist file or the sim data hist for the compare runs #
# simulations_hist: name for the comparison hist file for comparison runs                     #
correctans_hist = folder + 'ultrafaint'
simulations_hist = folder + '3.9'
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# optional run arguements #
manual_body_list = None #"~/Desktop/research/nbody_tools/disk.out"
piping_file = None

#    run specfics   #
#version = '_1.68_x86_64-pc-linux-gnu__mt'
version  = ''
lua = path + 'lua/' + "full_control.lua"
#lua = path + 'lua/' + "EMD_v168.lua"


# # # # # # # # # # # # # # # # # # # # # #
#    standard nbody running env usage     #
# # # # # # # # # # # # # # # # # # # # # #
def standard_run():
    nbody = nbody_running_env(lua, version, path)
    
    if(remake):
        if(full_remake):
            nbody.build(True)#true for complete rebuild
        else:
            nbody.build(False)

    if(run_nbody):
        nbody.run(args_run, correctans_hist, None, piping_file, manual_body_list)#normally used to create the correctans_hist
    
    if(run_and_compare):
        nbody.run(args_run_comp, simulations_hist, correctans_hist, piping_file, manual_body_list)
    
    if(match_histograms):
        nbody.match_hists(simulations_hist, correctans_hist)
    
    return 0

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #    
standard_run()

if(plot_hists):
    plot(correctans_hist , simulations_hist, simulations_hist, '1', '2')

if(lb_plot_switch):
    lb_plot(correctans_hist)

if(lambda_beta_plot_switch):
    lambda_beta_plot(correctans_hist)
    
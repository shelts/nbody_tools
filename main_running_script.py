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

correct = [4, 0.2, 0.2, 12., 0.2] 
compare = [4, 0.2, 0.2, 12., 0.2] 

compare1 = [4.08753706475328, 0.20861176280277, 0.235449047582905, 11.9003162573009, 0.269766858968207]
compare2 = [4.04829233251125, 0.202535436238761, 0.173454370530649, 11.9484601872371, 0.166652986169686]
compare3 = [3.98887482577406, 0.212173176887538, 0.219882548707629, 12.0152276604504, 0.23749775053657]

compare1 = [5.33576774207282, 0.362931115969133, 0.366297555140227, 0.303243393002725, 0.501014110903782]
compare2 = [5.33577724052272, 0.388179685962787, 0.467409414668402, 0.300555761652065, 0.402103010713059]
compare3 = [4.65701582900497, 0.474930122569772, 0.205244143091193, 0.292069199893403, 0.0190570899930729]


correct = [4, 0.2, 0.5, 0.13357417952 , 0.01187679999]
correct = [4, 0.2, 0.2, 12., 0.2] 
compare = [4, 0.2, 0.2, 12., 0.2] 
# # # # # # # # # # # # # # # # # # # # # # # #
#              Standard Run switches          #
# # # # # # # # # # # # # # # # # # # # # # # #
run_nbody                 = n                 #
remake                    = n                 #
full_remake               = n                 #
run_and_compare           = n                 #
match_histograms          = y                 #
# # # # # # # # # # # # # # # # # # # # # # # #

#    Histogram names      #
folder = path + 'quick_plots/hists_outs/willet_paras/'

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# correctans_hist: name for non comparing hist file or the sim data hist for the compare runs #
# simulations_hist: name for the comparison hist file for comparison runs                     #
#correctans_hist  =  'hist_v172_3p95_0p2_0p2_12_0p2__11_7_18'
#correctans_hist  = 'hist_v172_3p95_0p2_0p2_12_0p2__9_24_18'
#correctans_hist  = 'data_hist_fall_2018'
correctans_hist = "data_hist_fall_2018_skipped_bins"
#correctans_hist = '4bt_3.95ft_withbestlikerange_test_copy'
simulations_hist = 'willet_parameters_1.4DataHistMassAsBaryonMass_RestAsDM_.2r_.8rr'
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


compare_args = [compare]#doing it this way because I often want to do multiple arguements with a single comparison hist
sim_hists = [simulations_hist]

#compare_args = [compare1, compare2, compare3]
#sim_hists = ['fit1_data', 'fit2_data', 'fit3_data']

# optional run arguements #
manual_body_list = '' #"~/Desktop/research/nbody_tools/disk.out"
piping_file = None

#    run specfics   #
#version = '_1.70_x86_64-pc-linux-gnu__mt'
version  = ''
lua = path + 'lua/' + "EMD_v172_data_neworbital.lua"
#lua = path + 'lua/' + "EMD_v172.lua"
#lua = path + 'lua/' + "full_control.lua"


# # # # # # # # # # # # # # # # # # # # # #
#    standard nbody running env usage     #
# # # # # # # # # # # # # # # # # # # # # #
nbody = nbody_running_env(lua, version, path)
    
if(remake):
    if(full_remake):
        nbody.build(True)#true for complete rebuild
    else:
        nbody.build(False)

if(run_nbody):
    nbody.run(correct, folder + correctans_hist, None, piping_file, manual_body_list)#normally used to create the correctans_hist

if(run_and_compare):
    for i in range(len(compare_args)):
        nbody.run(compare_args[i], folder + sim_hists[i], folder + correctans_hist, piping_file, manual_body_list)

if(match_histograms):
    nbody.match_hists(folder + simulations_hist, folder + correctans_hist)
    


#print convert_to_Lambda_Beta(250, 48.6, 22.6, False)

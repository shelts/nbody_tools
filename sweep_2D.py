#! /usr/bin/python
#/* Copyright (c) 2016 Siddhartha Shelton */
import os
from subprocess import call
import random
from nbody_functional import *
#random.seed(a = 12345678)#lmc
random.seed(a = 687651463)#teletraan
#--------------------------------------------------------------------------------------------------
#       PARAMETER LIBRARY       #
#--------------------------------------------------------------------------------------------------
lmc_dir = '/home/shelts/research/'
sid_dir = '/home/sidd/Desktop/research/'
sgr_dir = '/Users/master/sidd_research/'
path = sid_dir

folder        = path + "like_surface/2D_hists/"
binary        = path + "nbody_test/bin/milkyway_nbody"
lua           = path + "lua/full_control.lua"

args = [3.95, 0.2, 0.2, 12, 0.2]
#input_hist    = folder + "arg_" + str(args[0]) + "_" + str(args[1]) + "_" + str(args[2]) + "_" + str(args[3]) + "_" + str(args[4]) + "_correct"
input_hist    = folder + "hist_v170_3p95_0p2_0p2_12_0p2__7_23_18_diffSeed"
#input_hist    = folder + "data_hist_spring_2018"
parameters_names = ['ft', 'r', 'rr', 'm', 'mr']

#ranges  = [ [2.0, 6.0],  \
            #[0.05, 0.5],  \
            #[0.05, 0.5],  \
            #[1., 60.0,], \
            #[.01, .95,],   \
          #]   

ranges  = [ [2.0, 6.0],  \
            [0.05, 0.5],  \
            [0.5, 0.95],  \
            [1., 60.0,], \
            [.001, .01,],   \
          ]


search_N = [50, 50, 50, 50, 50]
y = True
n = False

#choose what to run
make_folders      = n
rebuild_binary    = n
make_correct_hist = n
random_iter       = y

run1_ft = n
run1_r  = n
run1_rr = y
run1_m  = n
run1_mr = n
which_sweeps1 = [run1_ft, run1_r, run1_rr, run1_m, run1_mr]

run2_ft = n
run2_r  = n
run2_rr = n
run2_m  = n
run2_mr = y
which_sweeps2 = [run2_ft, run2_r, run2_rr, run2_m, run2_mr]
#--------------------------------------------------------------------------------------------------

    
class sweep:
    def __init__(self, p1, p2, nbody):
        os.system("mkdir " + path + "like_surface/2D_hists/parameter_sweep")
        
        self.p1 = p1 #parameter index
        self.p2 = p2
        self.data_vals1 = []
        self.data_vals2 = []
        self.data_val_file = path + "like_surface/2D_hists/parameter_sweep" + "/" + parameters_names[self.p1] + "_" + parameters_names[self.p2] + "_vals.txt"
        
        self.get_data_vals()
        self.run_sweep(nbody)
        self.write_data_vals()
        
    def get_data_vals(self):
        self.data_vals1.append(args[self.p1]) #correct value
        self.data_vals2.append(args[self.p2])
        
        for i in range(0, search_N[self.p1] * search_N[self.p2]):
            val1 = random.uniform(0.0, 1.0) * (ranges[self.p1][1] - ranges[self.p1][0]) + ranges[self.p1][0]
            val2 = random.uniform(0.0, 1.0) * (ranges[self.p2][1] - ranges[self.p2][0]) + ranges[self.p2][0]
            self.data_vals1.append(val1)
            self.data_vals2.append(val2)
            
    def run_sweep(self, nbody):
        paras = list(args)
        for i in range(0, search_N[self.p1] * search_N[self.p2] + 1): #the number of runs stated aboce plus the initial correct value run
            paras[self.p1] = self.data_vals1[i]
            paras[self.p2] = self.data_vals2[i]
            
            output_hist = folder + parameters_names[self.p1] + "_" + parameters_names[self.p2] + "_hists/" + "arg_" + str(paras[0]) + "_" + str(paras[1]) + "_" + str(paras[2]) + "_" + str(paras[3]) + "_" + str(paras[4])
            pipe_name = folder + "parameter_sweep/" + parameters_names[self.p1] + "_" + parameters_names[self.p2] + ".txt"
            #nbody.run(paras, output_hist, input_hist, pipe_name)
    
    def write_data_vals(self):
        f = open(self.data_val_file, 'w')
        for i in range(0, len(self.data_vals1)):
            f.write("%0.15f\t%0.15f\n" % (self.data_vals1[i], self.data_vals2[i]))
        f.close()
        
def mk_dirs():
    os.chdir(path + "like_surface")
    os.system("mkdir 2D_hists")
    for i in range(0, len(which_sweeps1)):
        for j in range(0, len(which_sweeps2)):
            if(which_sweeps1[i] and which_sweeps2[j] and i != j):    
                os.system("mkdir 2D_hists/" + parameters_names[i] + "_" + parameters_names[j] + "_hists")
    
    return 0

def main():
    nbody = nbody_running_env(lua, '', path)
    
    if(make_folders):
        mk_dirs()
    
    if(rebuild_binary):
        nbody.build(False)
        
    if(make_correct_hist):
        nbody.run(args, input_hist)
    
    for i in range(0, len(which_sweeps1)):
        for j in range(0, len(which_sweeps2)):
            if(which_sweeps1[i] and which_sweeps2[j] and i != j):
                sweeper = sweep(i, j, nbody)
                del sweeper
            
            
    return 0
    
main()
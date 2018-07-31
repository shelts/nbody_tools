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
path = lmc_dir

folder        = path + "like_surface/hists/"
binary        = path + "nbody_test/bin/milkyway_nbody"
lua           = path + "lua/full_control.lua"

args = [3.95, 0.2, 0.2, 12, 0.2]
input_hist    = folder + "arg_" + str(args[0]) + "_" + str(args[1]) + "_" + str(args[2]) + "_" + str(args[3]) + "_" + str(args[4]) + "_correct"
parameters_names = ['ft', 'r', 'rr', 'm', 'mr']

ranges  = [ [2.0, 6.0],  \
            [0.05, 0.5],  \
            [0.05, 0.5],  \
            [1., 60.0,], \
            [.01, .95,],   \
          ]   
search_N = [5, 5, 5, 5, 5]
y = True
n = False

#choose what to run
make_folders      = y
rebuild_binary    = y
make_correct_hist = n
random_iter       = y

run_ft = n
run_r  = n
run_rr = y
run_m  = n
run_mr = y
which_sweeps1 = [run_ft, run_r, run_rr, run_m, run_mr]
which_sweeps2 = [run_ft, run_r, run_rr, run_m, run_mr]
#--------------------------------------------------------------------------------------------------

    
class sweep:
    def __init__(self, p1, p2, nbody):
        os.system("mkdir " + path + "like_surface/hists/parameter_sweep")
        
        self.p1 = p1 #parameter index
        self.p2 = p2
        self.data_vals1 = []
        self.data_vals2 = []
        self.data_val_file = path + "like_surface/hists/parameter_sweep" + "/" + parameters_names[self.p1] + "_" + parameters_names[self.p2] + "_vals.txt"
        
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
        for i in range(0, search_N[self.p1] * search_N[self.p2]):
            paras[self.p1] = self.data_vals1[i]
            paras[self.p2] = self.data_vals2[i]
            
            output_hist = folder + parameters_names[self.p1] + "_" + parameters_names[self.p2] + "_hists/" + "arg_" + str(paras[0]) + "_" + str(paras[1]) + "_" + str(paras[2]) + "_" + str(paras[3]) + "_" + str(paras[4])
            pipe_name = folder + "parameter_sweep/" + parameters_names[self.p1] + "_" + parameters_names[self.p2] + ".txt"
            nbody.run(paras, output_hist, input_hist, pipe_name)
    
    def write_data_vals(self):
        f = open(self.data_val_file, 'w')
        for i in range(0, len(self.data_vals)):
            f.write("%0.15f\t%0.15f\n" % (self.data_vals1[i], self.data_vals2[i]))
        f.close()
        
def mk_dirs():
    os.chdir(path + "like_surface")
    os.system("mkdir hists")
    for i in range(0, len(parameters_names)):
        os.system("mkdir hists/" + parameters_names[i] + "_hists")
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
            if(which_sweeps1[i] and which_sweeps2[j]):
                sweeper = sweep(i, j, nbody)
                del sweeper
            
            
    return 0
    
main()
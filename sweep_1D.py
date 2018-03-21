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
rebuild_binary    = n
make_correct_hist = y
random_iter       = y

run_ft = y
run_r  = n
run_rr = n
run_m  = n
run_mr = n
which_sweeps = [run_ft, run_r, run_rr, run_m, run_mr]
#--------------------------------------------------------------------------------------------------

    
class sweep:
    def __init__(self, parameter, nbody):
        os.system("mkdir " + folder + "parameter_sweep")
        
        self.parameter = parameter #parameter index
        self.data_vals = []
        self.data_val_file = folder + "parameter_sweep/" + parameters_names[self.parameter] + "_vals.txt"
        
        self.get_data_vals()
        self.run_sweep(nbody)
        self.write_data_vals()
        
    def get_data_vals(self):
        if(random_iter):
            self.data_vals.append(args[self.parameter]) #correct value
        else:
            val = ranges[self.parameter][0] # lower range
            dN = (ranges[self.parameter][1] - ranges[self.parameter][0]) / search_N[self.parameter]
            self.data_vals.append(val)
            
        for i in range(search_N[self.parameter]):
            if(random_iter):
                val = random.uniform(0.0, 1.0) * (ranges[self.parameter][1] - ranges[self.parameter][0]) + ranges[self.parameter][0]
            else:
                val += dN
            self.data_vals.append(val)

    def run_sweep(self, nbody):
        paras = list(args)
        for i in range(len(self.data_vals)):
            paras[self.parameter] = self.data_vals[i]
            output_hist = folder + parameters_names[self.parameter] + "_hists/" + "arg_" + str(paras[0]) + "_" + str(paras[1]) + "_" + str(paras[2]) + "_" + str(paras[3]) + "_" + str(paras[4])
            pipe_name = folder + "parameter_sweep/" + parameters_names[self.parameter] + ".txt"
            nbody.run(paras, output_hist, input_hist, pipe_name)
    
    def write_data_vals(self):
        f = open(self.data_val_file, 'w')
        for i in range(0, len(self.data_vals)):
            f.write("%0.15f\n" % self.data_vals[i])
        f.close()
        
def mk_dirs():
    os.system("mkdir " + folder)
    for i in range(len(parameters_names)):
        os.system("mkdir " + folder + parameters_names[i] + "_hists")
    return 0

def main():
    nbody = nbody_running_env(lua, '', path)
    
    if(make_folders):
        mk_dirs()
    
    if(rebuild_binary):
        nbody.build(False)
        
    if(make_correct_hist):
        nbody.run(args, input_hist)
    
    for i in range(len(which_sweeps)):
        if(which_sweeps[i]):
            sweeper = sweep(i, nbody)
            del sweeper
            
            
    return 0
    
main()
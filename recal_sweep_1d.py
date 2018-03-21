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

sweep_name = 'parameter_sweep_data_hist_spring_2018'
#sweep_name = 'parameter_sweep_beta_dispersions'
folder        = path + "like_surface/" + sweep_name + "/"
binary        = path + "nbody_test/bin/milkyway_nbody"
lua           = path + "lua/full_control.lua"

args = [3.95, 0.2, 0.2, 12, 0.2]
input_hist    = folder + "arg_" + str(args[0]) + "_" + str(args[1]) + "_" + str(args[2]) + "_" + str(args[3]) + "_" + str(args[4]) + "_correct"
parameters_names = ['ft', 'r', 'rr', 'm', 'mr']

y = True
n = False

#choose what to run
rebuild_binary    = n
make_correct_hist = n

run_ft = y
run_r  = y
run_rr = y
run_m  = y
run_mr = y
which_sweeps = [run_ft, run_r, run_rr, run_m, run_mr]
#--------------------------------------------------------------------------------------------------

    
class recalc_sweep:
    def __init__(self, parameter, nbody):
        
        self.parameter = parameter #parameter index
        self.data_vals = []
        self.data_val_file = folder + sweep_name + "/" + parameters_names[self.parameter] + "_vals.txt"
        os.system("cp " + self.data_val_file + " " + folder + "recalc_parameter_sweep/")
        
        self.read_data_vals()
        self.rematch(nbody)
        
    def read_data_vals(self):
        f = open(self.data_val_file, 'r')
        for line in f:
            self.data_vals.append(float(line))

    def rematch(self, nbody):
        paras = list(args)
        for i in range(len(self.data_vals)): # theres one more, because of the correct answer
            paras[self.parameter] = self.data_vals[i]
            output_hist = folder + parameters_names[self.parameter] + "_hists/" + "arg_" + str(paras[0]) + "_" + str(paras[1]) + "_" + str(paras[2]) + "_" + str(paras[3]) + "_" + str(paras[4])
            pipe_name = folder + "recalc_parameter_sweep/" + parameters_names[self.parameter] + ".txt"
            nbody.match_hists(output_hist, input_hist, pipe_name)
    

def main():
    os.system("mkdir " + folder + "recalc_parameter_sweep")
    nbody = nbody_running_env(lua, '', path)
    
    if(rebuild_binary):
        nbody.build(False)
        
    if(make_correct_hist):
        nbody.run(args, input_hist)
    
    for i in range(len(which_sweeps)):
        if(which_sweeps[i]):
            sweeper = recalc_sweep(i, nbody)
            del sweeper
            
            
    return 0
    
main()
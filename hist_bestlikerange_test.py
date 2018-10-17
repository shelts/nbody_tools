#! /usr/bin/python
#/* Copyright (c) 2016 Siddhartha Shelton */
from nbody_functional import *
import random
random.seed(a = 1466)#teletraan

lmc_dir = '/home/shelts/research/'
sid_dir = '/home/sidd/Desktop/research/'
sgr_dir = '/Users/master/sidd_research/'
path   = sid_dir
folder = path + "quick_plots/hists_outs/"

binary        = path + "nbody_test/bin/milkyway_nbody"
lua           = path + "lua/full_control.lua"

input_hist = folder + 'hist_v172_3p95_0p2_0p2_12_0p2__9_24_18'


ranges  = [ [2.0, 6.0],  \
            [0.05, 0.5],  \
            [0.1, 0.6],  \
            [.1, 100.0,], \
            [.001, .95,],   \
          ]   

class hist_test:
    def __init__(self):
        self.args = []
        self.N = 10
        
        
    def determine_parameters(self):
        arg_set = []
        
        for j in range(self.N):
            arg_set = []
            for i in range(len(ranges)):
                val = random.uniform(0.0, 1.0) * (ranges[i][1] - ranges[i][0]) + ranges[i][0]
                arg_set.append(val) #creating a parameter set
            print arg_set
            self.args.append(arg_set)

    def run_sims(self):
        nbody = nbody_running_env(lua, '', path)
        for i in range(len(self.args)):
            output_hist = path + "nbody_tools/tests/bestlike_hists/" + "arg" 
            for j in range(len(ranges)):
                output_hist += "_" + str(self.args[i][j])  
            pipe_name = path + "nbody_tools/tests/bestlike_hists/likes.txt"
            nbody.run(self.args[i], output_hist, input_hist, pipe_name) 
            self.get_percentage(output_hist)
            
    def get_percentage(self, output_hist):
        f = open(output_hist, 'r')
        g = open('nbody_tools/tests/bestlike_hists/times.txt', 'a')
        fts = []
        bts = []
        for line in f:
            if(line.startswith("# Evolve backward time = ")):
                bt = line.split('# Evolve backward time = ')
                bt = bt[1].split('\n') 
                bt = float(bt[0])
                
            if(line.startswith("# Evolve forward time = ")):
                ft = line.split('# Evolve forward time = ')
                ft = ft[1].split('\n') 
                ft = float(ft[0])
                break
        g.write("%0.15f\t%0.15f\n" % (bt, ft))
        f.close()
        g.close()
        
        
def main():
    tst = hist_test()
    tst.determine_parameters()
    tst.run_sims()
    

main()
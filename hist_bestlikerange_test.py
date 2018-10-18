#! /usr/bin/python
#/* Copyright (c) 2016 Siddhartha Shelton */
from nbody_functional import *
import matplotlib.pyplot as plt
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
        self.N = 100
        
        
    def determine_parameters(self):
        arg_set = []
        
        for j in range(self.N):
            arg_set = []
            for i in range(len(ranges)):
                val = random.uniform(0.0, 1.0) * (ranges[i][1] - ranges[i][0]) + ranges[i][0]
                arg_set.append(val) #creating a parameter set
            #print arg_set
            self.args.append(arg_set)

    def run_sims(self):
        nbody = nbody_running_env(lua, '', path)
        for i in range(len(self.args)):
            output_hist = path + "nbody_tools/tests/bestlike_hists/" + "arg" 
            for j in range(len(ranges)):
                output_hist += "_" + str(self.args[i][j])  
            pipe_name = path + "nbody_tools/tests/bestlike_hists/likes.txt"
            nbody.run(self.args[i], output_hist, input_hist, pipe_name) 
            
    def get_percentage(self):
        self.fts = []
        self.bts = []
        for i in range(len(self.args)):
            output_hist = path + "nbody_tools/tests/bestlike_hists/" + "arg" 
            for j in range(len(ranges)):
                output_hist += "_" + str(self.args[i][j])  
            output_hist += '.hist'
            #print output_hist
            f = open(output_hist, 'r')
            for line in f:
                if(line.startswith("# Evolve backward time = ")):
                    bt = line.split('# Evolve backward time = ')
                    bt = bt[1].split('\n') 
                    bt = float(bt[0])
                    self.bts.append(bt)
                    
                if(line.startswith("# Evolve forward time = ")):
                    ft = line.split('# Evolve forward time = ')
                    ft = ft[1].split('\n') 
                    ft = float(ft[0])
                    self.fts.append(ft)
                    break
            f.close()
        
    def read_likes(self):
        g = open(path + 'nbody_tools/tests/bestlike_hists/likes.txt', 'r')
        self.likes = []
        for line in g:
             if (line.startswith("<search_likelihood")):
                ss = line.split('<search_likelihood>')#splits the line between the two sides the delimiter
                ss = ss[1].split('</search_likelihood>')#chooses the second of the split parts and resplits
                ss = ss[0].split('\n') 
                self.likes.append(float(ss[0]))
                
    
    def write_out_times(self):
        g = open(path + 'nbody_tools/tests/bestlike_hists/times.txt', 'w')
        for i in range(len(self.fts)):
            g.write("%0.15f\t%0.15f\n" % (self.bts, self.fts))
        g.close()
        
        
    def calc_percs(self):
        self.perc = []
        
        for i in range(len(self.fts)):
            percent = self.fts[i]/self.bts[i]
            #print percent
            self.perc.append(percent)
    
    def plot(self):
        hst = binner([0.98, 1.], 100, self.perc)
        #plt.xlim((,)
        #plt.ylim((0.0, ))
        plt.ylabel('N')
        plt.xlabel('Best Likelihood Range')
        #print hst.bin_centers
        #print hst.counts
        plt.bar(hst.bin_centers, hst.counts, width = 0.001, color='k')
        plt.savefig('tests/likes_bestlike_range.png', format='png')
        
        
def main():
    tst = hist_test()
    
    tst.determine_parameters()
    #tst.run_sims()
    #tst.write_out_times()
    tst.get_percentage()
    tst.read_likes()
    tst.calc_percs()
    tst.plot()
    
main()
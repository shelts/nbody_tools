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
correct_hist_folder = path + "quick_plots/hists_outs/"

binary        = path + "nbody_test/bin/milkyway_nbody"
lua           = path + "lua/full_control.lua"

input_hist = correct_hist_folder + 'hist_v172_3p95_0p2_0p2_12_0p2__9_24_18'
hist_folder = 'tests/bestlike_hists/'
hist_time_ranges = ['90/', '95/', '98/']

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

    def run_sims(self, time_range):
        nbody = nbody_running_env(lua, '', path)
        for i in range(len(self.args)):
            output_hist = path + 'nbody_tools/' + hist_folder + hist_time_ranges[time_range] +  "arg" 
            for j in range(len(ranges)):
                output_hist += "_" + str(self.args[i][j])  
            pipe_name = path + 'nbody_tools/' + hist_folder + hist_time_ranges[time_range] + "likes.txt"
            nbody.run(self.args[i], output_hist, input_hist, pipe_name) 
            
    def read_likes(self):
        self.likes = []
        for i in range(len(hist_time_ranges)):
            likes = []
            g = open(hist_folder + hist_time_ranges[i] + "likes.txt", 'r')
            for line in g:
                if (line.startswith("<search_likelihood")):
                    ss = line.split('<search_likelihood>')#splits the line between the two sides the delimiter
                    ss = ss[1].split('</search_likelihood>')#chooses the second of the split parts and resplits
                    ss = ss[0].split('\n') 
                    likes.append(float(ss[0]))
            self.likes.append(likes)
        #print self.likes
            
    def get_percentage(self):
        self.fts = []
        self.bts = []
        self.perc = []
        hist_paths
        for i in range(len(hist_time_ranges)):
            self.perc.append([])
            hist_paths.append(hist_folder + hist_time_ranges[i] )
            
        for i in range(len(self.args)):
            output_hist = "arg" #forms histogram name
            for j in range(len(ranges)):
                output_hist += "_" + str(self.args[i][j])  
            output_hist += '.hist'
                
            #output_hists = []
            perc = []
            for j in range(len(hist_time_ranges)):#the different hist folders
                #output_hists.append( h )#list of the histogram name with the paths to the different folders
                h = hist_folder + hist_time_ranges[j] + output_hist 
                
                hist = nbody_histograms(h)
                percent = hist.perc
                self.perc[j].append(percent)#list of the percentages for each arg. each member a list of the percs from each folder
                
            #print self.likes[i]
            self.plot_all_hists(output_hists, self.likes[i])
       
    
    #def write_out_times(self):
        #g = open( hist_folder + "times.txt", 'w')
        #for i in range(len(self.fts)):
            #g.write("%0.15f\t%0.15f\n" % (self.bts, self.fts))
        #g.close()
        
        
    def plot(self):
        for i in range(len(hist_time_ranges)):
            hst = binner([0.90, 1.], 50, self.perc[i])
            plt.subplot(311 + i)
            #plt.xlim((,)
            plt.ylim((0.0, 60))
            plt.ylabel('N')
            plt.xlabel('Best Likelihood Range')
            #print hst.bin_centers
            #print hst.counts
            plt.bar(hst.bin_centers, hst.counts, width = 0.001, color='k')

        plt.savefig('tests/likes_bestlike_ranges.png', format='png', bbox_inches='tight')
        
   
   
    def plot_all_hists(self, hist_names, likes):
        correct_hist = nbody_histograms(correct_hist_folder + 'hist_v172_3p95_0p2_0p2_12_0p2__9_24_18.hist')
        #hist_folder1 = 'bestlike_hists_90'
        #hist_folder2 = 'bestlike_hists_95'
        #hist_folder3 = 'bestlike_hists_98'
        
        xlower = -150
        xupper = 150
        #for line in f:
        #hist_name = line.strip('\n')
        #hist1 = nbody_histograms('./tests/' + hist_folder1 + '/' + hist_name)
        #hist2 = nbody_histograms('./tests/' + hist_folder2 + '/' + hist_name)
        #hist3 = nbody_histograms('./tests/' + hist_folder3 + '/' + hist_name)
        
        f, (f1, f2) = plt.subplots(2, sharex = True, sharey = True, figsize=(20, 10))
        plt.subplot(411 )
        #print correct_hist.lbins
        plt.bar(correct_hist.lbins, correct_hist.counts, width = 2, color='k')
        #plt.ylim((0.0, ylimit))
        plt.xticks([])
        plt.ylabel('N')
        #plt.xlabel(r'$\Lambda$')
        
        for i in range(len(hist_time_ranges)):
            hist = nbody_histograms(hist_names[i])
            plt.subplot(412 + i)
            plt.bar(hist.lbins, hist.counts, width = 2, color='r', label = str(hist.perc))
            plt.legend()
            plt.xlim((xlower, xupper))
            plt.ylim((0.0, .1))
            plt.xticks([])
            plt.ylabel('N')
            plt.xlabel(r'$\Lambda$')
            plt.legend( loc='upper left', borderaxespad=0.,  prop={'size': 12}, framealpha=1)
            f.subplots_adjust(hspace=0)
            
        
            #plt.subplot(413)
            #plt.bar(hist2.lbins, hist2.counts, width = 2, color='r', label = str(hist2.perc))
            #plt.legend()
            #plt.xlim((xlower, xupper))
            #plt.ylim((0.0, .1))
            #plt.xticks([])
            #plt.ylabel('N')
            #plt.xlabel(r'$\Lambda$')
            #plt.legend( loc='upper left', borderaxespad=0.,  prop={'size': 12}, framealpha=1)
            #f.subplots_adjust(hspace=0)
            
            #plt.subplot(414)
            #plt.bar(hist3.lbins, hist3.counts, width = 2, color='r', label = str(hist3.perc))
            #plt.legend()
            #plt.xlim((xlower, xupper))
            #plt.ylim((0.0, .1))
            #plt.ylabel('N')
            #plt.legend( loc='upper left', borderaxespad=0.,  prop={'size': 12}, framealpha=1)
            #f.subplots_adjust(hspace=0)
        
        plt.xlabel(r'$\Lambda$')
        #plt.savefig('./tests/bestlike_hists_plots/' + hist_names.strip('.hist') + '.png', format='png', bbox_inches='tight')
        plt.savefig('./tests/bestlike_hists_plots/' + hist_names.strip('.hist') + '.png', format='png', bbox_inches='tight')
        plt.clf()
        plt.close()
            
           

def main():
    tst = hist_test()
    
    tst.determine_parameters()
    #tst.run_sims()
    tst.read_likes()
    tst.get_percentage()
    #tst.write_out_times()
    tst.plot()
    #tst.plot_all_hists()
    
main()
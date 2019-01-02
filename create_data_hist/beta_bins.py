#! /usr/bin/python
#/* Copyright (c) 2018 Siddhartha Shelton */
# # # # # # # # # # # # # # # # # # # # # # #
#   This File Works For create_data_hist.py #
# # # # # # # # # # # # # # # # # # # # # # #
import os
from mpl_toolkits.mplot3d import Axes3D
from subprocess import call
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from differential_evolution import *
from hessian import *
from bin_classes import *
#from hessian2 import *
#from nbody_functional import *
#from testing_hessian import parameter_sweeps
from plot_functions import *

class bin_betas:#class to make histogram of betas in each bin
    def __init__(self, beta_coors_ON, beta_coors_OFF, hist_paras):#(on field beta coordinates, Off field beta coordinates, lambda bin parameters)
        run_optimization = True
        plot_each_bin = False
        
        self.hist_paras = hist_paras
        del hist_paras
        
        self.beta_hist_init = beta_hist(self.hist_paras.Nbins)#get bin centers
        
        self.ON_field_bins  = self.beta_hist_init.initialize_beta_bins() # sets up the beta bins
        self.OFF_field_bins = self.beta_hist_init.initialize_beta_bins()
        self.combined_field = self.beta_hist_init.initialize_beta_bins()
        
        # binning the fields #
        self.beta_hist_init.bin_fields(beta_coors_ON, beta_coors_OFF, self.ON_field_bins, self.OFF_field_bins, self.combined_field)
        del beta_coors_ON, beta_coors_OFF # free up some space
        
        if(plot_each_bin):
            self.plot_each_bin()
            
        if(run_optimization):
            self.optimize()
        
        
    def optimize(self):
        iters = 500000
        file_name = None
        sigmas = []
        #os.system("rm -r stream_beta_plots/lamb*")
        r1 = [[-5,0.], [205,215], [55,70], [.25,.4], [1.0,1.5]]
        r2 = [[0,4], [285,300], [55,70], [-.4,-.2], [.55,.7]]
        r3 = [[1.,5], [255,270], [65,80], [.2,.35], [.7,.8]]
        r4 = [[-4.,2], [15,25], [50,65], [.25,.4], [1.0,1.5]]
        ranges = [r1, r2, r3, r4]
        
        for i in range(0, self.hist_paras.Nbins):#for each lambda bin
            file_name = "pop/saved_" + str(i) + '.pop'
            if file_name:
                iters = 1
            self.fit = diff_evo(self.beta_hist_init.bin_centers , self.combined_field[i], iters, file_name)
            
            #self.fit.pop.save_population("pop/saved_" + str(i) + '.pop')
            self.fit_paras = self.fit.pop.best_paras
            self.cost = self.fit.pop.best_cost
            print 'BIN: ', i
            print 'Paras: ', self.fit_paras
            
            
            self.errors1 = hessian(self.fit.cost, self.fit_paras, None) #initial errors
            
            for j in range(0, 10):#keep running until error is same as step sizes
                step_sizes = self.errors1.errs
                self.errors1 = hessian(self.fit.cost, self.fit_paras, self.errors1.errs)
                
                
            print 'UPDATED ERRORS: ', self.errors1.errs, '\n'
            sigmas.append(self.fit_paras[4])
            
            
            plot_each_bin(i, self.hist_paras, self.beta_hist_init, self.ON_field_bins, self.OFF_field_bins, self.combined_field) # plot each lambda bin seperately
            plot_fit_dots(i, self.hist_paras, self.beta_hist_init, self.ON_field_bins, self.OFF_field_bins, self.combined_field, self.fit_paras, self.fit, self.cost)
        #self.plot_sigma(sigmas, hist_paras)
        


    
    
    

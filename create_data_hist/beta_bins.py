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
#from hessian2 import *
#from nbody_functional import *
#from testing_hessian import parameter_sweeps
#from plot_functions import *

class bin_betas:#class to make histogram of betas in each bin
    def __init__(self, beta_coors_ON, beta_coors_OFF, lmda_bnd):#(on field beta coordinates, Off field beta coordinates, lambda bin parameters)
        run_optimization = True
        plot_each_bin = True
        den_correction = False
        
        self.binned_beta_ON  = []
        self.binned_beta_OFF = []
        self.binned_beta_combined = []
        self.lmda_bnd = lmda_bnd
        del lmda_bnd
        
        # bin the on and off field seperately so you can adjust it until they have same number of bins #
        # these parameters should be kept the same. But the option is there.
        self.beta_Nbins = 30
        self.lower = -4.0
        self.upper = 4.0
        
        self.bin_width    = abs(self.lower - self.upper) / self.beta_Nbins
        
        self.initialize_beta_bins(beta_coors_ON, beta_coors_OFF) # sets up the beta bins
        del beta_coors_ON, beta_coors_OFF # free up some space
        
        if(den_correction):
            self.off_field_star_density()
            self.den_correction()
        
        if(plot_each_bin):
            #self.plot_each_bin()
            self.plot_each_bin_adj()
            
        if(run_optimization):
            self.optimize()
        
        
    def initialize_beta_bins(self, beta_coors_ON, beta_coors_OFF):
        self.bin_centers = []
        
        # initialize the beta bin centers ON field #
        center = self.lower +  self.bin_width / 2.0
        for i in range(0, self.beta_Nbins): # initial beta bin centers On field
            self.bin_centers.append(center)
            center += self.bin_width
        
        # create array for storing beta count data #
        for i in range(0, self.lmda_bnd.Nbins):  
            self.binned_beta_ON.append([]) # empty vessel for each Lambda bin for the beta bins
            self.binned_beta_OFF.append([])
            self.binned_beta_combined.append([])
            
            # initialize the counts to zero in each bin ON field #
            for j in range(0, self.beta_Nbins): # for each beta bins
                self.binned_beta_ON[i].append(0.0) # initialize the counts for the beta bins
                self.binned_beta_OFF[i].append(0.0)
                self.binned_beta_combined[i].append(0.0)
            # send the beta coors for this lambda bin for binning #    
            self.binner(i, beta_coors_ON[i], beta_coors_OFF[i]) 

    
    def binner(self, lmbda_bin, coors_ON, coors_OFF): # (current lambda bin, beta coors on field, beta coors off field)
        for j in range(0, len(coors_ON)): # for each beta coordinate in the lmda bin
            for k in range(0, self.beta_Nbins): # for each beta bin
                lower_bound = (self.bin_centers[k] - self.bin_width / 2.0) # bin bounds
                upper_bound = (self.bin_centers[k] + self.bin_width / 2.0)
                
                if(coors_ON[j] >= lower_bound  and coors_ON[j] <= upper_bound): # check if beta coor is in the bin
                    self.binned_beta_ON[lmbda_bin][k] += 1.0
                    self.binned_beta_combined[lmbda_bin][k] += 1.0
        
        for j in range(0, len(coors_OFF)): # for each beta coordinate in the lmda bin
            for k in range(0, self.beta_Nbins): # for each beta bin
                lower_bound = (self.bin_centers[k] - self.bin_width / 2.0)
                upper_bound = (self.bin_centers[k] + self.bin_width / 2.0)
                if(coors_OFF[j] >= lower_bound  and coors_OFF[j] <= upper_bound):
                    self.binned_beta_OFF[lmbda_bin][k] += 1.0
                    self.binned_beta_combined[lmbda_bin][k] += 1.0
                #print lower_bound, upper_bound
    
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
        
        for i in range(0, self.lmda_bnd.Nbins):
            file_name = "pop/saved_" + str(i) + '.pop'
            if file_name:
                iters = 1
            self.fit = diff_evo(self.bin_centers , self.binned_beta_combined[i], iters, file_name)
            #self.fit.pop.save_population("pop/saved_" + str(i) + '.pop')
            self.fit_paras = self.fit.pop.best_paras
            self.cost = self.fit.pop.best_cost
            print 'BIN: ', i
            print 'Paras: ', self.fit_paras
            
            
            self.errors1 = hessian(self.fit.cost, self.fit_paras, None) #initial errors
            #errors2 = hessian2(self.fit.cost, self.fit_paras, None) #initial errors
            #print 'ERRORS: ' , errors1.errs, '\n'
            #print 'ERRORS: ' , errors2.errs, '\n'
            
            for j in range(0, 10):#keep running until error is same as step sizes
                step_sizes = self.errors1.errs
                self.errors1 = hessian(self.fit.cost, self.fit_paras, self.errors1.errs)
                
                #step_sizes2 = errors2.errs
                #errors2 = hessian2(self.fit.cost, self.fit_paras, errors2.errs)
                
            #print 'STEP SIZES: ', step_sizes
            print 'UPDATED ERRORS: ', self.errors1.errs, '\n'
            #print 'UPDATED ERRORS2: ', errors2.errs, '\n'
            sigmas.append(self.fit_paras[4])
            
            #errors2 = variable_error(self.fit, self.fit_paras, self.cost)
            #print 'ERRORS+: ', errors2.error1
            #print 'ERRORS-: ', errors2.error2
            
            #sweep = parameter_sweeps(self.fit, self.fit_paras, str(i), ranges[i])
            
            self.plot_each_bin(i) # plot each lambda bin seperately
            self.plot_fit_dots(i)
        self.plot_sigma(sigmas)
        
    def plot_each_bin(self, i = None):
        w = 0.25
        #test_dat = test_data()
        plt.figure()
        plt.xlim(self.lower - 2, self.upper + 2)
        plt.ylim(0.0, 400)
        plt.ylabel("counts")
        plt.xlabel(r"$\beta_{Orphan}$")
        
        # this is sloppy. but whatevs
        if(i != None):
            fit_paras = list(self.fit_paras)
            fit_xs, fit_fs = self.fit.cost.generate_plot_points(fit_paras)
            
            plt.plot(fit_xs,  fit_fs, color='k',linewidth = 2, alpha = 1., label = 'paras: m=' + str(round(fit_paras[0], 2)) + ' b=' + str(round(fit_paras[1], 2)) + ' A=' + str(round(fit_paras[2], 2)) + r" $x_{0}$=" + str(round(fit_paras[3], 2)) + r' $\sigma$=' + str(round(fit_paras[4], 2)) + ' L=' + str(self.cost) )
            plt.bar(self.bin_centers, self.binned_beta_combined[i], width=w, color='k', alpha = 1., label = 'C')
            plt.bar(self.bin_centers, self.binned_beta_OFF[i], width=w, color='r', alpha = 0.5, label = 'OFF')
            plt.bar(self.bin_centers, self.binned_beta_ON[i], width=w, color='b', alpha = 0.5, label = 'ON')
            
            plt.legend()
            plt.savefig('stream_beta_plots/lambda_bin_' + str(i) + '_(' + str(self.lmda_bnd.bin_lowers[i]) + ',' + str(self.lmda_bnd.bin_centers[i]) + ',' +  str(self.lmda_bnd.bin_uppers[i]) + ').png', format = 'png')
            plt.close()
        else:
            os.system("rm -r stream_beta_plots/lamb*")
            for i in range(0, self.lmda_bnd.Nbins):
                plt.figure()
                plt.xlim(self.lower - 2 , self.upper + 2)
                plt.ylim(0.0, 200)
                plt.ylabel("counts")
                plt.xlabel(r"$\beta_{Orphan}$")
                plt.bar(self.bin_centers, self.binned_beta_combined[i], width=w, color='k', alpha = 1., label = 'Combined')
                plt.bar(self.bin_centers, self.binned_beta_OFF[i], width=w, color='r', alpha = 0.5, label = 'OFF Field')
                plt.bar(self.bin_centers, self.binned_beta_ON[i], width=w, color='b', alpha = 0.5, label = 'ON Field')
                plt.legend()
                #plt.savefig('stream_beta_plots/lambda_bin_' + str(i) + '_(' + str(self.lmda_bnd.bin_lowers[i]) + ',' + str(self.lmda_bnd.bin_centers[i]) + ',' +  str(self.lmda_bnd.bin_uppers[i]) + ').png', format = 'png')
                plt.savefig('stream_beta_plots/lambda_bin_' + str(i) + '_' + str(self.lmda_bnd.bin_centers[i]) + '.png', format = 'png')
                plt.close()
        #plt.clf()
        
        return 0
    
    
    def plot_each_bin_adj(self):
        w = 0.25
        #test_dat = test_data()
        plt.xlim(self.lower - 2, self.upper + 2)
        plt.ylim(0.0, 400)
        plt.ylabel("counts")
        plt.xlabel(r"$\beta_{Orphan}$")
        plt.figure(figsize=(20, 60))
        fig, axes = plt.subplots(ncols=2, sharex=True, sharey=True)
        fig.subplots_adjust(hspace=0, wspace=0)
        for i in range(0, self.lmda_bnd.Nbins):
            #plt.ylabel("counts")
            
            plt.subplot(3, 8, i + 1)
            plt.xlim(self.lower - 0.5 , self.upper + 0.5)
            plt.ylim(0.0, 200)
            plt.yticks([])
            if(i == 0 or i == 8 or i == 16): #or i == 16 or i == 20):
                plt.yticks([50,100, 150])
            if(i == 8):
                plt.ylabel("N")
            if(i >= 16):
                plt.xticks([-2, 0, 2])
            if(i == 19):
                plt.xlabel(r"$\beta_{Orphan}$")
            plt.bar(self.bin_centers, self.binned_beta_combined[i], width=w, color='k', alpha = 1., label = 'Combined')
            plt.bar(self.bin_centers, self.binned_beta_OFF[i], width=w, color='r', alpha = 0.5, label = 'OFF Field')
            plt.bar(self.bin_centers, self.binned_beta_ON[i], width=w, color='b', alpha = 0.5, label = 'ON Field')
            #plt.legend()
            
        plt.savefig('stream_beta_plots/lambda_bin_combined.png', format = 'png', dpi=300)
        plt.close()

    def plot_fit_dots(self, i):
        plt.figure()
        plt.xlim(self.lower - 2, self.upper + 2)
        
        # this is sloppy. but whatevs
        fit_paras = list(self.fit_paras)
        fit_xs, fit_fs = self.fit.cost.generate_plot_points(fit_paras)
        w = 0.25
        
        #fit_paras1 = list(self.fit_paras)
        #fit_paras2 = list(self.fit_paras)
        #for j in range(4,5):
            #fit_paras1[j] += self.errors1.errs[j]
            #fit_paras2[j] -= self.errors1.errs[j]
            
        
        #fit_xs2, fit_fs2 = self.fit.cost.generate_plot_points(fit_paras1)
        #fit_xs3, fit_fs3 = self.fit.cost.generate_plot_points(fit_paras2)
        lb = 'paras: m=' + str(round(fit_paras[0], 2)) + ' b=' + str(round(fit_paras[1], 2)) + ' A=' + str(round(fit_paras[2], 2)) + r" $x_{0}$=" + str(round(fit_paras[3], 2)) + r' $\sigma$=' + str(round(fit_paras[4], 2)) + ' L=' + str(self.cost)
        #plt.plot(fit_xs2,  fit_fs2, color='r',linewidth = 2, alpha = 1., label = '+')
        #plt.plot(fit_xs3,  fit_fs3, color='blue',linewidth = 2, alpha = 1., label = '-')
        #f, ((ax1, ax2)) = plt.subplots(2, sharex='col', sharey='row')
      
        fig, axes = plt.subplots(ncols=2, sharex=True, sharey=True)
        fig.subplots_adjust(hspace=0)
        ax1 = plt.subplot(211)
        plt.ylabel("Star Count", fontsize=16)
        plt.xlim(self.lower - 0.5 , self.upper + 0.5)
        plt.ylim(0.0, 400)
        plt.plot(fit_xs,  fit_fs, color='k',linewidth = 2, alpha = 1., label = '' )
        plt.plot(self.bin_centers, self.binned_beta_combined[i], '.', markersize=4.5, markerfacecolor='white', markeredgecolor='k', alpha = 0.9, marker = 'o', markeredgewidth=1,label = 'C')
        #plt.plot(self.bin_centers, self.binned_beta_OFF[i]     , 'o', markersize=2.5, color='r', alpha = 0.8, marker = 'o', label = 'OFF')
        #plt.plot(self.bin_centers, self.binned_beta_ON[i]      , 'o', markersize=2.5,  color='b', alpha = 0.8, marker = 'o', label = 'ON')
        plt.xticks([])
        plt.yticks([50, 100, 150, 200, 250, 300, 350, 400])
        
        ax2 = plt.subplot(212)
        plt.ylabel("Star Count", fontsize=16)
        plt.xlabel(r"$\beta_{Orphan}$", fontsize=16)
        plt.xlim(self.lower - 0.5 , self.upper + 0.5)
        plt.ylim(0.0, 400)
        plt.bar(self.bin_centers, self.binned_beta_combined[i], width=w, color='w', edgecolor = "k", hatch='xxxxx', alpha = 1., label = 'Combined')
        plt.bar(self.bin_centers, self.binned_beta_OFF[i],      width=w, color='w', edgecolor = "firebrick", hatch='\\\\\\\\', alpha = 1., label = 'OFF')
        plt.bar(self.bin_centers, self.binned_beta_ON[i],       width=w, color='w', edgecolor = "b", hatch='////', alpha = 1., label = 'ON')
        plt.yticks([50, 100, 150,  200, 250, 300, 350])
        #plt.legend()
        if(i== 0 ):
            plt.legend(bbox_to_anchor=(0.65,0.7), loc='lower left', borderaxespad=0.,  prop={'size': 14}, framealpha=1)
        elif(i == 1 ):
            plt.legend(bbox_to_anchor=(0.65,0.87), loc='lower left', borderaxespad=0.,  prop={'size': 14}, framealpha=1)
        elif(i == 2 ):
            plt.legend(bbox_to_anchor=(0.65,0.87), loc='lower left', borderaxespad=0.,  prop={'size': 14}, framealpha=1)
        elif(i == 3 ):
            plt.legend(bbox_to_anchor=(0.65,0.4), loc='lower left', borderaxespad=0.,  prop={'size': 14}, framealpha=1)
            
        plt.savefig('stream_beta_plots/lambda_dots_' + str(i) + '_(' + str(self.lmda_bnd.bin_lowers[i]) + ',' + str(self.lmda_bnd.bin_centers[i]) + ',' +  str(self.lmda_bnd.bin_uppers[i]) + ').png', format = 'png')
        plt.savefig('stream_beta_plots/dots/lambda_dots_' + str(i) + '.pdf', format = 'pdf')
        plt.savefig('stream_beta_plots/dots/lambda_dots_' + str(i) + '.png', format = 'png')
        plt.close()
    
    
    def plot_sigma(self, sigmas):
        plt.title(r'$\sigma$ vs $\Lambda_{Orphan}$')
        plt.xlabel(r'$\Lambda_{Orphan}$')
        plt.ylabel(r'$\sigma$')
        plt.ylim(0, 1.5)
        plt.scatter(self.lmda_bnd.bin_centers, sigmas, marker='o')
        plt.savefig('plots/sigma_v_lambda.png', format='png')
    
    
    

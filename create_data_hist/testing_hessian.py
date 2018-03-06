#! /usr/bin/python
#/* Copyright (c) 2018 Siddhartha Shelton */
# # # # # # # # # # # # # # # # # # # # # # #
#   Something to run front end to test      #
#    implementation of hessian              #
# # # # # # # # # # # # # # # # # # # # # # #
import matplotlib.pyplot as plt
import sys
from test_data import *
from differential_evolution import *
from hessian import *

def plot(test, fit):
    w = 0.25
    plt.figure()
    #plt.xlim(self.lower, self.upper)
    plt.ylim(0, 100)
    plt.ylabel("counts")
    plt.xlabel(r"$\beta_{Orphan}$")
    
    fit_paras = fit.pop.best_paras
    fit_xs, fit_fs = fit.cost.generate_plot_points(fit_paras)
    plt.plot(fit_xs,  fit_fs, color='k',linewidth = 2, alpha = 1., label = 'paras: m=' + str(round(fit_paras[0], 2)) + ' b=' + str(round(fit_paras[1], 2)) + ' A=' + str(round(fit_paras[2], 2)) + r" $x_{0}$=" + str(round(fit_paras[3], 2)) + r' $\sigma$=' + str(round(fit_paras[4], 2)) + ' L=' + str(fit.pop.best_cost) )
    plt.scatter(test.xs, test.fsn, s = 8, color = 'b', marker='o')
    plt.legend()
    plt.savefig('plots/testing_hessian_fit.png', format = 'png')
    plt.close()


class parameter_sweeps:
    class points:
        def __init__(self):
            self.para = []
            self.cost = []
            self.dim = 0.0
        
    def __init__(self, fit, correct):
        self.best = fit.pop.best_paras
        self.correct = correct
        self.dim = len(self.best)
        self.sweep = []
        
        
        for i in range(0, self.dim):
            #print self.correct
            p = self.points()
            self.sweep.append(p)
            self.run_sweep(i, fit)
            
        self.plot_sweep()
        
    def run_sweep(self, i, fit):
        upper = fit.ranges[i].upper
        lower = fit.ranges[i].lower
        N = 20000
        dn = (upper - lower) / float(N)
        
        val = lower
        parameters = list(self.correct)
        #print self.correct
        while(val < upper):
            #print parameters, self.correct

            self.sweep[i].para.append(val)
            parameters[i] = val
            cost = fit.cost.get_cost(parameters)
            self.sweep[i].cost.append(cost)
            val += dn
        self.sweep[i].dim = N
        return 0
    
    def plot_sweep(self):
        plot_coor = 231
        names = ['Linear slope', 'Y-intercept', 'Guassian Amplitude', 'Guassian Center', r'$\sigma$']
        labels = ['m', 'b', 'A', r'$\mu$',  r'$\sigma$']
        plt.figure(figsize=(20, 10))
        for i in range(0, self.dim):
            tmp = []
            fitted_para = []
            correct_para = []
            correct_cost = []
            N = 1000
            plt.subplot(plot_coor + i)
            if(i == 0):
                #plt.ylim(-400.0,0.0)
                plt.ylim(-10, 0.0)
                plt.xlim(-10, 10)
            elif(i == 1):
                #plt.ylim(-175.0, 0.0)
                plt.ylim(-5.0, 0.0)
                plt.xlim(20, 40)
            elif(i == 2):
                #plt.ylim(-175.0, 0.0)
                plt.ylim(-5.0, 0.0)
                plt.xlim(40, 60)
            elif(i == 3):
                #plt.ylim(-10.0,0.0)
                plt.ylim(-.6,0.0)
                plt.xlim(-0.25, 0.1)
            elif(i == 4):
                #plt.ylim(-10.0,0.0)
                plt.ylim(-.75,0.0)
                plt.xlim(1.35, 1.55)
                
            for j in range(0, N):
                tmp.append(- float(j))
                fitted_para.append(self.best[i])
                correct_para.append(self.correct[i])
            plt.title(names[i])
            plt.xlabel(labels[i])
            plt.ylabel('cost')
            plt.scatter(self.sweep[i].para, self.sweep[i].cost,color='k', s=.5, marker= 'o' )
            plt.plot(fitted_para, tmp,color='b' )
            plt.plot(correct_para, tmp,color='r' )

        plt.savefig('plots/parameter_sweeps_peak.png', format='png')
        
        
def main(file_name = None):
    test = test_data() #creating fittable data

    if(file_name):
        print 'optimizing from file'
        fit = diff_evo(test.xs, test.fsn, 10, file_name)
    else:
        print 'optimizing...'
        fit = diff_evo(test.xs, test.fsn, 50000, file_name)
        fit.pop.save_population('optimized_test_data.pop')
        
    
    plot(test, fit)
    
    fit_parameters = fit.pop.best_paras
    print 'best fit parameters: '
    print fit_parameters
    
    print '\ncalculating errors...'
    errors = hessian(fit.cost, fit_parameters)
    print 'done\n'
    
    print 'running parameter sweeps...'
    para_sweeps = parameter_sweeps(fit, test.correct)
    print 'done\n'
    
args = sys.argv;
file_name = None
if(len(args) > 1):
    file_name = args[1]
main(file_name)



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
from hessian2 import *
def plot(test, fit, name):
    w = 0.25
    plt.figure()
    #plt.xlim(self.lower, self.upper)
    plt.ylim(0, 400)
    plt.ylabel("counts")
    plt.xlabel(r"$\beta_{Orphan}$")
    
    fit_paras = fit.pop.best_paras
    fit_xs, fit_fs = fit.cost.generate_plot_points(fit_paras)
    plt.plot(fit_xs,  fit_fs, color='k',linewidth = 2, alpha = 1., label = 'paras: m=' + str(round(fit_paras[0], 2)) + ' b=' + str(round(fit_paras[1], 2)) + ' A=' + str(round(fit_paras[2], 2)) + r" $x_{0}$=" + str(round(fit_paras[3], 2)) + r' $\sigma$=' + str(round(fit_paras[4], 2)) + ' L=' + str(fit.pop.best_cost) )
    plt.scatter(test.xs, test.fsn, s = 8, color = 'b', marker='o')
    plt.legend()
    plt.savefig('plots/testing_hessian_fit_' + name + '.png', format = 'png')
    plt.close()


class parameter_sweeps:
    class points:
        def __init__(self):
            self.para = []
            self.cost = []
            self.dim = 0.0
        
    def __init__(self, fit, correct, name, ranges):
        self.best = fit.pop.best_paras
        self.correct = correct
        self.dim = len(self.best)
        self.sweep = []
        
        
        
        self.run_sweep(fit)
        self.plot_sweep(name, ranges)
        
    def run_sweep(self, fit):
        for i in range(0, self.dim):
            p = self.points()
            self.sweep.append(p)
            upper = fit.ranges[i].upper
            lower = fit.ranges[i].lower
            N = 20000
            dn = (upper - lower) / float(N)
            
            val = lower
            parameters = list(self.correct)
            
            while(val < upper):
                self.sweep[i].para.append(val)
                parameters[i] = val
                cost = fit.cost.get_cost(parameters)
                self.sweep[i].cost.append(cost)
                val += dn
            self.sweep[i].dim = N
            
        return 0
        
    

    def plot_sweep(self, name, ranges):
        plot_coor = 231
        names = ['Linear slope', 'Y-intercept', 'Guassian Amplitude', 'Guassian Center', r'$\sigma$']
        labels = ['m', 'b', 'A', r'$\mu$',  r'$\sigma$']
        plt.figure(figsize=(20, 10))

        for i in range(0, self.dim):
            tmp = []
            fitted_para = []
            correct_para = []
            correct_cost = []
            N = 10000
            plt.subplot(plot_coor + i)
            if(i == 0):
                plt.ylim(-400.0,0.0)
                #plt.ylim(-10, 0.0)
                #plt.xlim(ranges[i][0], ranges[i][1])
            elif(i == 1):
                plt.ylim(-175.0, 0.0)
                #plt.ylim(-5.0, 0.0)
                #plt.xlim(ranges[i][0], ranges[i][1])
            elif(i == 2):
                plt.ylim(-175.0, 0.0)
                #plt.ylim(-5.0, 0.0)
                #plt.xlim(ranges[i][0], ranges[i][1])
            elif(i == 3):
                plt.ylim(-10.0,0.0)
                #plt.ylim(-.6,0.0)
                #plt.xlim(ranges[i][0], ranges[i][1])
            elif(i == 4):
                plt.ylim(-10.0,0.0)
                #plt.ylim(-.75,0.0)
                #plt.xlim(ranges[i][0], ranges[i][1])
                
            for j in range(0, N):
                tmp.append(- float(j))
                fitted_para.append(self.best[i])
                correct_para.append(self.correct[i])
            plt.title(names[i])
            plt.xlabel(labels[i])
            plt.ylabel('cost')
            plt.scatter(self.sweep[i].para, self.sweep[i].cost,color='k', s=.5, marker= 'o' )
            plt.plot(fitted_para, tmp,color='b', label='fitted' )
            plt.plot(correct_para, tmp,color='r' , label='correct')
            plt.legend()
        plt.savefig('plots/parameter_sweeps_data' + name + '.png', format='png')
        plt.clf()
        
        
#def main(file_name = None):
    #paras = []
    #p1 = [-1.75, 207., 61., 0.34, 1.07]
    #r1 = [[-5,0.], [205,215], [55,70], [.25,.4], [1.0,1.5]]
    #s1 = [10,10,18,.12,.12]
    
    #p2 = [1.6, 291., 66., -0.36, 0.64]
    #r2 = [[0,4], [285,300], [55,70], [-.4,-.2], [.55,.7]]
    #s2 = [8,10,16,.15,.12]
    
    #p3 = [3.75, 262., 74., 0.26, .74]
    #r3 = [[1.,5], [255,270], [65,80], [.2,.35], [.7,.8]]
    #s3 = [5,10,16,.08, .06]
    
    #p4 = [-.33, 20., 55., 0.3, 1.3]
    #r4 = [[-4.,2], [15,25], [50,65], [.25,.4], [1.0,1.5]]
    #s4 = [5,8,10,.08,.2]
    
    #paras  = [p1, p2, p3, p4]
    #ranges = [r1, r2, r3, r4]
    #steps  = [s1, s2, s3, s4]
    #for i in range(0, len(paras)):
        #test = test_data(paras[i], [-4,4]) #creating fittable data
        
        #if(file_name):
            #print 'optimizing from file'
            #fit = diff_evo(test.xs, test.fsn, 10, file_name + str(i) + '.pop')
        #else:
            #print 'optimizing...'
            #fit = diff_evo(test.xs, test.fsn, 500000, file_name)
            #fit.pop.save_population('pop/optimized_test_data' + str(i) + '.pop')
        
        
        #print 'plotting...'
        #plot(test, fit, str(i))
        #print 'done'
    
        #print 'best fit parameters: '
        #print fit.pop.best_paras
        
        #print '\ncalculating errors...'
        ##errors = hessian(fit.cost, fit.pop.best_paras, steps[i])
        ##print str(i), ' ERROR: ', errors.errs
        #print 'done\n'
        
        
        #print 'running parameter sweeps...'
        #para_sweeps = parameter_sweeps(fit, test.correct, str(i), ranges[i])
        
        #print 'done\n'
        #del test, fit, para_sweeps
        
#args = sys.argv;
#file_name = None
#if(len(args) > 1):
    #file_name = args[1]
##main(file_name)

#def main():
    #h = hessian2(None, None, None)
    
#main()

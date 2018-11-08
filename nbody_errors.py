#! /usr/bin/python
#/* Copyright (c) 2018 Siddhartha Shelton */
from nbody_functional import *
import numpy as np
from numpy.linalg import inv
import math as mt
lmc_dir = '/home/shelts/research/'
sid_dir = '/home/sidd/Desktop/research/'
sgr_dir = '/Users/master/sidd_research/'
path = sid_dir

class hessian:
    def __init__(self, cost, parameters, step_sizes = None):#(link to cost function, best fit parameters, optimizing step sizes)
        self.cost = cost
        self.paras = parameters
        self.steps = step_sizes #
        self.dim = len(self.paras)
        self.create_matrix()
        self.invert()
        
    def create_matrix(self):
        self.H = []
        print 'creating matrix'
        for i in range(0, self.dim):
            self.H.append([])
            for j in range(0, self.dim):
                print 'working on element', i, j
                derivative = self.calc_derivative_genstencil(i, j)
                self.H[i].append(derivative)
            #print self.H[i]
       
       

    
    
    def calc_derivative_genstencil(self, i, j):#stencil order depends on the steps and coeff arrays
        n = len(self.paras)
        if(self.steps):#optimizing step sizes or fix step size
            h1 = self.steps[i]
            h2 = self.steps[j]
        else:
            h1 = 0.05
            h2 = h1
        
        a = self.paras[i]
        b = self.paras[j]
        p = list(self.paras)#copies the list of parameters
        f = open(self.cost.likelihood_file, 'a')
        f.write('working on element ' + str(i) + ',' + str(j) + '\n')
        f.write('starting parameters:  ' + str(p[0]) + ' ' + str(p[1]) + ' ' + str(p[2]) + ' ' + str(p[3]) + ' ' + str(p[4]) + '\n')
        
        if(i == j): # straight up second derivative
            #asteps = [-3., -2., -1., 0., 1., 2., 3.]
            #coeffs = [2., -27., 270., -490., 270., -27., 2.]
            #div = 180. * h1 * h1
            
            asteps = [-1., 1., 0]#the h steps
            coeffs = [1., 1., -2.]#the coeffs when added together
            div =  h1 * h1 
            
            fs = []
            for k in range(len(asteps)):
                p[i] = a + asteps[k] * h1
                f.write('derivative parameters:  ' + str(p[0]) + ' ' + str(p[1]) + ' ' + str(p[2]) + ' ' + str(p[3]) + ' ' + str(p[4]) + '\n')
                fs.append(self.cost.get_likelihood(p))
                
                
            der = coeffs[0] * fs[0]
            for k in range(1, len(fs)):
                der += coeffs[k] * fs[k]
                
            der *= 1. / div
            f.write('derivative: %f\n' % (der))
            del fs, asteps, coeffs
            
            
        else: # second partial derivative
            #this is sloppy
            #asteps = [ 1. , 2., -2, -1., -1., -2., 1., 2.,  2., -2., -2., 2., -1., 1.,  1., -1.]
            #bsteps = [-2., -1.,  1., 2., -2., -1., 2., 1., -2.,  2., -2., 2., -1., 1., -1.,  1.]
            #coeffs = [-63., -63., -63., -63., 63., 63., 63., 63., 44., 44., -44., -44., 74., 74., -74., -74.]
            #div = (600. * h1 * h2)
            
            asteps = [1., 1., -1., -1.]
            bsteps = [1., -1., 1., -1.]
            coeffs = [1., -1., -1., 1.]
            div =  4.* h1 * h2
            
            
            fs = []
            for k in range(len(asteps)):
                p[i] = a + asteps[k] * h1
                p[j] = b + bsteps[k] * h2
                f.write('derivative parameters:  ' + str(p[0]) + ' ' + str(p[1]) + ' ' + str(p[2]) + ' ' + str(p[3]) + ' ' + str(p[4]) + '\n')
                fs.append(self.cost.get_likelihood(p))
            
            der = coeffs[0] * fs[0]
            for k in range(1, len(fs)):
                der += coeffs[k] * fs[k]
                
            der *= 1. / div
            f.write('derivative: %f\n' % (der))
            del fs, asteps, bsteps, coeffs
            
        f.close()
        return der
    
    
    def invert(self):
        self.errs = []
        array = []
        for i in range(0, self.dim):
            array.append(self.H[i])
        H = np.array(array)
        print H
        H_inv = inv(H)
        print H_inv
        f = open(self.cost.likelihood_file, 'a')
        for i in range(0, self.dim):
            errs = ( abs(H_inv[i][i]))**0.5
            self.errs.append(errs)
        f.write('ERRORS: ' + str(self.errs[0]) + ' ' + str(self.errs[1]) + ' ' + str(self.errs[2]) + ' ' + str(self.errs[3]) + ' ' + str(self.errs[4]) + '\n')
        print errs
        f.close()
          
class nbody_cost:
    def __init__(self, piping_file, lua, hist_name):
        self.likelihood_file = piping_file
        self.lua = lua
        self.correct_hist = hist_name
        
        
        
    def get_likelihood(self, parameters):
        nbody = nbody_running_env(self.lua, '', path)
        simulations_hist = 'test_' + str(parameters[0]) + '_' + str(parameters[1]) + '_' + str(parameters[2]) + '_' + str(parameters[3]) + '_' + str(parameters[4])
        nbody.run(parameters, simulations_hist, self.correct_hist, self.likelihood_file)
        #nbody.run(parameters, simulations_hist, self.correct_hist, None)
        likelihood = self.parse_likelihood()
        return likelihood
        
        
    def parse_likelihood(self):
        l = open(self.likelihood_file, 'r')
        
        for line in l:
            if(line.startswith("<search_likelihood")):
                ss = line.split('<search_likelihood>')#splits the line between the two sides the delimiter
                ss = ss[1].split('</search_likelihood>')#chooses the second of the split parts and resplits
                ss = ss[0].split('\n') 
                like = float(ss[0]) #keep rewriting it to get the last one in file
        
        l.close()
        print 'returning like: ', like
        return like
        
        
        
def main():
    create_best_fit_hist = True
    
    lua = path + 'lua/' + "full_control.lua"
    lua = path + 'lua/' + "EMD_v172.lua"
    piping_file = 'hessian_run_likelihoods.txt'
    hist_name = 'mw_best_fit'
    fit_parameters1 = [4.08753706475328, 0.20861176280277, 0.235449047582905, 11.9003162573009, 0.269766858968207]#best fit parameters from mw@h 1
    fit_parameters2 = [4.04829233251125, 0.202535436238761, 0.173454370530649, 11.9484601872371, 0.166652986169686]
    fit_parameters3 = [3.98887482577406, 0.212173176887538, 0.219882548707629, 12.0152276604504, 0.23749775053657]
    
    fit_parameters = [fit_parameters1, fit_parameters2, fit_parameters3]
    hist_names = ['mw_best_fit1', 'mw_best_fit2', 'mw_best_fit3']
    piping_files = ['hessian_run_likelihoods1.txt', 'hessian_run_likelihoods2.txt','hessian_run_likelihoods3.txt']
    
    for name in range(len(hist_names)):
        if(create_best_fit_hist):
            nb = nbody_running_env(lua, '', path)
            nb.run(fit_parameters[name], hist_names[name])
        
        
        #initialize the cost function
        nb_cost = nbody_cost(piping_files[name], lua, hist_names[name])
        errs = [mt.sqrt(abs(2.74946424e-07)), mt.sqrt(abs(-9.82330531e-08)), mt.sqrt(abs(-5.67039708e-08)), mt.sqrt(abs(2.27250996e-07)), mt.sqrt(abs(-3.20844368e-08)) ]
        errs = None
        
        hess = hessian(nb_cost, fit_parameters[name], errs) #get initial errors
        del nb_cost
    #i = 0
    #f = open(piping_file, 'a')
    #while(1):#iterate errors until errors equal step size
        #hess = hessian(nb_cost, fit_parameters, hess.errs)
        #print i
        #i += 1
        
    
main()
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
                derivative = self.calc_derivative(i, j)
                self.H[i].append(derivative)
            #print self.H[i]
       
       
    def calc_derivative(self, i, j):
        n = len(self.paras)
        if(self.steps):#optimizing step sizes or fix step size
            h1 = self.steps[i]
            h2 = self.steps[j]
        else:
            h1 = 0.001
            h2 = h1
        
        a = self.paras[i]
        b = self.paras[j]
        p = list(self.paras)
        f = open(self.cost.likelihood_file, 'a')
        f.write('working on element ' + str(i) + ',' + str(j) + '\n')
        f.write('starting parameters:  ' + str(p[0]) + ' ' + str(p[1]) + ' ' + str(p[2]) + ' ' + str(p[3]) + ' ' + str(p[4]) + '\n')
        if(i == j): # straight up second derivative
            f.write('derivative parameters:  ' + str(p[0]) + ' ' + str(p[1]) + ' ' + str(p[2]) + ' ' + str(p[3]) + ' ' + str(p[4]) + '\n')
            f1 = self.cost.get_likelihood(p)
            
            p[i] = a + h1
            f.write('derivative parameters:  ' + str(p[0]) + ' ' + str(p[1]) + ' ' + str(p[2]) + ' ' + str(p[3]) + ' ' + str(p[4]) + '\n')
            f2 = self.cost.get_likelihood(p)
            
            p[i] = a - h1
            f.write('derivative parameters:  ' + str(p[0]) + ' ' + str(p[1]) + ' ' + str(p[2]) + ' ' + str(p[3]) + ' ' + str(p[4]) + '\n')
            f3 = self.cost.get_likelihood(p)
            
            der = ((f2)) - 2.0 * ((f1)) + ((f3))
            f.write('derivative: %f\n' % (der))
            der = der / (h1 * h1)
            
        else: # second partial derivative
            p[i] = a + h1
            p[j] = b + h2
            f.write('derivative parameters:  ' + str(p[0]) + ' ' + str(p[1]) + ' ' + str(p[2]) + ' ' + str(p[3]) + ' ' + str(p[4]) + '\n')
            f1 = self.cost.get_likelihood(p)
        
            p[i] = a + h1
            p[j] = b - h2
            f.write('derivative parameters:  ' + str(p[0]) + ' ' + str(p[1]) + ' ' + str(p[2]) + ' ' + str(p[3]) + ' ' + str(p[4]) + '\n')
            f2 = self.cost.get_likelihood(p)
            
            p[i] = a - h1
            p[j] = b + h2
            f.write('derivative parameters:  ' + str(p[0]) + ' ' + str(p[1]) + ' ' + str(p[2]) + ' ' + str(p[3]) + ' ' + str(p[4]) + '\n')
            f3 = self.cost.get_likelihood(p)
            
            p[i] = a - h1
            p[j] = b - h2
            f.write('derivative parameters:  ' + str(p[0]) + ' ' + str(p[1]) + ' ' + str(p[2]) + ' ' + str(p[3]) + ' ' + str(p[4]) + '\n')
            f4 = self.cost.get_likelihood(p)
            
            der = ((f1)) - ((f2)) - ((f3)) + ((f4))
            f.write('derivative: %f\n' % (der))
            der = der / (4.0 * h1 * h2)
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
    piping_file = 'hessian_run_likelihoods.txt'
    hist_name = 'mw_best_fit'
    fit_parameters = [4.03545444101925, 0.102054233253449, 0.415975899916935, 1.12339623813343, 0.0101505240447525]#best fit parameters from mw@h
    
    if(create_best_fit_hist):
        nb = nbody_running_env(lua, '', path)
        nb.run(fit_parameters, hist_name)
    
    
    #initialize the cost function
    nb_cost = nbody_cost(piping_file, lua, hist_name)
    errs = [mt.sqrt(abs(2.74946424e-07)), mt.sqrt(abs(-9.82330531e-08)), mt.sqrt(abs(-5.67039708e-08)), mt.sqrt(abs(2.27250996e-07)), mt.sqrt(abs(-3.20844368e-08)) ]
    hess = hessian(nb_cost, fit_parameters, errs) #get initial errors
    
    i = 0
    #f = open(piping_file, 'a')
    while(1):#iterate errors until errors equal step size
        hess = hessian(nb_cost, fit_parameters, hess.errs)
        print i
        i += 1
        
    
main()
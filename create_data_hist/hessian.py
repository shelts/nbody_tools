#! /usr/bin/python
#/* Copyright (c) 2018 Siddhartha Shelton */
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Hessian matrix implementation for calculating error in fits             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import numpy as np
from numpy.linalg import inv
import math as mt

def function(p):
    x = p[0]
    y = p[1]
    z = p[2]
    
    f = x * y * z + x**2 * y * z + x * y**2 * z + x * y * z**2
    return f

class hessian:
    def __init__(self, cost, parameters, step_sizes):
        self.cost = cost
        self.paras = parameters
        self.steps = step_sizes # by eye
        #self.paras = [2.0, 3.0, 4.0]
        self.dim = len(self.paras)
        self.create_matrix()
        self.invert()
    def create_matrix(self):
        self.H = []
        for i in range(0, self.dim):
            self.H.append([])
            for j in range(0, self.dim):
                derivative = self.calc_derivative(i, j)
                self.H[i].append(derivative)
            #print self.H[i]
       
       
    def calc_derivative(self, i, j):
        n = len(self.paras)
        h1 = self.steps[i]
        h2 = self.steps[j]
        
        #h1 = 0.1
        #print h1
        h2 = h1
        
        a = self.paras[i]
        b = self.paras[j]
        p = list(self.paras)
        #print p
        if(i == j): # straight up second derivative
            #f1 = function(p)
            f1 = self.cost.get_cost(p)
            
            p[i] = a + h1
            #f2 = function(p)
            f2 = self.cost.get_cost(p)
            
            p[i] = a - h1
            #f3 = function(p)
            f3 = self.cost.get_cost(p)
            
            # calculate in log space
            #der = mt.log(abs(f2)) - 2.0 * mt.log(abs(f1)) + mt.log(abs(f3))
            der = ((f2)) - 2.0 * ((f1)) + ((f3))
            der = der / (h1 * h1)
            
        else: # second partial derivative
            p[i] = a + h1
            p[j] = b + h2
            #f1 = function(p)
            f1 = self.cost.get_cost(p)
        
            p[i] = a + h1
            p[j] = b - h2
            #f2 = function(p)
            #print p, i, j
            f2 = self.cost.get_cost(p)
            
            p[i] = a - h1
            p[j] = b + h2
            #f3 = function(p)
            f3 = self.cost.get_cost(p)
            
            p[i] = a - h1
            p[j] = b - h2
            #f4 = function(p)
            f4 = self.cost.get_cost(p)
            
            # calculate in log space
            #der = mt.log(abs(f1)) - mt.log(abs(f2)) - mt.log(abs(f3)) + mt.log(abs(f4))
            der = ((f1)) - ((f2)) - ((f3)) + ((f4))
            
            der = der / (4.0 * h1 * h2)
        
        return der
        
    def invert(self):
        self.errs = []
        array = []
        for i in range(0, self.dim):
            array.append(self.H[i])
        H = np.array(array)
        H_inv = inv(H)
        for i in range(0, self.dim):
            errs = ( abs(H_inv[i][i]))**0.5
            self.errs.append(errs)
            
            
            
class variable_error:
    def __init__(self, fit, best_fit, best_cost):
        self.best = best_fit
        self.best_cost = best_cost
        self.errors(fit)
        
    def errors(self, fit):
        paras = list(self.best)
        dn = 0.001
        self.error1 = []
        self.error2 = []
        for i in range(0, len(self.best)):
            paras = list(self.best)
            while(1):
                paras[i] += dn
                cost = fit.cost.get_cost(paras)
                if(abs(self.best_cost - cost) >= 1.):
                    self.error1.append(abs(paras[i] - self.best[i]))
                    #diff1.append(abs(cost_best - cost))
                    break
            paras = list(self.best)
            while(1):
                paras[i] -= dn
                cost = fit.cost.get_cost(paras)
                if(abs(self.best_cost - cost) >= 1):
                    self.error2.append(abs(paras[i] - self.best[i]))
                    #diff2.append(abs(cost_best - cost))
                    break
        
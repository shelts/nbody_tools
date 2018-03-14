#! /usr/bin/python
#/* Copyright (c) 2018 Siddhartha Shelton */
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Hessian matrix implementation for calculating error in fits             #
# this one is modelled after how Newby did it.                            #
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

class hessian2:
    def __init__(self, cost, parameters, step_sizes = None):
        self.cost = cost
        self.paras = parameters
        self.steps = step_sizes #
        #self.paras = [2.0, 3.0, 4.0]
        self.dim = len(self.paras)
        self.create_matrix()
        self.invert()
    def create_matrix(self):
        self.H = []
        #print 'hessian2', '\n'
        for i in range(0, self.dim):
            self.H.append([])
            for j in range(0, self.dim):
                derivative = self.calc_derivative(i, j)
                self.H[i].append(derivative)
            #print self.H[i]
        #print  '\n'
       
    def calc_derivative(self, i, j):
        n = len(self.paras)
        if(self.steps):
            h1 = self.steps[i]
            h2 = self.steps[j]
        else:
            h1 = 0.001
            h2 = h1
        
        p = list(self.paras)
        
        p[i] += h1
        p[j] += h2
        #f1 = function(p)
        f1 = self.cost.get_cost(p)
        
        p = list(self.paras)
        p[i] += h1
        p[j] += -h2
        #f2 = function(p)
        f2 = self.cost.get_cost(p)
        
        p = list(self.paras)
        p[i] += -h1
        p[j] += h2
        #f3 = function(p)
        f3 = self.cost.get_cost(p)
        
        p = list(self.paras)
        p[i] += -h1
        p[j] += -h2
        #f4 = function(p)
        f4 = self.cost.get_cost(p)
        
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
            
            
            

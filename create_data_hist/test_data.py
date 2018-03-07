#! /usr/bin/python
#/* Copyright (c) 2018 Siddhartha Shelton */
# # # # # # # # # # # # # # # # # # # # # # #
#   This File Works For create_data_hist.py #
# # # # # # # # # # # # # # # # # # # # # # #
import math as mt
import random
import matplotlib.pyplot as plt

random.seed(a = 12345678)

# class to create a test data set. Currently uses a linear + guassian model, with guassian noise
class test_data: # class to create a test data set with guassian noise
    def __init__(self, parameters, data_ranges):
        self.N = 30 # number of points to generate
        self.data_range = data_ranges #[-4.0,4.0] # range for generating the points
        
        self.m   = parameters[0] #0.0 # slope for the linear background
        self.b   = parameters[1] #25.0 # y-intercept for the 
        
        self.A   = parameters[2] #50.0 # amplitude
        self.mu  = parameters[3]#0 # x-axis offset for the guassian
        self.sig = parameters[4] #1.5 #mt.sqrt(0.5) # 0.7 dispersion
        self.correct = [self.m, self.b, self.A, self.mu, self.sig]
        
        self.generate_points()
        
    def func(self, x): # function used for fitting
        linear = self.m * x + self.b
        guass = self.A * mt.exp( - (x - self.mu)**2.0 / (2.0 * self.sig**2.0))
        return linear + guass
    
    def generate_points(self):# generating the points from the function
        self.fs = []
        self.xs = []
        x = self.data_range[0]
        dn = abs(self.data_range[0] - self.data_range[1]) / float(self.N)
        for i in range(0, self.N):
            f = self.func(x)
            self.xs.append(x)
            self.fs.append(f)
            x += dn
        
        self.guass_noise()
        
    def guass_noise(self): #used to add guassian noise to the data points
        a = 2.0
        mu = 1.0
        sig = 2.0
        self.fsn = []
        for i in range(0, self.N):
            self.fsn.append(self.fs[i])
            x = random.uniform(-2, 2)
            noise = a * mt.exp( -(x - mu)**2.0 / (2.0 * sig**2.0))
            if(x > 0.0):
                self.fsn[i] += noise
            else:
                self.fsn[i] -= noise
        
    def plot(self): # plot the points with noise
        plt.ylim(0, 100)
        plt.xlim(-6, 6)
        plt.plot(self.xs, self.fs, linewidth = 2, color = 'r')
        plt.scatter(self.xs, self.fsn, s = 8, color = 'b', marker='o')
        plt.savefig('plots/test_data.png', format='png')

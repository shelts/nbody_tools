#! /usr/bin/python
#/* Copyright (c) 2018 Siddhartha Shelton */
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Cost function for the data fitting                                      #
# You would need to change depending on the problem                       #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import math as mt

class cost_function: # function to get the cost associated with a parameter set
    def __init__(self, xs, ys):
        self.ys = ys
        self.xs = xs
        
    def least_square(self, function_values): # does a least square calculation. Not fitting function specific
        Rsq = 0.0
        N = float(len(function_values))
        for i in range(0, len(function_values)): 
            Rsq += (self.ys[i] - function_values[i])**2.0
            
        return Rsq**0.5 / N
    
    def function(self, parameters, x_value):# this is the fitting function. Specific to the problem at hand
        m = parameters[0]
        b = parameters[1]
        
        A   = parameters[2]
        mu  = parameters[3]
        sig = parameters[4]
        
        #m2 = parameters[5]
        #b2 = parameters[6]
        
        linear = m * x_value + b # linear model to fit the background
        #linear2 = m2 * x_value + b
        guass = A * mt.exp( -(x_value - mu)**2.0 / (2.0 * sig**2.0)) # guass model to fit the on field 
        
        return linear + guass 
        
    def get_cost(self, parameters): #function to get the costs from a set of parameters
        function_values = []
        for i in range(0, len(self.xs)):
            function_values.append(self.function(parameters, self.xs[i])) # get the function values for each of the data's x values
        
        cost = self.least_square(function_values) # get the cost associated with the function values
        return -cost
    
    
    def generate_plot_points(self, best_paras): # uses the fitting function with the best set of parameters to generate plottable points
        x = -6.0 #TODO: make the parameters here generalizable. right now these are hard coded to my problem
        dx = (6.0 - -6.0) / 100.0
        xs = []
        fs = []
        for i in range(0, 100): 
            f = self.function(best_paras, x) # simple way of getting my function points out
            x += dx
            fs.append(f)
            xs.append(x)
            
        return xs, fs
            
    def plot_current_best(self, counter, best_paras, best_cost): # plots the current best parameter set. unique to this problem
        xs, fs = self.generate_plot_points(best_paras)
        print best_paras, best_cost
        plt.ylim(0, 100)
        plt.xlim(-6, 6)
        plt.plot(xs, fs, linewidth = 2, color = 'r')
        plt.scatter(self.cost.xs, self.cost.ys, s = 8, color = 'b', marker='o')
        plt.savefig('fitting/fit_' + str(counter) + '.png', format='png')
        plt.clf()
        
    
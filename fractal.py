#! /usr/bin/python
#/* Copyright (c) 2016 Siddhartha Shelton */
from nbody_functional import *
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.interpolate import griddata
import math as mt
import random
random.seed(a = 687651463)



class fractal:
    def __init__(self):
        self.xs    = []
        self.funcs = []
        self.c     = 0.2
        self.generator()
        self.plot()
        
    def func(self, x):
        return mt.sin(x) + mt.exp(x) + self.c
    
    def generator(self):
        counter = 0
        counter2 = 0
        N = 1000000
        
        for i in range(N):
            x = random.uniform(0.0, 1.0)
            self.xs.append(x)
            self.funcs.append(self.func(x))
            
            
    
    def plot(self):
        #likelihood_cutoff = -200
        
        #x = np.asarray(self.vals)
        #y = np.asarray(self.vals2)
        #z = np.asarray(sweep.liks) 
        
        #nInterp = 75
        #xi, yi = np.linspace(x.min(), x.max(), nInterp), np.linspace(y.min(), y.max(), nInterp)
        #xi, yi = np.meshgrid(xi, yi)
        #zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

        #plt.figsize=(20, 10)
        #plt.xlabel(titles[coori])
        #plt.ylabel(titles[coorj])        
        
        ##constant DM mass region:
        #plt.plot(const_half_light.rrs, const_half_light.mrs, linestyle = '-', linewidth = 5, color ='grey', alpha = 0.5)
        
        #fitted points:
        plt.scatter(self.xs, self.funcs, s=20, marker= 'o',  color='k', alpha=1, edgecolors='none')
        
        
        #plt.imshow(zi, vmin=likelihood_cutoff, vmax=0, origin='lower', cmap ='winter'  , extent=[x.min(), x.max(), y.min(), y.max()])
        #plt.colorbar()
        plt.show()
        #plt.savefig('fractal.png', format='png', dpi = 300, bbox_inches='tight')
        




run = fractal()
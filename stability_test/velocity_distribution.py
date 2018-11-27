#! /usr/bin/python
#/* Copyright (c) 2016=8 Siddhartha Shelton */
import os
import subprocess
from subprocess import call
import math as mt
import random
import matplotlib.pyplot as plt
os.system('cp ../nbody_functional.py ./')
from nbody_functional import *

class plummer:
    def __init__(self, rscale, mass):
        self.rscale = rscale
        self.mass = mass
        
    def potential(self, r):
        pot = - self.mass / mt.sqrt( r**2 + self.rscale**2 )
        return pot
        
    def density(self, r):
        coeff = 3.0 / (4.0 * mt.pi);
        den = (self.mass / self.rscale**3) * (1.0 + r**2/self.rscale**2 )**(-5./2.);
        den *= coeff;
        return den;
    
    def dist_func(self, v, r):
        
        coeff = 24.0 * mt.sqrt(2.0) / ( 7.0 * mt.pi**3 )
        pot =  self.potential(r)
        energy = -pot - 0.5 * v**2
      
        f = v**2 * coeff *(1. / self.mass**5) * self.rscale**2 * energy*(7./2.)
        return f
    
    def esc_vel(self, r):
        return mt.sqrt(abs( 2. * self.potential(r)))
        

class vel_dist:
    def __init__(self, parameters, out):
        self.rl = parameters[0]
        rr = parameters[1]
        self.ml = parameters[2]
        mr = parameters[3]
        
        self.md = (self.ml / mr) * (1.0 - mr)
        self.rd = (self.rl / rr) * (1.0 - rr)
        print self.rl, self.rd, self.ml, self.md
        
        #self.file_name = file_name
        self.vs = []
        self.out = out 
        self.N_vs =  len(self.out.vs)
        print self.N_vs
        self.get_vs()
        
        
        
    def get_vs(self):
        plum = plummer(self.rl, self.ml)
        for i in range(self.N_vs):
            r = self.out.gc_rs[i]
            #print r
            vesc = plum.esc_vel(r)
            vmax = mt.sqrt(2. / 3.) * vesc
            fmax = plum.dist_func(vmax, r)
            
            while(1):
                v = random.uniform(0.0, 1.0) * vesc
                u = random.uniform(0.0, 1.0)
                f = plum.dist_func(v, r)
                
                if(abs(f / fmax) > u):
                    self.vs.append(v)
                    break
        #print self.vs
    

def plot(bin_vals_theory, bin_vals_data):
    ylimit = 1500
    xlower = 0.0 
    xupper = 10.
    w_adjacent = .1
    print("plotting histograms\n")
            
    plt.bar(bin_vals_data.bin_centers, bin_vals_data.counts, width = w_adjacent, color='r')
    plt.plot(bin_vals_theory.bin_centers, bin_vals_theory.counts, color='k')
    #plt.legend(handles=[mpatches.Patch(color='b', label= plot_hist1)])
    #plt.title('MW@h Test Histogram')
    plt.xlim((xlower, xupper))
    #plt.ylim((0.0, ylimit))
    plt.ylabel('N')
    plt.xlabel('Lambda')

    plt.savefig('vel_theory.png', format='png', bbox_inches='tight')
    plt.clf()
    #plt.show()
    return 1
    

def main():
    path = '/home/sidd/Desktop/research/nbody_tools/stability_test/'
    file1 = path + 'outputs/output_plummer_plummer_0gy_same1.out'
    #file2 = 'output_plummer_plummer_4gy_same'
    
    p = [0.2, 0.5, 6., 0.5]
    out = nbody_outputs(file1)
    out.dark_light_split()
    
    binned_vs_data = binner([0.0, 10.], 20, out.light_vs)
    theory = vel_dist(p, out)
    binned_vs = binner([0.0, 10.], 20, theory.vs)
    
    
    plot(binned_vs, binned_vs_data)
    
main()
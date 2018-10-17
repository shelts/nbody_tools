#! /usr/bin/python3
#/* Copyright (c) 2018 Siddhartha Shelton */

import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math as mt
import matplotlib.patches as mpatches
import random
random.seed(a = 486813)#teletraan
#import sys
#sys.path.insert(0,'/sidd/Desktop/research/nbody_tools/')
#sys.path.append('../..')
os.system('cp ../nbody_functional.py ./')
from nbody_functional import *




class lb_cm:
    def __init__(self, filename, sigma_cutoff):
        self.filename = filename
        self.outliers_removed = 0
        self.sigma_cutoff = sigma_cutoff
        self.out = nbody_outputs(filename)
        self.out.dark_light_split()
        self.make_list()
        self.get_cm()
        
    def make_list(self):
        self.Ns = []
        for i in range(len(self.out.light_l)):
            self.Ns.append(i)
    
    def get_cm(self):
        cm_l = self.out.light_m[0] * self.out.light_l[0] 
        cm_b = self.out.light_m[0] * self.out.light_b[0] 
        cm_r = self.out.light_m[0] * self.out.light_r[0] 
        M_t  = self.out.light_m[0]
        for i in range(0, len(self.out.light_l)):
            cm_l += self.out.light_m[i] * self.out.light_l[i] 
            cm_b += self.out.light_m[i] * self.out.light_b[i] 
            cm_r += self.out.light_m[i] * self.out.light_r[i] 
            M_t  += self.out.light_m[i]
            
        self.cm_l = cm_l / M_t
        self.cm_b = cm_b / M_t
        self.cm_r = cm_r / M_t
        self.cm_lb = mt.sqrt( self.cm_l * self.cm_l + self.cm_b * self.cm_b)
    
  
    
    def calc_sigma(self):
        N = len(self.Ns)
        skipping = False
        counter = 0
        for i in (self.Ns):
            rsq = self.out.light_l[i] * self.out.light_l[i] + self.out.light_b[i] * self.out.light_b[i]
            r = mt.sqrt(rsq)
            if(counter == 0):
                sigma = (self.cm_lb - r)**2.0
            else:
                sigma += (self.cm_lb - r)**2.0
            counter += 1
            
            
        N = len(self.Ns)
        self.sigma_sq = sigma / (N - 1.)
        self.sigma    = mt.sqrt(self.sigma_sq)
        
    def outlier_rej(self):
        counter = 0
        while(counter < 30):
            skipping = False
            skip_is = []
            index = 0
            for i in (self.Ns):
                rsq = self.out.light_l[i] * self.out.light_l[i] + self.out.light_b[i] * self.out.light_b[i]
                r = mt.sqrt(rsq)
                if(abs(self.cm_lb - r) > self.sigma * self.sigma_cutoff):
                    skip_is.append(index) #get the index of the outlier
                    self.outliers_removed += 1
                index += 1
            for i in sorted(skip_is, reverse = True): #sort the indices in order from largest to smallest        
                del self.Ns[i]#remove the indices from the list without affecting the others.

            self.calc_sigma()
            #print('sigma: ', self.sigma, '\titeration: ', counter, '\ttotal removed: ', self.outliers_removed)
            counter += 1
                    
    
    def vel_dispersion(self):
        vsum_sq = 0.
        vsum    = 0.
        baryon_mass = 0
        for i in self.Ns:
            baryon_mass += self.out.light_m[i]
            vsq = self.out.light_vx[i] * self.out.light_vx[i] + self.out.light_vy[i] * self.out.light_vy[i] + self.out.light_vz[i] * self.out.light_vz[i]
            v   = mt.sqrt(vsq)
            
            vsum_sq += vsq
            vsum    += v
            
        N = len(self.Ns)
        self.v_sigmasq = vsum_sq / (N - 1.) - (N / (N - 1.)) * (vsum / N)**2.0
        self.baryon_mass = baryon_mass
        #print(self.v_sigmasq)
        
        
    def determine_mass(self):
        M = self.v_sigmasq * self.cm_r
        print('predicted total mass: ', M)
        print('baryon mass: ', self.baryon_mass)
        print('predicted DM mass: ', M - self.baryon_mass)
        
            
            
    def distance(self, l, b):
        dist = mt.sqrt( (self.cm_l - l)**2.0 + (self.cm_b - b)**2.0 )
        return dist               
        
    def solve_b(self, l, R):
        #print(l, R)
        #print(R * R - (l - self.cm_l)**2.0)
        b1 = mt.sqrt(abs(R * R - (l - self.cm_l)**2.0)) + self.cm_b
        b2 = -mt.sqrt(abs(R * R - (l - self.cm_l)**2.0)) + self.cm_b 
        return b1, b2
        
    def make_circle(self):
        self.circle_l = []
        self.circle_b = []
        
        counter = 1 
        threshold = self.sigma
        l = self.cm_l - threshold 
        #print(self.cm_l, l)
        while( l < (self.cm_l + threshold) ):
            #print(self.cm_l + l)
            b1, b2 = self.solve_b(l, threshold)
            
            #if(r == threshold):
            self.circle_l.append(l)
            self.circle_b.append(b1)
            
            self.circle_l.append(l)
            self.circle_b.append(b2)
            l += 0.001
            counter += 1
            #print(counter)
                
        #print(len(self.circle_l))
        
        
    def plot(self):
        plt.figure(figsize=(10, 10))
        xlower = 200.0
        xupper = 240.0
        ylower = 35
        yupper = 75
        plt.xlim((xlower, xupper))
        plt.ylim((ylower, yupper))
        plt.xlabel('l')
        plt.ylabel('b')
        plt.title('l vs b')

        plt.scatter(self.out.light_l, self.out.light_b,  s = 0.5, color = 'b', alpha=.5, marker = '.', label = 'baryons')
        plt.scatter(self.cm_l, self.cm_b, s = 10., color = 'red', alpha=1.0, marker = 'o', label = 'CM')
        plt.scatter(self.circle_l, self.circle_b,  s = 0.1, color = 'k', alpha=1, marker = '+', label = r'2.5$\sigma$ radius')
        
        plt.legend()
        plt.savefig('lb_cm.png', format='png', dpi=500)

        
        

def main():
    folder = '/home/sidd/Desktop/research/quick_plots/hists_outs/'
    filename = 'slightly_disrupt.out'
    
    sigma_cutoff = 3
    
    a = lb_cm(folder + filename, sigma_cutoff)
    a.calc_sigma()
    a.outlier_rej()
    a.vel_dispersion()
    a.determine_mass()
    a.make_circle()
    a.plot()
main()
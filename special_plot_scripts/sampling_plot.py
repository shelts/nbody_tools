#! /usr/bin/python
#/* Copyright (c) 2018 Siddhartha Shelton */
import random
import math as mt
import matplotlib.pyplot as plt
random.seed(a = 687651463)

class sampling:
    def __init__(self, scale_r, M):
        self.radii = []
        self.funcp = []
        self.fs    = []
        self.throw_away_r = []
        self.throw_away_funcp = []
        
        self.M = M
        self.a = scale_r
        self.max_r = mt.sqrt(2.0 / 3.0) * scale_r
        self.max_rsq_rho = self.plummer_rsq_den(self.max_r)
        
        
    def plummer_rsq_den(self, r):
        coeff = (3.0 * self.M) / (4.0 * mt.pi * self.a**3.0)
        quot = ((r * r) / (self.a * self.a))
        
        den = coeff * r * r * (1.0 + quot)**(-5.0 / 2.0)
        return den
        
    def rejection_sample(self):
        counter = 0
        counter2 = 0
        N = 10000
        self.massper = self.M / float(N)
        
        while(counter < N):
            u = random.uniform(0.0, 1.0)
            r = random.uniform(0.0, 1.0) * 10. * self.a
            
            rsq_rho = self.plummer_rsq_den(r) 
            test = rsq_rho / (self.max_rsq_rho)
            
            if(test >= u):
                self.radii.append( r)
                self.funcp.append(u * self.max_rsq_rho)
                counter += 1
            else:
                counter2 += 1
                self.throw_away_r.append( r)
                self.throw_away_funcp.append(u * self.max_rsq_rho )
        
        
        
    def get_func_vals(self, dN):
        x = 0.001
        self.rs = []
        self.fs = []
        self.fs_hist = []
        for i in range(1000):
            self.rs.append(x)
            self.fs.append(self.plummer_rsq_den(x))
            self.fs_hist.append(4.0 * mt.pi * self.plummer_rsq_den(x) * dN / self.massper)
            x += 0.01
    
    
    def bin_all(self, radii):
        binN = 50
        bin_upper = 2.0
        bin_lower = 0.0
        bin_width = abs(bin_upper - bin_lower) / float(binN)
        counts = []
        bins = []
        cur_bin_lower = bin_lower
        cur_bin_upper = bin_lower + bin_width
        
        for j in range(binN):
            counts.append(0.0)
            bins.append(bin_lower + bin_width * (j + 0.5) ) 
        
        for i in range(0, len(radii)):
            cur_bin_lower = bin_lower
            cur_bin_upper = bin_lower + bin_width
            for j in range(0, binN):
                if(radii[i] > cur_bin_lower and radii[i] <= cur_bin_upper):
                    counts[j] += 1.0 
                    break
                cur_bin_lower += bin_width 
                cur_bin_upper += bin_width
            
        self.counts = counts
        self.bins = bins
        self.bin_width = bin_width
    
    def plot(self, plot_name):
        plt.figure(figsize=(20, 10))
        plt.ylim(0.0, 2.65)
        plt.xlim(0.0, 1.5)
        plt.tick_params(axis='y', which='major', labelsize=24)
        plt.tick_params(axis='x', which='major', labelsize=24)
        plt.xlabel('Radius (kpc)', fontsize=28)
        plt.ylabel(r'r$^2$ $\rho$', fontsize=28)
        plt.plot(self.radii, self.funcp, '+', markersize = 1, color = 'g', marker = '+')
        plt.plot(self.throw_away_r, self.throw_away_funcp, '.', markersize = 1.0, color = 'r', marker = 'o')
        plt.plot(self.rs, self.fs, color = 'k', linewidth = 2.5, linestyle = '-')
        plt.savefig("sampling_plot" + plot_name + ".eps", format='eps')
        plt.clf()
    
    def plot_hists(self, counts, bins, plot_name):
        #plt.ylim(0.0, 3.0)
        plt.xlim(0.0, 1.5)
        #print len(self.rs), len(self.fs)
        #print counts
        plt.plot(self.rs, self.fs_hist, color = 'k', linewidth = 2, linestyle = '-')
        plt.bar(bins, counts, color = 'g', width = 0.05)
        plt.savefig("sampling_plot" + plot_name + ".png", format='png')
        plt.clf()
        

def main():
    s = sampling(0.2, 12)
    s.rejection_sample()
    s.bin_all(s.radii)
    s.get_func_vals(s.bin_width)
    s.plot_hists(s.counts, s.bins, '2')
    s.plot('')
    
    #s.bin_all(s.throw_away_r)
    #s.get_func_vals(s.bin_width)
    #s.plot_hists(s.counts, s.bins, '3')
    
    
main()
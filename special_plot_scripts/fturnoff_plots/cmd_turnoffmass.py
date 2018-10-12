#! /usr/bin/python
#/* Copyright (c) 2016 Siddhartha Shelton */

import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math as mt
import matplotlib.patches as mpatches


class cmd:
    class star:
        def __init__(self, g, r, ra, dec, gmr):
            self.g = g
            self.r = r
            self.ra = ra
            self.dec = dec
            self.gmr = gmr
            
    def __init__(self, file_name):
        self.file_name = file_name
        self.stars   = []
        
        self.parse()
    
    def parse(self):
        f = open(self.file_name, 'r')
        for line in f:
            if (line.startswith("#") or line.startswith("objid")):
                continue
            ss = line.split(',')
            ra  = float(ss[1])
            dec = float(ss[2])
            g = float(ss[4])
            r = float(ss[5])
            s = self.star(g, r, ra, dec, g - r)
            self.stars.append(s)
        
        f.close()

    def fturnoff_select(self):
        self.fturnoffs = []
        for i in range(len(self.stars)):
            if(self.stars[i].gmr > 0.12 and self.stars[i].gmr < 0.26):
                self.fturnoffs.append(self.stars[i])
                
                
        print 'number of F-turnoffs: ', len(self.fturnoffs)

    def plummer_model(self):
        def den(r, M, a):
            return (3.0 * M / a**3) * (1.0 + r**2/ a**2)**(-5. / 2.)
        #M = 3.0e4 #solar masses
        M = 822
        #M = 2577 #table 3
        a = 0.0184 / 1.3
        r = 0.0
        mp = 1.
        self.plummer_countrs = []
        self.plummer_dN = []
        while(r < 10.0 * a):
            count = r * r * den(r, M, a) * self.bin_width / mp
            self.plummer_dN.append(count)
            self.plummer_countrs.append(r)
            r += 0.001
    
    def data_binner(self):
        def angular_dist(ra1, dec1, ra2, dec2):
            ra1  = mt.radians(ra1)
            dec1 = mt.radians(dec1)
            ra2  = mt.radians(ra2)
            dec2 = mt.radians(dec2)
            
            cosD =  mt.cos(mt.pi / 2. - dec1) * mt.cos(mt.pi / 2. - dec2) 
            cosD += mt.sin(mt.pi / 2. - dec1) * mt.sin(mt.pi / 2. - dec2) * mt.cos(ra1 - ra2)
            D = mt.acos(cosD)
            D = mt.degrees(D)
            return D
        
        center_ra = 229.025
        center_de = -.125
        #print angular_dist(center_ra, center_de, 228.98 , -.1)
        
        outer_ra =  229.08
        #outer_ra =  229.16 #table 3
        
        binN = 20
        self.bin_width = angular_dist(center_ra, center_de, outer_ra , center_de) / binN
        
        self.star_N = []
        self.bin_mids = []
        loc = self.bin_width / 2.0
        
        for i in range(binN):
            self.star_N.append(0)
            loc += self.bin_width 
            self.bin_mids.append(loc)
        print len(self.stars)
        for i in range(len(self.stars)):
            dist = angular_dist(center_ra, center_de, self.stars[i].ra, self.stars[i].dec)
            for j in range(binN):
                if(dist < (self.bin_mids[j] + self.bin_width / 2.) and dist > (self.bin_mids[j] - self.bin_width / 2.)):
                    self.star_N[j] += 1
                    break
        #print self.star_N
        
        
    def plot_cmd(self):
        plt.ylim((30, 10))
        plt.xlim((-1, 3))
        plt.xlabel('(g-r)')
        plt.ylabel('g')
        for i in range(len(self.stars)):
            plt.plot(self.stars[i].gmr, self.stars[i].g, '.', markersize = 1, color = 'r', marker = 'o')
        for i in range(len(self.fturnoffs)):
            plt.plot(self.fturnoffs[i].gmr, self.fturnoffs[i].g, '.', markersize = 1, color = 'b', marker = '+')
        plt.savefig('CMD.png', format='png', bbox_inches='tight')
        
        plt.clf()
        plt.xlabel('RA')
        plt.ylabel('DEC')
        #plt.ylim((28.25, 28.75))
        #plt.xlim((211.25, 211.75))
        for i in range(len(self.stars)):
            plt.plot(self.stars[i].ra, self.stars[i].dec, '.', markersize = 1, color = 'r', marker = 'o')
        for i in range(len(self.fturnoffs)):
            plt.plot(self.fturnoffs[i].ra, self.fturnoffs[i].dec, '+', markersize = 3, color = 'b', marker = '+')
        plt.savefig('ra_dec.png', format='png', bbox_inches='tight')
    
    
    
    def plot_counts(self):
        #plt.ylim((0, 100))
        plt.xlim((0.0, 0.2))
        plt.xlabel('r')
        plt.ylabel('dN')
        plt.plot(self.plummer_countrs, self.plummer_dN, linewidth = 1, color = 'r')
        plt.bar(self.bin_mids, self.star_N, width = .001, color='r')
        plt.savefig('star_counts.png', format='png', bbox_inches='tight')
        
def main():
    file_name = 'MyTable_5_shelts.csv'
    cd = cmd(file_name)
    #cd.fturnoff_select()
    #cd.plot_cmd()
    cd.data_binner()
    cd.plummer_model()
    cd.plot_counts()
    
main()
    